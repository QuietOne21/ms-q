from datetime import datetime, timedelta, date, time
from sqlalchemy.orm import Session
from app.models.reservation import Reservation, ReservationStatus
from app.models.restaurant_table import RestaurantTable

from sqlalchemy import func, text

RESERVATION_DURATION_MINUTES = 90

PENDING_HOLD_MINUTES = 15
MAX_PENDING_PER_CUSTOMER = 3

def hold_cutoff():
    return func.date_sub(func.now(), text(f"INTERVAL {PENDING_HOLD_MINUTES} MINUTE"))

def expire_stale_pending_reservations(db: Session, restaurant_id: int) -> None:
    db.query(Reservation).filter(
        Reservation.restaurant_id == restaurant_id,
        Reservation.status == ReservationStatus.pending,
        Reservation.created_at < hold_cutoff(),
    ).update({Reservation.status: ReservationStatus.cancelled}, synchronize_session=False)

def _reservation_window(res_date: date, res_time: time) -> tuple[datetime, datetime]:
    start = datetime.combine(res_date, res_time)
    end = start + timedelta(minutes=RESERVATION_DURATION_MINUTES)
    return start, end

def find_available_table(
    db: Session,
    restaurant_id: int,
    party_size: int,
    res_date: date,
    res_time: time,
) -> RestaurantTable | None:
    requested_start, requested_end = _reservation_window(res_date, res_time)

    candidate_tables = (
        db.query(RestaurantTable)
        .filter(
            RestaurantTable.restaurant_id == restaurant_id,
            RestaurantTable.seats >= party_size,
        )
        .all()
    )

    active_statuses = [ReservationStatus.pending, ReservationStatus.confirmed]

    for table in candidate_tables:
        existing_reservations = (
            db.query(Reservation)
            .filter(
                Reservation.table_id == table.id,
                Reservation.date == res_date,
                Reservation.status.in_(active_statuses),
            )
            .all()
        )

        has_conflict = False
        for existing in existing_reservations:
            existing_start, existing_end = _reservation_window(existing.date, existing.time)
            if requested_start < existing_end and existing_start < requested_end:
                has_conflict = True
                break

        if not has_conflict:
            return table

    return None