from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

# ================ > Create An Order < ================
@router.post("/", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order_data: schemas.OrderCreate, db: Session = Depends(get_db)):
    try:
        
        new_order = models.Order(
            customer_name = order_data.customer_name,
            total_amount = 0,
            status = "pending"
        )
    
        db.add(new_order)
        db.flush()
    
        total_amount = 0
    
        for item in order_data.items:
            product = db.query(models.Product).filter(models.Product.id ==item.product_id).first()
        
            if not product:
                raise HTTPException(
                    status_code= 404,
                    detail = f"product with ID {item.product_id} not found"
                )
            
            if product.stock_quantity < item.quantity:
                raise HTTPException(
                    status_code= 400,
                    detail = f"Insufficient stock for product {product.name}"
                )
            
            order_item = models.OrderItem(
                order_id = new_order.id,
                product_id = product.id,
                quantity = item.quantity,
                price = product.price
            )
        
            db.add(order_item)
            total_amount+=product.price * item.quantity
    
            product.stock_quantity -= item.quantity
        
        new_order.total_amount = total_amount
    
        db.commit()
        db.refresh(new_order)
    
        return new_order
    
    except Exception:
        db.rollback()
        raise
    
    
# ===================== > Get Orders < =====================
@router.get("/", response_model= list[schemas.OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    
    return orders
    
# ===================== > Gt Order By ID < =====================
@router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order_by_id(order_id : int, db : Session= Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code= 404,
            detail = "Order not found"
        )
        
    return order


# ================= > Update Order Status < ==================
@router.put("/{order_id}/status", response_model=schemas.OrderResponse)
def update_order_status(
    order_id: int,
    status_data: schemas.OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    order = db.query(models.Order).filter(
        models.Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    allowed_transitions = {
        "pending": ["confirmed"],
        "confirmed": ["shipped"],
        "shipped": ["delivered"],
        "delivered": [],
        "cancelled": []
    }

    if status_data.status not in allowed_transitions[order.status]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot change order status from {order.status} to {status_data.status}"
        )

    order.status = status_data.status

    db.commit()
    db.refresh(order)

    return order

# ================ > Cancellation Order < ===================
@router.put("/{order_id}/cancel", response_model=schemas.OrderResponse)
def cancel_order(order_id: int, db: Session = Depends(get_db)):

    order = db.query(models.Order).filter(
        models.Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order.status not in ["pending", "confirmed"]:
        raise HTTPException(
            status_code=400,
            detail="Only pending and confirmed orders can be cancelled"
        )

    try:
        for item in order.items:
            item.product.stock_quantity += item.quantity

        order.status = "cancelled"

        db.commit()
        db.refresh(order)

        return order

    except Exception:
        db.rollback()
        raise