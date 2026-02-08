from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from config import Config


class Database:
    def __init__(self, uri: str, db_name: str):
        self.client = AsyncIOMotorClient(uri)
        db = self.client[db_name]

        self.users = db.users
        self.welcome_message = db.welcome_message
        self.goodbye_message = db.goodbye_message

    def new_user(self, user_id: int) -> dict:
        """Return a new user document with defaults."""
        return {
            "id": int(user_id),
            "join_date": datetime.utcnow().isoformat()
        }

    async def user_exists(self, user_id: int) -> bool:
        """Check if a user exists in the database."""
        return await self.users.find_one(
            {"id": int(user_id)},
            {"_id": 1}
        ) is not None

    async def add_user(self, user_id: int) -> bool:
        """Add a new user to the database."""
        if await self.user_exists(user_id):
            return False

        await self.users.insert_one(self.new_user(user_id))
        return True

    async def total_users_count(self) -> int:
        """Get the total number of users."""
        return await self.users.count_documents({})
    
    async def get_all_users(self):
        """Get all users from the database."""
        return self.users.find({})

    async def set_welcome_message(self, message: str) -> None:
        """Set the welcome message."""
        await self.welcome_message.update_one(
            {},
            {"$set": {"welcome_message": message}},
            upsert=True
        )

    async def get_welcome_message(self) -> Optional[str]:
        """Get the welcome message."""
        data = await self.welcome_message.find_one({})
        return data.get("welcome_message") if data else None

    async def set_goodbye_message(self, message: str) -> None:
        """Set the goodbye message."""
        await self.goodbye_message.update_one(
            {},
            {"$set": {"goodbye_message": message}},
            upsert=True
        )

    async def get_goodbye_message(self) -> Optional[str]:
        """Get the goodbye message."""
        data = await self.goodbye_message.find_one({})
        return data.get("goodbye_message") if data else None


db = Database(Config.MONGO_DB_URI, Config.DATABASE_NAME)
