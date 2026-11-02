from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int
    name: str = Field(min_length=2, max_length=100)
    price: float = Field(gt=0)
    description: str = Field(default="", max_length=500)
    in_stock: bool = True
