from fastapi import FastAPI, HTTPException, status

from app.models import Product
from app.schemas import ProductCreate, ProductUpdate

app = FastAPI(
    title="Product Management API",
    description="Backend application for CI and security pipeline practice",
    version="1.0.0",
)

products: dict[int, Product] = {}
next_product_id = 1


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "Product Management API is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate) -> Product:
    global next_product_id

    new_product = Product(
        id=next_product_id,
        **product.model_dump(),
    )

    products[next_product_id] = new_product
    next_product_id += 1

    return new_product


@app.get("/products")
def get_products() -> list[Product]:
    return list(products.values())


@app.get("/products/{product_id}")
def get_product(product_id: int) -> Product:
    product = products.get(product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    product_data: ProductUpdate,
) -> Product:
    existing_product = products.get(product_id)

    if existing_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    updated_data = existing_product.model_dump()
    changes = product_data.model_dump(exclude_unset=True)
    updated_data.update(changes)

    updated_product = Product(**updated_data)
    products[product_id] = updated_product

    return updated_product


@app.delete("/products/{product_id}")
def delete_product(product_id: int) -> dict[str, str]:
    if product_id not in products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    del products[product_id]

    return {"message": "Product deleted successfully"}
