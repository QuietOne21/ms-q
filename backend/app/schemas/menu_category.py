from pydantic import BaseModel

class MenuCategoryCreate(BaseModel):
    name: str

class MenuCategoryResponse(BaseModel):
    id: int
    restaurant_id: int
    name: str

    class Config:
        from_attribute = True