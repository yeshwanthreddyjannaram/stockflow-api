from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/categories", tags=["categories"])


# ============== > Post Category < ==================
@router.post("/", response_model=schemas.CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    new_category = models.Category(name = category.name)
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return new_category

# ================ > Get Category < ===================
@router.get("/", response_model=list[schemas.CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    
    return categories

# ================ > Get Category By ID < ==================
@router.get("/{category_id}", response_model = schemas.CategoryResponse)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code= 404,
            detail="Category not found"
        )
    return category

# ================ > Upadte Category < =====================
@router.put("/{category_id}", response_model= schemas.CategoryResponse)
def update_category(category_id: int, category_data: schemas.CategoryCreate ,db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code= 404,
            detail= "Category not found"
        )
        
    category.name = category_data.name
    
    db.commit()
    db.refresh(category)
    
    
    return category

# ================ > Delete Category < ================
@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):

    category = db.query(models.Category).filter(
        models.Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    # Check whether products are linked to this category
    existing_product = db.query(models.Product).filter(
        models.Product.category_id == category_id
    ).first()

    if existing_product:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category because products are associated with it"
        )

    db.delete(category)
    db.commit()

    return {"message": "Category deleted successfully"}