from pydantic import BaseModel

class TableCreate(BaseModel):
    label: str
    seats: int

class TableResponse(BaseModel):
    id: int
    restaurant_id: int
    label: str
    seats: int

    class Config:
        from_attributes = True