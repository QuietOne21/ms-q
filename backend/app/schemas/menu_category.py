from pydantic import BaseModel, Field

class MenuCategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)

class MenuCategoryResponse(BaseModel):
    id: int
    restaurant_id: int
    name: str

    class Config:
        from_attribute = True