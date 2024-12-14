import re
from os import getenv

# API credentials
API_ID = int(getenv("API_ID", 24089031))  # Default value provided as 24089031
API_HASH = getenv("API_HASH", "0615e3afe13ddaaf8e9ddbd3977d35ff")

# Bot token
BOT_TOKEN = getenv("BOT_TOKEN", "7771917183:AAH-AEqm3VJa1S5BChBNdWivCC0LVlGAoLk")

# Owner and Sudoers
OWNER_ID = int(getenv("OWNER_ID", 6806897901))  # Default OWNER_ID
SUDOERS = list(
    map(int, getenv("SUDOERS", "5743956401,6368715469,6806897901,6777860063").split(","))
)  # Convert to a list of integers

# Chat-related IDs
CHAT_ID = list(map(int, getenv("CHAT_ID", "-1002374835450,-1002274287324").split(",")))
UPLOAD_CHAT_ID = int(getenv("UPLOAD_CHAT_ID", -1002339161004))
LOGGER_ID = int(getenv("LOGGER_ID", -1002342285813))

# MongoDB URIs
MONGO_DB_URI = getenv(
    "MONGO_DB_URI",
    "mongodb+srv://shivaiaxz:YfVBSatihAQlPAXc@cluster0.rqcpm.mongodb.net/?retryWrites=true&w=majority",
)
MONGO_DB_UPDATE_URI = getenv(
    "MONGO_DB_UPDATE_URI",
    "mongodb+srv://shivaiaxz:YfVBSatihAQlPAXc@cluster0.rqcpm.mongodb.net/?retryWrites=true&w=majority",
)