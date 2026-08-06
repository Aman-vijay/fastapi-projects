from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from db import get_session
from model import StatusLog, OrderStatus,Order
from datetime import datetime, date 

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/daily", response_model=list[StatusLog])
def get_daily_summary(
    summary_date:date |None = Query(default=None,description="Filter by summary date"),
    session: Session = Depends(get_session)
):
    if summary_date is None:
        summary_date = date.today()

    start = datetime.combine(summary_date, datetime.min.time())
    end = datetime.combine(summary_date, datetime.max.time())

    summary = {}
    total_orders = 0

    for status in OrderStatus:
        count = session.exec(select(func.count(Order.id)).
        where(Order.status == status,
        Order.created_at >= start,
        Order.created_at <= end
        )).one_or_none()

        summary[status.value] = count or 0
        total_orders += count or 0

    return {
        "date": summary_date.isoformat(),
        "by_status": summary,
        "total_orders": total_orders
    }





