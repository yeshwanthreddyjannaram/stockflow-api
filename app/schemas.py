from pydantic import BaseModel, Field
from typing import Literal


class CategoryCreate(BaseModel):
    name: str = Field(min_length= 3, max_length= 50)
    
class CategoryResponse(BaseModel):
    id : int
    name : str
    
    model_config = {"from_attributes": True}
    
class ProductCreate(BaseModel):
    name: str = Field(min_length= 2, max_length= 100)
    price: float = Field(gt=0)
    stock_quantity: int =Field(ge=0)
    category_id: int = Field(gt=0)
    
class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock_quantity: int
    category_id: int = Field(gt=0)
    
    model_config = {"from_attributes": True}
    
    

class OrderItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    customer_name: str = Field(min_length=2, max_length=100)
    items: list[OrderItemCreate]= Field(min_length=1)


class OrderItemResponse(BaseModel):
    id: int
    product_id: int = Field(gt=0)
    quantity: int
    price: float

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: int
    customer_name: str = Field(min_length=2, max_length=100)
    total_amount: float
    status: str
    items: list[OrderItemResponse]

    model_config = {"from_attributes": True}

class OrderStatusUpdate(BaseModel):
    status: Literal[
        "pending",
        "confirmed",
        "shipped",
        "delivered",
        "cancelled"
    ]