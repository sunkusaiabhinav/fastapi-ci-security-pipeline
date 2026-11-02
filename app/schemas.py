from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    price: float = Field(gt=0)
    description: str = Field(default="", max_length=500)


class ProductUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    price: float | None = Field(default=None, gt=0)

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    in_stock: bool | None = None
