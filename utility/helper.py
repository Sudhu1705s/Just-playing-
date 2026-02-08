import asyncio
from pyrogram import Client
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from pytz import timezone
from datetime import datetime
from config import Config
from .database import db
import logging

logger = logging.getLogger(__name__)


async def new_user_log(client: Client, user) -> None:
    """Adds a user to the database."""

    success = await db.add_user(user.id)
    curr = datetime.now(timezone("Asia/Kolkata"))
    date = curr.strftime("%d %B, %Y")
    time_str = curr.strftime("%I:%M:%S %p")

    log_message = (
        "<b>📥 <u>New User Started the Client</u></b>\n\n"
        f"> ➲ <b>User ID:</b> <code>{user.id}</code>\n"
        f"> ➲ <b>First Name:</b> {user.first_name}\n"
        f"> ➲ <b>Last Name:</b> {user.last_name or 'None'}\n"
        f"> ➲ <b>Username:</b> @{user.username or 'None'}\n"
        f"> ➲ <b>Mention:</b> {user.mention}\n"
        f"> ➲ <b>Direct Link:</b> <a href='tg://openmessage?user_id={user.id}'>Click Here</a>\n\n"
        f"🗓️ <b>Date:</b> <b>{date}</b>\n"
        f"⏰ <b>Time:</b> <b>{time_str}</b>\n\n"
        f"👨‍💻 <b>Handled by:</b> <b>{client.mention}</b>"
    )

    if success:
        await client.send_message(
            chat_id=Config.LOG_CHANNEL,
            text=log_message
        )


async def send_msg(user_id: int, message):
    """Send message with proper error handling"""
    try:
        await message.forward(chat_id=user_id)
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_msg(user_id, message)
    except (InputUserDeactivated, UserIsBlocked, PeerIdInvalid) as e:
        logger.info(f"{user_id}: {e.__class__.__name__}")
        return 400
    except Exception as e:
        logger.error(f"{user_id}: {e}")
        return 500