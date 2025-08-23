import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import AudioPiped
import yt_dlp

# === ENV Variables ===
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = int(os.getenv("GROUP_CHAT_ID"))

# === Pyrogram Client ===
app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
pytgcalls = PyTgCalls(app)

# === Flask for Uptime Robot ===
from flask import Flask
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Music Bot is running ✅", 200

# === Helper: download audio from YouTube ===
async def download_audio(url: str) -> str:
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'noplaylist': True,
    }
    os.makedirs("downloads", exist_ok=True)
    loop = asyncio.get_event_loop()
    info = await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=True))
    return ydl_opts['outtmpl'].replace("%(title)s.%(ext)s", f"{info['title']}.{info['ext']}")

# === /play Command ===
@app.on_message(filters.command("play") & filters.chat(GROUP_CHAT_ID))
async def play(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("⚠️ Usage: /play <YouTube URL>")
        return

    query = " ".join(message.command[1:])
    msg = await message.reply_text("🔎 Searching & downloading...")
    
    try:
        file_path = await download_audio(query)
        await message.reply_text(f"✅ Downloaded: {os.path.basename(file_path)}\nJoining VC...")

        # Join VC & play using AudioPiped (old stable style)
        await pytgcalls.join_group_call(
            GROUP_CHAT_ID,
            AudioPiped(file_path)
        )
        await message.reply_text("▶️ Playing now!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

# === /pause Command ===
@app.on_message(filters.command("pause") & filters.chat(GROUP_CHAT_ID))
async def pause(client: Client, message: Message):
    try:
        await pytgcalls.pause_stream(GROUP_CHAT_ID)
        await message.reply_text("⏸ Paused!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

# === /resume Command ===
@app.on_message(filters.command("resume") & filters.chat(GROUP_CHAT_ID))
async def resume(client: Client, message: Message):
    try:
        await pytgcalls.resume_stream(GROUP_CHAT_ID)
        await message.reply_text("▶️ Resumed!")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

# === Main ===
async def main():
    await app.start()
    await pytgcalls.start()
    print("🎵 Music Bot running...")
    
    import threading
    threading.Thread(target=lambda: flask_app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000))), daemon=True).start()

    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())