# Re2ake
AI-based Automated Customer Support for a university project. Implemented as an Telegram Bot + API in Python

# Structure
The app is split into 2 main services: the backend API that handles the database operations and requests to OpenAI, and the Python Bot frontend, used to interact with the end users

# Running
First, run the backend API using
```sh
fastapi run api/main.py
```

Then, run the Telegram Bot using
```sh
python bot/main.py
```