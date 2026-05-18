from entrypoints.routes import refresh_token_routes, user_routes
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi import FastAPI
import framework.container

load_dotenv()

app = FastAPI(
    title="AuthCore",
    version="0.1.2",
    description="Under construction..."
)

origins: list[str] = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.route)
app.include_router(refresh_token_routes.route)
