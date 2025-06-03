from fastapi import FastAPI
from api import mtm_routes  # adjust if path is different

app = FastAPI()
app.include_router(mtm_routes.router)

