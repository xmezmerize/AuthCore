from entrypoints.routes import user_routes
from dotenv import load_dotenv
from fastapi import FastAPI
import framework.container


load_dotenv()

app = FastAPI(
    title="AuthCore",
    version="0.2.1",
    description="Under construction..."
)

app.include_router(user_routes.route)
