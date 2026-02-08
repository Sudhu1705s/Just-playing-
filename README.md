# Auto Request Acceptor Bot

A Telegram bot built with Python and Pyrofork (Pyrogram) that automatically accepts join requests in your Telegram channels and groups.

## 🚀 Features

- **Auto Accept Requests**: Automatically accepts pending join requests.
- **Welcome Messages**: Support for custom welcome messages (configurable via database).
- **Admin Logs**: Logs new user activities to a configured log channel.
- **MongoDB Support**: Uses MongoDB for storing user data and configurations.

## 🛠 Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- A MongoDB database (local or cloud, e.g., MongoDB Atlas)
- Telegram API ID and API Hash (get them from [my.telegram.org](https://my.telegram.org))
- A Telegram Bot Token (get it from [@BotFather](https://t.me/BotFather))

## 📥 Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. Create a `.env` file in the root directory of the project.
2. Add the following configuration variables to the `.env` file:

   ```env
   API_ID=your_api_id
   API_HASH=your_api_hash
   BOT_TOKEN=your_bot_token
   MONGO_DB_URI=your_mongodb_connection_string
   DATABASE_NAME=Cluster0
   OWNER_ID=123456789 987654321  # Space-separated user IDs
   LOG_CHANNEL=-1001234567890   # Channel ID for logs
   ```

   **Variable Details:**

   - `API_ID` & `API_HASH`: Your Telegram API credentials.
   - `BOT_TOKEN`: The token provided by BotFather.
   - `MONGO_DB_URI`: Your MongoDB connection string.
   - `DATABASE_NAME`: Name of your database (default: Cluster0).
   - `OWNER_ID`: ID(s) of the bot owner(s).
   - `LOG_CHANNEL`: ID of the channel where logs will be sent.

## ▶️ Usage

To start the bot, run the following command:

```bash
python main.py
```

The bot will start and print a success message in the console. It will also notify the owner(s) in Telegram.

## 📂 Project Structure

```
.
├── config.py           # Configuration loader
├── Dockerfile          # Docker configuration
├── main.py             # Entry point of the bot
├── requirements.txt    # Python dependencies
├── handlers/           # Bot event handlers
│   ├── callbacks.py
│   ├── commands.py
│   └── listen_join_req.py
└── utility/            # Helper functions and database
    ├── database.py
    └── helper.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open-source.
