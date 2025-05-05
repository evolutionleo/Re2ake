# Re2ake
AI-based Automated Customer Support for a university project. Implemented as an Telegram Bot + API in Python

# Structure
The app is split into 2 main services: the backend API that handles the database operations and requests to OpenAI, and the Python Bot frontend, used to interact with the end users

# Running
You'll need a .env file in the root of the project with your OpenAI API key, and a Telegram Bot Token
```
OPENAI_API_KEY=...
TELEGRAM_BOT_TOKEN=...
```

First, run the backend API using
```sh
fastapi run api/main.py
```

Then, run the Telegram Bot using
```sh
python bot/main.py
```