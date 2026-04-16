from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

# Import our MongoDB collections
from db.mongodb import jewellery_collection, orders_collection

router = APIRouter()


class OrderItem(BaseModel):
    jewellery_id: str
    name: str
    price: int
    quantity: int = 1


class Order(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone: str
    items: list[OrderItem]
    total: int


@router.get("/products")
async def get_products():
    """Fetch all products directly from MongoDB"""
    products = []
    # Find all documents in the catalogue
    async for doc in jewellery_collection.find({}):
        doc["_id"] = str(doc["_id"])  # Convert MongoDB's internal ObjectId to a normal string
        products.append(doc)
    return products


@router.get("/products/{item_id}")
async def get_product(item_id: str):
    """Fetch a single product by its ID"""
    # Ask MongoDB to find one specific item
    item = await jewellery_collection.find_one({"id": item_id})

    if not item:
        raise HTTPException(404, "Product not found")

    item["_id"] = str(item["_id"])
    return item


@router.post("/orders")
async def place_order(order: Order):
    """Save a new order into the MongoDB orders collection"""
    order_data = order.dict()

    # Count existing orders to generate a unique AURA ID
    order_count = await orders_collection.count_documents({})

    order_data["order_id"] = f"AURA{order_count + 1001}"
    order_data["status"] = "confirmed"
    order_data["timestamp"] = datetime.now().isoformat()

    # Insert the order into the database!
    await orders_collection.insert_one(order_data)

    return {
        "success": True,
        "order_id": order_data["order_id"],
        "message": f"Order confirmed! Your jewellery will arrive in 5-7 days."
    }


@router.get("/orders")
async def get_orders():
    """View all placed orders"""
    orders = []
    async for doc in orders_collection.find({}):
        doc["_id"] = str(doc["_id"])
        orders.append(doc)
    return orders