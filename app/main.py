from typing import Union

from fastapi import FastAPI
from app.routers import user
from app.routers import task

# Add these imports at the top
import asyncio
from pathlib import Path
from alembic.config import Config
from alembic import command
from app.core.config import DATABASE_URL

from contextlib import asynccontextmanager

# Add this function
async def _run_alembic_upgrade_head() -> None:
    project_root = Path(__file__).resolve().parents[1]
    cfg = Config(str(project_root / "alembic.ini"))
    # Ensure script_location and URL are set
    cfg.set_main_option("script_location", str(project_root / "alembic"))
    cfg.set_main_option("sqlalchemy.url", DATABASE_URL)
    # Run in a thread to avoid blocking the event loop
    await asyncio.to_thread(command.upgrade, cfg, "head")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Idempotent: upgrade head does nothing if already at head
    await _run_alembic_upgrade_head()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(user.router)
app.include_router(task.router)
