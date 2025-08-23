# Telegram VC Music Bot 🎵

Ye bot aapke Telegram group ke voice chat me songs play karne ke liye bana hai.  
Bot commands: `/play <YouTube URL>` aur `/pause` (optional `/resume` bhi included).  

---

## Features

- Play songs in Telegram Group Voice Chat
- Pause & Resume playback
- Flask health check for uptime monitoring (UptimeRobot friendly)
- Minimal dependencies, easy deploy on Render/Heroku

---

## Requirements

- Python 3.10+
- Environment variables:

API_ID=123456 API_HASH=abcdef1234567890 BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11 GROUP_CHAT_ID=-1001234567890 PORT=5000

- Install dependencies:
```bash
pip install -r requirements.txt


---

Deployment (Render)

1. Create a new Web Service on Render


2. Connect your GitHub repo with this bot


3. Set environment variables (API_ID, API_HASH, BOT_TOKEN, GROUP_CHAT_ID, PORT)


4. Start command:

python music_bot.py


5. Use UptimeRobot to ping your Render URL every 5–10 mins:

https://<your-render-url>/




---

Commands

Command	Description

/play <URL>	Download & play song in VC
/pause	Pause current song
/resume	Resume playback



---

Folder Structure

.
├── music_bot.py
├── requirements.txt
├── downloads/        # Automatically created for downloaded songs
└── README.md


---

Made with ❤️ by Harshit