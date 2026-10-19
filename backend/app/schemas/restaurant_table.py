from pydantic import BaseModel, Field

class TableCreate(BaseModel):
    label: str
    seats: int = Field(gt=0, le=20)

class TableResponse(BaseModel):
    id: int
    restaurant_id: int
    label: str
    seats: int

    class Config:
        from_attributes = True