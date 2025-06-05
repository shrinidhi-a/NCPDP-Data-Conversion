from fastapi import FastAPI
from app.router import patients  # Make sure to import the patients router correctly
from app.router import nested_resources  # Import the nested resources router

app = FastAPI()

# Include the router in the main app
app.include_router(patients.router)
app.include_router(nested_resources.router)   # Include the nested resources router
