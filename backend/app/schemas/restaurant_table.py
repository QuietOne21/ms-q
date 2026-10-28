from pydantic import BaseModel, Field

class TableCreate(BaseModel):
    label: str = Field(min_length=1, max_digits=255)
    seats: int = Field(gt=0, le=20)

class TableResponse(BaseModel):
    id: int
    restaurant_id: int
    label: str
    seats: int

    class Config:
        from_attributes = True