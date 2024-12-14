from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import aiohttp
from PIL import Image
from io import BytesIO
import random
import config

# Client setup
app = Client(
    "seize", 
    api_id=config.API_ID, 
    api_hash=config.API_HASH, 
    bot_token=config.BOT_TOKEN
)

# MongoDB connection
# Client 1 collection DB URL
Client_1 = AsyncIOMotorClient(config.MONGO_DB_URI)
db_1 = Client_1['seize_collection']

# Client 2 coin update DB URL
Client_2 = AsyncIOMotorClient(config.MONGO_DB_UPDATE_URI)
db_2 = Client_2['Charector_catcher']

user_collection = db_2["user_collection_lmaoooo"]
collection = db_1["charectors"]


# Upload handler
@app.on_message(filters.command("upload"))
async def upload(client, message: Message):
    if message.chat.id != config.UPLOAD_CHAT_ID or message.from_user.id not in config.SUDOERS:
        await message.reply("You are not authorized to use this command.")
        return
    try:
        parts = message.text.split(" ", 2)
        if len(parts) != 3:
            await message.reply("Invalid format. Use /upload <character link> <character name>")
            return

        character_link, character_name = parts[1], parts[2]

        async with aiohttp.ClientSession() as session:
            async with session.get(character_link) as response:
                if response.status != 200:
                    await message.reply("Invalid link! Please check the link and try again.")
                    return
                image_data = await response.read()
                image = Image.open(BytesIO(image_data))
                buffer = BytesIO()
                image.save(buffer, format="JPEG")
                buffer.seek(0)

                photo = await app.send_photo(chat_id=config.LOGGER_ID, photo=buffer)
                photo_id = photo.photo[-1].file_id
                await collection.insert_one({"charectors": photo_id, "character_name": character_name})
                await message.reply("Character uploaded successfully!")
    except Exception as e:
        await message.reply(f"Error occurred: {e}")


# Guess handler
@app.on_message(filters.command("nguess"))
async def nguess(client, message: Message):
    if message.chat.id != config.CHAT_ID:
        return
    try:
        characters = await collection.find().to_list(length=100000)
        if not characters:
            await message.reply("No characters available. Please upload some first.")
            return

        random_character = random.choice(characters)
        photo_id = random_character["charectors"]
        character_name = random_character["character_name"]

        await app.send_photo(chat_id=config.CHAT_ID, photo=photo_id, caption="Guess the character!")
        start_time = asyncio.get_event_loop().time()
        while True:
            if asyncio.get_event_loop().time() - start_time >= 20:
                await message.reply(f"Time's up! The character was {character_name}")
                break
            await asyncio.sleep(1)
    except Exception as e:
        await message.reply(f"Error occurred: {e}")


# Name check handler
@app.on_message(filters.command("name"))
async def name_check(client, message: Message):
    try:
        user_guess = message.text.split(" ", 1)[1].strip().lower()
        characters = await collection.find().to_list(length=100000)
        for character in characters:
            if character["character_name"].lower() == user_guess:
                user_id = message.from_user.id
                user_data = await user_collection.find_one({"id": user_id})
                if user_data:
                    user_data["Balance"] += 50
                    user_data["streak"] += 1

                    # Bonus rewards for streaks
                    if user_data["streak"] == 30:
                        user_data["Balance"] += 3000
                        await message.reply("🎉 30-streak! Earned 3000 bitcoins! 🎉")
                    elif user_data["streak"] == 50:
                        user_data["Balance"] += 4000
                        await message.reply("🎉 50-streak! Earned 4000 bitcoins! 🎉")
                    elif user_data["streak"] == 100:
                        user_data["Balance"] += 5000
                        await message.reply("🎉 100-streak! Earned 5000 bitcoins! 🎉")

                    await user_collection.update_one({"id": user_id}, {"$set": user_data})
                else:
                    await user_collection.insert_one({"id": user_id, "Balance": 50, "streak": 1})

                await message.reply("🎉 Correct! You've earned 50 bitcoins! 🎉")
                return

        await message.reply("Sorry, incorrect guess!")
    except Exception as e:
        await message.reply(f"Error occurred: {e}")


# Start handler
@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply("Welcome to the Seize game! Use /help to see available commands.")


# Help handler
@app.on_message(filters.command("help"))
async def help(client, message: Message):
    await message.reply(
        "You can use the following commands:\n"
        "/start - Start the game\n"
        "/help - Show this message\n"
        "/upload - Upload a character\n"
        "/nguess - Play the guessing game\n"
        "/name - Check if a character name is correct"
    )


if __name__ == "__main__":
    app.run()