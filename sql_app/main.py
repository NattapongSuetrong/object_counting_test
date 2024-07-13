from fastapi import Depends, FastAPI, HTTPException # type: ignore
from sqlalchemy.orm import Session # type: ignore
from typing import List
import models
from schemas import UserCreate, UserRead, ShrimpQuantityCreate, ShrimpQuantityRead # type: ignore
from database import SessionLocal, engine # type: ignore

# Create all tables defined in models
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a user
@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(username=user.username, email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Read all users
# @app.get("/users/", response_model=List[UserRead])
# def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     users = db.query(models.User).offset(skip).limit(limit).all()
#     return users

# Read a user by ID
@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update a user
@app.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user.username
    db_user.email = user.email
    db_user.hashed_password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user

# Delete a user
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted"}

# Add shrimp quantity
@app.post("/shrimp_quantities/", response_model=ShrimpQuantityRead)
def create_shrimp_quantity(shrimp_quantity: ShrimpQuantityCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == shrimp_quantity.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_shrimp_quantity = models.ShrimpQuantity(quantity=shrimp_quantity.quantity, user_id=shrimp_quantity.user_id)
    db.add(db_shrimp_quantity)
    db.commit()
    db.refresh(db_shrimp_quantity)
    return db_shrimp_quantity

# Read all shrimp quantities
@app.get("/shrimp_quantities/", response_model=List[ShrimpQuantityRead])
def read_shrimp_quantities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    shrimp_quantities = db.query(models.ShrimpQuantity).offset(skip).limit(limit).all()
    return shrimp_quantities

# Read shrimp quantity by ID
@app.get("/shrimp_quantities/{shrimp_quantity_id}", response_model=ShrimpQuantityRead)
def read_shrimp_quantity(shrimp_quantity_id: int, db: Session = Depends(get_db)):
    shrimp_quantity = db.query(models.ShrimpQuantity).filter(models.ShrimpQuantity.id == shrimp_quantity_id).first()
    if shrimp_quantity is None:
        raise HTTPException(status_code=404, detail="Shrimp quantity not found")
    return shrimp_quantity

# Update shrimp quantity
@app.put("/shrimp_quantities/{shrimp_quantity_id}", response_model=ShrimpQuantityRead)
def update_shrimp_quantity(shrimp_quantity_id: int, shrimp_quantity: ShrimpQuantityCreate, db: Session = Depends(get_db)):
    db_shrimp_quantity = db.query(models.ShrimpQuantity).filter(models.ShrimpQuantity.id == shrimp_quantity_id).first()
    if db_shrimp_quantity is None:
        raise HTTPException(status_code=404, detail="Shrimp quantity not found")
    db_shrimp_quantity.quantity = shrimp_quantity.quantity
    db_shrimp_quantity.user_id = shrimp_quantity.user_id
    db.commit()
    db.refresh(db_shrimp_quantity)
    return db_shrimp_quantity

# Delete shrimp quantity
@app.delete("/shrimp_quantities/{shrimp_quantity_id}")
def delete_shrimp_quantity(shrimp_quantity_id: int, db: Session = Depends(get_db)):
    db_shrimp_quantity = db.query(models.ShrimpQuantity).filter(models.ShrimpQuantity.id == shrimp_quantity_id).first()
    if db_shrimp_quantity is None:
        raise HTTPException(status_code=404, detail="Shrimp quantity not found")
    db.delete(db_shrimp_quantity)
    db.commit()
    return {"detail": "Shrimp quantity deleted"}
