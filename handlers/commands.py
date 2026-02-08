import sys
from pyrogram import Client,filters
from utility.helper import new_user_log
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utility.database import db
from config import Config
import time
from utility.helper import send_msg
import datetime
import os



@Client.on_message(filters.command("start") & filters.private)
async def start_command_handler(client: Client, message: Message):
    IMG_URL = "https://i.ibb.co/BHqqT4Ws/photo-2025-12-14-18-31-43-7583788732830974036.jpg"
    ms = await message.reply_text("> **Processing...**")
    await new_user_log(client, message.from_user)
    is_admin = message.from_user.id in Config.OWNER_ID
    help_button = InlineKeyboardMarkup([[InlineKeyboardButton("Help", callback_data="help")]])
    await message.reply_photo(
        photo=IMG_URL,
        caption=f"Hello {message.from_user.mention},\n\nI'm auto request acceptor bot. I can accept all your join request automatically in any chat.\n\nJust add me to your group or channel as admin with 'Invite via link' permission",
        reply_markup=help_button if is_admin else None
    )
    await ms.delete()

@Client.on_message(filters.private & filters.command("reboot") & filters.user(Config.OWNER_ID))
async def reboot_command_handler(client: Client, message: Message):
    await message.reply_text("> **Rebooting...**")
    os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_message(filters.private & filters.command("status") & filters.user(Config.OWNER_ID))
async def status_command_handler(client: Client, message: Message):
    """Get bot statistics"""
    total_users = await db.total_users_count()
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - client.uptime))

    start_t = time.time()
    status_msg = await message.reply("> **📊 Fetching statistics...**")
    end_t = time.time()

    ping = (end_t - start_t) * 1000

    await status_msg.edit(
        text=(
            "**📈 Bot Status**\n\n"
            f"> **⌚️ Uptime:** `{uptime}`\n"
            f"> **🚀 Current Ping:** `{ping:.2f} ms`\n"
            f"> **👥 Total Users:** `{total_users}`"
        )
    )


@Client.on_message(filters.private & filters.command('broadcast') & filters.reply & filters.user(Config.OWNER_ID))
async def broadcast(bot: Client, message: Message):
    """Broadcast a message to all users"""

    # Log the broadcast initiation
    await bot.send_message(
        Config.LOG_CHANNEL,
        f"**📣 Broadcast initiated by {message.from_user.mention} (`{message.from_user.id}`)**"
    )
    # Get message to broadcast
    broadcast_msg = message.reply_to_message
    all_users = await db.get_all_users()
    total_users = await db.total_users_count()

    # Initialize status message
    status_msg = await message.reply_text("> **📣 Broadcast started...**")

    # Initialize counters
    done = 0
    success = 0
    failed = 0
    start_time = time.time()

    # Process broadcast
    async for user in all_users:
        status = await send_msg(user['id'], broadcast_msg)

        if status == 200:
            success += 1
        else:
            failed += 1

        if status == 400:
            await db.delete_user(user['id'])

        done += 1

        # Update status every 20 messages
        if not done % 20:
            await status_msg.edit(
                f"> **📤 Broadcast In Progress**\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"> **👥 Total Users:** `{total_users}`\n"
                f"> **✅ Completed:** `{done} / {total_users}`\n"
                f"> **🎯 Success:** `{success}`\n"
                f"> **⚠️ Failed:** `{failed}`\n"
                f"━━━━━━━━━━━━━━━━━━━━"
            )

    # Calculate completion time
    completion_time = datetime.timedelta(
        seconds=int(time.time() - start_time))

    # Send final status
    await status_msg.edit(
        f"> **✅ Broadcast Completed**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"> **⏱️ Time Taken:** `{completion_time}`\n"
        f"> **👥 Total Users:** `{total_users}`\n"
        f"> **📨 Delivered:** `{success}`\n"
        f"> **⚠️ Failed:** `{failed}`\n"
        f"> **📊 Processed:** `{done} / {total_users}`\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )