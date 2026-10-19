from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal
from app.auth.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.reservation import  Reservation, ReservationStatus
from app.models.order import Order
from app.models.payment import Payment, PaymentStatus
from app.models.restaurant import Restaurant
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services.payment_service import process_payment

PAYABLE_STATUSES = (ReservationStatus.pending, ReservationStatus.confirmed)

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/", response_model=PaymentResponse)
def create_payment(
    data: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reservation = db.query(Reservation).filter(
        Reservation.id == data.reservation_id,
        Reservation.customer_id == current_user.id,
    ).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    if reservation.status not in PAYABLE_STATUSES:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot pay for a reservation with status '{reservation.status.value}'",
        )

    existing_payment = db.query(Payment).filter(Payment.reservation_id == reservation.id).first()
    if existing_payment:
        raise HTTPException(status_code=400, detail="This reservation has already been paid")

    order = db.query(Order).filter(Order.reservation_id == reservation.id).first()
    order_total = Decimal("0.00")
    if order:
        order_total = sum(item.quantity * item.price_at_time_of_order for item in order.items)

    restaurant = db.query(Restaurant).filter(Restaurant.id == reservation.restaurant_id).first()
    amount = restaurant.reservation_fee + order_total

    result = process_payment(float(amount))

    payment = existing_payment or Payment(reservation_id=reservation.id)
    payment.amount = amount
    payment.status = PaymentStatus.successful if result["success"] else PaymentStatus.failed
    payment.payment_reference = result["reference"]
    db.add(payment)

    if result["success"]:
        reservation.status = ReservationStatus.confirmed

    db.commit()
    db.refresh(payment)

    if not result["success"]:
        raise HTTPException(
            status_code= 402,
            detail="Payment failed. Please try again.",
        )

    return payment