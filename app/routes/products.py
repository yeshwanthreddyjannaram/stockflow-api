from fastapi import APIRouter, status, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from sqlalchemy.exc import IntegrityError

router= APIRouter(prefix= "/products", tags= ["Products"])


#============== > Post Product < ==============
@router.post("/", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    
    category = db.query(models.Category).filter(models.Category.id == product.category_id).first()
    
    if not category:
        raise HTTPException(
            status_code= 404,
            detail= "Category not found"
        )
    
    new_product=models.Product(
        name= product.name,
        price= product.price,
        stock_quantity= product.stock_quantity,
        category_id= product.category_id
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return new_product


# ==================== > Get Products < ======================
@router.get("/", response_model= list[schemas.ProductResponse])
def get_products( search : str = None , category_id : int= None , max_price: float = None ,
                 skip: int =Query(0, ge=0),limit: int =Query(10, ge=1),db: Session= Depends(get_db)):
    query=db.query(models.Product) 
    
    if search:
        query= query.filter(models.Product.name.ilike(f"%{search}%"))
        
    if category_id is not None:
        query= query.filter(models.Product.category_id == category_id)
       
    if max_price is not None:
        query= query.filter(models.Product.price <=max_price)
    
    products=query.offset(skip).limit(limit).all()
    
    return products
    
    
#  =================== > GET Product By ID < ===================
@router.get("/{product_id}", response_model=schemas.ProductResponse)
def get_product_by_id(product_id: int, db: Session= Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code= 404,
            detail= "Product not found"
        )
    return product


# ==================== > Update Product < ========================

@router.put("/{product_id}", response_model=schemas.ProductResponse)
def update_product(
    product_id: int,
    product_data: schemas.ProductCreate,
    db: Session = Depends(get_db)
):
    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    category = db.query(models.Category).filter(
        models.Category.id == product_data.category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    product.name = product_data.name
    product.price = product_data.price
    product.stock_quantity = product_data.stock_quantity
    product.category_id = product_data.category_id

    db.commit()
    db.refresh(product)

    return product


# =================== > Delete Product < ===================
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):

    product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Check whether this product is used in existing orders
    existing_order_item = db.query(models.OrderItem).filter(
        models.OrderItem.product_id == product_id
    ).first()

    if existing_order_item:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete product because it is associated with existing orders"
        )

    # Delete product safely
    try:
        db.delete(product)
        db.commit()

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Cannot delete product because it is associated with existing orders"
        )

    return {
        "message": "Product deleted successfully"
    }