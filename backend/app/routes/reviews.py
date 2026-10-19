from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.auth.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.restaurant import Restaurant
from app.models.reservation import Reservation, ReservationStatus
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewResponse, RatingSummary
from app.schemas.review import ReviewCreate, RatingSummary, ReviewResponse

router = APIRouter(tags=["reviews"])

@router.post("/reviews", response_model=ReviewResponse)
def create_review(
    data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reservation = db.query(Reservation).filter(
        Reservation.id == data.reservation_id,
        Reservation.customer_id == current_user.id,
    ).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    if reservation.status != ReservationStatus.completed:
        raise HTTPException(
            status_code=400,
            detail="You can only review a completed reservation",
        )

    if reservation.status != ReservationStatus.completed:
        raise HTTPException(
            status_code=400,
            detail="You can only review a completed reservation",
        )

    existing = db.query(Review).filter(Review.reservation_id == reservation.id).first()

    if existing:
        raise HTTPException(status_code=400, detail="You already reviewed this reservation")

    review = Review(
        reservation_id = reservation.id,
        customer_id = current_user.id,
        restaurant_id = reservation.restaurant_id,
        rating = data.rating,
        comment = data.comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)

    return review


@router.get("/resetaurants/{restaurant_id}/reviews", response_model=list[ReviewResponse])
def list_restaurant_reviews(restaurant_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Review)
        .filter(Review.restaurant_id == restaurant_id)
        .order_by(Review.created_at.desc())
        .all()
    )


@router.get("/restaurants/{restaurant_id}/rating", response_model=RatingSummary)
def get_restaurant_rating(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    avg_rating, review_count = (
        db.query(func.avg(Review.rating), func.count(Review.id))
        .filter(Review.restaurant_id == restaurant_id)
        .one()
    )

    return RatingSummary(
        restaurant_id=restaurant_id,
        average_rating=round(float(avg_rating), 2) if avg_rating is not None else None,
        review_count=review_count,
    )