from fastapi import APIRouter, Depends, HTTPException,Query
from sqlmodel import Session, select
from db import get_session
from model import Order, OrderCreate, OrderUpdate, StatusLog, OrderStatus
from datetime import datetime


router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=Order)
def create_order(order: OrderCreate, session: Session = Depends(get_session)):
    new_order = Order(**order.model_dump())
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return new_order

@router.get("/", response_model=Order)
def list_orders(
    status: OrderStatus | None = Query(default=None,description="Filter by order status"),
    created_at: str | None = Query(default=None,description="Filter by created at"),
    skip: int = Query(0,ge=0,description="Number of items to skip"),
    limit: int = Query(10,ge=1,le=100,description="Number of items to return"),
    session: Session = Depends(get_session)
):
    query = select(Order)
    if status:
        query = query.where(Order.status == status)
    if created_at:
        start = datetime.combine(created_at, datetime.min.time())
        end = datetime.combine(created_at, datetime.max.time())
        query = query.where(Order.created_at >= start, Order.created_at <= end)
        
    query = query.offset(skip).limit(limit)
    orders = session.exec(query).all()
    return orders


