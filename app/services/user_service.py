import logging
from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate
from app.utilities.create_utility import schema_to_dict
from app.utilities.password_utility import hash_password  # ensure this exists

logger = logging.getLogger(__name__)

async def create_user(db: AsyncSession, user: UserCreate) -> User:
    """
    Create a new user; hashes password, commits, refreshes, returns instance.
    Raises IntegrityError upward for router to translate, or re-raises other DB errors.
    """
    data = schema_to_dict(user)
    # Ensure password is hashed here (centralized)
    data["password"] = hash_password(data["password"])

    new_user = User(**data)

    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        logger.info("User created: email=%s id=%s", new_user.email, new_user.id)
        return new_user
    except IntegrityError:
        await db.rollback()
        logger.warning("Integrity error creating user: email=%s", data.get("email"))
        raise
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error("Database error creating user: %s", str(e))
        raise
    except Exception as e:
        await db.rollback()
        logger.exception("Unexpected error creating user")
        raise


async def get_users(db: AsyncSession) -> List[User]:
    """
    Return all users.
    """
    try:
        result = await db.execute(select(User))
        users = result.scalars().all()
        logger.debug("Fetched %d users", len(users))
        return users
    except SQLAlchemyError as e:
        logger.error("Database error fetching users: %s", str(e))
        raise
    except Exception:
        logger.exception("Unexpected error fetching users")
        raise