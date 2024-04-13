from flask import Flask, request
from pyrogram import Client, idle

TOKEN = os.environ.get("TOKEN", "")
API_ID = int(os.environ.get("API_ID", ""))
API_HASH = os.environ.get("API_HASH", "")

bot = Client("Renamer", bot_token=TOKEN, api_id=API_ID, api_hash=API_HASH)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'STthamizhan'

# Webhook route
@app.route('/webhook', methods=['POST'])
def handle_webhook():
    update = request.get_json()
    bot.handle_update(update)
    return 'OK', 200

async def run():
    await bot.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

if __name__ == "__main__":
    asyncio.run(run())
           
