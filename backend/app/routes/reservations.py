from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.reservation import Reservation
from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.services.availability import find_available_table

from app.models.reservation import ReservationStatus

router = APIRouter(prefix="/reservations", tags=["reservations"])

@router.post("/", response_model=ReservationResponse)
def create_reservation(
    data: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == data.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    table = find_available_table(
        db, data.restaurant_id, data.party_size, data.date, data.time
    )

    if not table:
        raise HTTPException(
            status_code=409,
            detail="No available table for the requested date, time, and party size",
        )

    reservation = Reservation(
        customer_id=current_user.id,
        restaurant_id=data.restaurant_id,
        table_id=table.id,
        date=data.date,
        time=data.time,
        party_size=data.party_size,
        special_requests=data.special_requests,
    )
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation

@router.get("/", response_model=list[ReservationResponse])
def list_my_reservations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Reservation).filter(Reservation.customer_id == current_user.id).all()

@router.put("/{reservation_id}/cancel", response_model=ReservationResponse)
def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id,
        Reservation.customer_id == current_user.id,
    ).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    if reservation.status not in (ReservationStatus.pending, ReservationStatus.confirmed):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel a reservation with status '{reservation.status.value}' "
        )

    reservation.status = ReservationStatus.cancelled
    db.commit()
    db.refresh(reservation)
    return reservation