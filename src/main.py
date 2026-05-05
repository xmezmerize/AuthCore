from fastapi import FastAPI
from dotenv import load_dotenv

from entrypoints.routes import user_routes

import framework.container

load_dotenv()

app = FastAPI(
    title="AuthCore",
    version="0.2.0",
    description="Under construction..."
)

app.include_router(user_routes.route)
