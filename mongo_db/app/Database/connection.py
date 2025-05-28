import motor.motor_asyncio
from bson.errors import InvalidId
from bson import ObjectId

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client.healthcare
patients_collection = db.patients_data