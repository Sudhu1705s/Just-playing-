import time
from pyrogram import Client
from pyrogram import __version__
from pyrogram.raw.all import layer
from config import Config
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
# Suppress verbose logs from pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)


class Bot(Client):
    def __init__(self):
        super().__init__(
            "accept_join_requests_bot",
            api_id=Config.API_ID,  # Replace with your actual API ID
            api_hash=Config.API_HASH,  # Replace with your actual API Hash
            bot_token=Config.BOT_TOKEN,  # Replace with your actual Bot Token
            plugins={"root": "handlers"}

        )
        self.start_time = datetime.now()

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.uptime = time.time()
        logging.info(f"{me.username} Bot started successfully! ✅")

        for id in Config.OWNER_ID:
            try:
                await self.send_message(
                    chat_id=id,
                    text=f"✅ **{me.first_name}** is now online!\n\n"
                          f"🕒 Started at: `{self.start_time.strftime('%d-%m-%Y %I:%M:%S %p')}`\n"
                          f"📚 Version: `Pyrogram v{__version__} | Layer {layer}`"
                )
            except:
                pass

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped. ❌")


if __name__ == "__main__":
    bot = Bot()
    bot.run()
