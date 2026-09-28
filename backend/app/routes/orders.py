from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.reservation import Reservation
from app.models.menu_item import MenuItem
from app.models.order import Order, OrderItem
from app.schemas.order import OrderCreate, OrderResponse

router = APIRouter(prefix="/orders", tags=["orders"])

def _build_order_response(order: Order) -> OrderResponse:
    total = sum(item.quantity * item.price_at_time_of_order for item in order.items)
    return OrderResponse(
        id=order.id,
        reservation_id=order.reservation_id,
        status=order.status,
        created_at=order.created_at,
        items=order.items,
        total=total,
    )

@router.post("/", response_model=OrderResponse)
def create_order(
    data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reservation = db.query(Reservation).filter(
        Reservation.id == data.reservation_id,
        Reservation.customer_id == current_user.id,
    ).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    existing_order = db.query(Order).filter(Order.reservation_id == reservation.id).first()
    if existing_order:
        raise HTTPException(status_code=400, detail="This reservation already has an order")

    if not data.items:
        raise HTTPException(status_code=400, detail="Order must contain at least one item")

    order = Order(reservation_id=reservation.id)
    db.add(order)
    db.flush()

    for item_data in data.items:
        menu_item = db.query(MenuItem).filter(
            MenuItem.id == item_data.menu_item_id,
            MenuItem.restaurant_id == reservation.restaurant_id,
        ).first()

        if not menu_item:
            raise HTTPException(
                status_code=400,
                detail=f"'Menu item {item_data.menu_item_id}' not found for this restaurant",
            )

        if not menu_item.is_available:
            raise HTTPException(
                status_code=400,
                detail=f"'{menu_item.name}' is currently unavailable",
            )

        order_item = OrderItem(
            order_id=order.id,
            menu_item_id=menu_item.id,
            quantity=item_data.quantity,
            price_at_time_of_order=menu_item.price,
        )
        db.add(order_item)

    db.commit()
    db.refresh(order)
    return _build_order_response(order)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = (
         db.query(Order)
        .join(Reservation)
        .filter(Order.id == order_id, Reservation.customer_id == current_user.id)
        .first()
    )

    if not order:
        raise HTTPException(status_code=404, detail="order not found")

    return _build_order_response(order)