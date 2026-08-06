from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field

#Order Status - (Enum)- preparing,picked_up,in_transit,delivered,cancelled
class OrderStatus(Enum):
    PREPARING = "preparing"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

#Database Model for Order
class Order(SQLModel,table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str = Field(..., min_length=3, max_length=100)
    delivery_address: str = Field(..., min_length=3, max_length=200)
    items:str
    status: OrderStatus = Field(default=OrderStatus.PREPARING)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

#Schema for creating a new order
class OrderCreate(SQLModel):
    customer_name:str
    delivery_address:str
    items:str

#Schema for updating an order
class OrderUpdate(SQLModel):
    customer_name: Optional[str] = None
    delivery_address: Optional[str] = None
    status:Optional[OrderStatus] = None

#Database Model for Status List
class StatusLog(SQLModel):
    order_id:int
    old_status:str
    new_status:str
    changed_at:datetime
