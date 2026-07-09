import os, threading, asyncio
from flask import Flask, request
from telegram import Bot

TOKEN = '8974361808:AAGopgWcPlEGHINuJETOWo6nwoxtEfKc_jM'
CHAT_ID = 8710878580
bot = Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot activo'

@app.route('/health')
def health():
    return 'OK'

@app.route('/send', methods=['POST'])
def send():
    text = request.form.get('text', '')
    if text:
        asyncio.run(bot.send_message(chat_id=CHAT_ID, text=text))
        return 'Enviado'
    return 'Falta texto', 400

async def poll():
    offset = 0
    off_file = '/tmp/offset.txt'
    if os.path.exists(off_file):
        offset = int(open(off_file).read())
    while True:
        try:
            updates = await bot.get_updates(offset=offset+1, timeout=30)
            for u in updates:
                offset = u.update_id
                if u.message and u.message.text:
                    name = u.message.from_user.first_name
                    text = u.message.text
                    print(f'[{name}] {text}', flush=True)
            with open(off_file, 'w') as f:
                f.write(str(offset))
            await asyncio.sleep(1)
        except Exception as e:
            print(f'Error: {e}', flush=True)
            await asyncio.sleep(5)

if __name__ == '__main__':
    t = threading.Thread(target=lambda: asyncio.run(poll()), daemon=True)
    t.start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
