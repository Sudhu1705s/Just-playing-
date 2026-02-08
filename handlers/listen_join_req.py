from pyrogram import Client, filters
from utility.database import db
from pyrogram.errors import FloodWait
import asyncio
import logging

logger = logging.getLogger(__name__)

@Client.on_chat_join_request()
async def handle_join_request(client:Client, join_request):
    user = join_request.from_user
    chat = join_request.chat
    try:
        await client.approve_chat_join_request(chat.id, user.id)
        logger.info(f"Approved join request for user {user.id} to chat {chat.id}")
    except FloodWait as e:
        logger.warning(f"Flood wait error: waiting for {e.x} seconds")
        await asyncio.sleep(e.value)
        await client.approve_chat_join_request(chat.id, user.id)
        logger.info(f"Approved join request for user {user.id} to chat {chat.id}")

    # Optionally, send a welcome message to the user
    welcome_message = await db.get_welcome_message()

    if welcome_message:
        try:
            await client.send_message(
                user.id,
                welcome_message.format(mention=user.mention, chat=chat.title)
            )
        except Exception as e:
            logger.error(f"Failed to send welcome message to user {user.id}: {e}")
            
@Client.on_message((filters.channel | filters.group) & filters.left_chat_member)
async def handle_left_member(client:Client, message):
    user = message.left_chat_member
    chat = message.chat

    logger.info(f"User {user.id} has left the chat {chat.id}")

    # Optionally, send a goodbye message to the chat
    goodbye_message = await db.get_goodbye_message()

    if goodbye_message:
        try:
            await client.send_message(
                user.id,
                goodbye_message.format(mention=user.mention, chat=chat.title)
            )
        except Exception as e:
            logger.error(f"Failed to send goodbye message to user {user.id}: {e}")