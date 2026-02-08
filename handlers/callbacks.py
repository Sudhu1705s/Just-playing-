from pyrogram import Client, filters
from utility.database import db
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex(r"^help"))
async def help_callback_handler(client: Client, callback_query: CallbackQuery):
    help_text = (
        "This bot automatically accepts all join requests in groups or channels where it is an admin with 'Invite via link' permission.\n\n"
        "To use the bot:\n"
        "1. Add the bot to your group or channel as an admin.\n"
        "2. Ensure it has the 'Invite via link' permission.\n"
        "3. The bot will start accepting join requests automatically."
    )

    back_button = InlineKeyboardMarkup([[InlineKeyboardButton("SetWelcome-Message", callback_data="set_welcome"), InlineKeyboardButton("SetGoodbye-Message", callback_data="set_goodbye")],
                                        [InlineKeyboardButton("Close", callback_data="close")]])

    await callback_query.message.edit_text(
        text=help_text,
        reply_markup=back_button
    )


@Client.on_callback_query(filters.regex(r"^set_welcome"))
async def set_welcome_callback_handler(client: Client, callback_query: CallbackQuery):
    await callback_query.message.delete()
    read_msg = await client.ask(chat_id=callback_query.from_user.id,
                                text="**Please forward the welcome message you want to set. You can use placeholders like**\n\n> **{mention} for the user's name.**\n**{chat} for the chat name.**\n\n> **Use /cancel to abort.**", filters=filters.text,)
    if read_msg.text == "/cancel":
        await callback_query.message.reply_text(text="> **Operation cancelled.**",)
        return
    
    await db.set_welcome_message(read_msg.text)
    await callback_query.message.reply_text(text="> **Welcome message has been set successfully!**",)


@Client.on_callback_query(filters.regex(r"^set_goodbye"))
async def set_goodbye_callback_handler(client: Client, callback_query: CallbackQuery):
    await callback_query.message.delete()
    read_msg = await client.ask(chat_id=callback_query.from_user.id,
                                text="**Please forward the goodbye message you want to set. You can use placeholders like**\n\n> **{mention} for the user's name.**\n**{chat} for the chat name.**\n\n> **Use /cancel to abort.**", filters=filters.text,)

    if read_msg.text == "/cancel":
        await callback_query.message.reply_text(text="> **Operation cancelled.**",)
        return
    
    await db.set_goodbye_message(read_msg.text)
    await callback_query.message.reply_text(text="> **Goodbye message has been set successfully!**",)

@Client.on_callback_query(filters.regex(r"^close"))
async def close_callback_handler(client: Client, callback_query: CallbackQuery):
    await callback_query.message.delete()
