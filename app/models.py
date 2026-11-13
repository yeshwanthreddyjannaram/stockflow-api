from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

# ============= > Category Table < ================
class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key= True, index= True)
    name = Column(String, unique= True, nullable= False)
    products= relationship("Product", back_populates="category")
    

# ================ > Products Table < =================
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key= True, index= True)
    name = Column(String, nullable= False)
    price = Column(Float, nullable= False)
    stock_quantity = Column(Integer, nullable= False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable= False)
    
    category = relationship("Category", back_populates= "products")
    order_items = relationship("OrderItem", back_populates= "product", passive_deletes=True)
    

# =============== > Order Table < ===================
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index= True)
    customer_name = Column(String, nullable= False)
    total_amount = Column(Float, nullable= False, default= 0)
    status = Column(String, nullable= False, default = "pending")
    
    items = relationship("OrderItem", back_populates= "order")
    

# ================ > Order Item Table < =================
class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key= True, index= True)
    
    order_id = Column(Integer, ForeignKey("orders.id"), nullable= False)
    
    product_id = Column(Integer,ForeignKey("products.id"), nullable= False)
    
    quantity = Column(Integer, nullable= False)
    
    price = Column(Float, nullable=False)
    
    order = relationship("Order", back_populates= "items")
    product = relationship("Product", back_populates= "order_items")
    
    