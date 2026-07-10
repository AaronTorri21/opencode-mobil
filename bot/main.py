import os, threading, asyncio, json, urllib.request
from flask import Flask, request
from telegram import Bot

TOKEN = '8974361808:AAGopgWcPlEGHINuJETOWo6nwoxtEfKc_jM'
CHAT_ID = 8710878580
OPENAI_KEY = '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'
bot = Bot(token=TOKEN)
app = Flask(__name__)

def preguntar_openai(texto):
    url = 'https://api.openai.com/v1/chat/completions'
    data = json.dumps({
        'model': 'gpt-4o-mini',
        'messages': [{'role': 'user', 'content': texto}]
    }).encode()
    try:
        req = urllib.request.Request(url, data=data, headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENAI_KEY}'
        })
        r = urllib.request.urlopen(req, timeout=30)
        resp = json.loads(r.read())
        return resp['choices'][0]['message']['content']
    except Exception as e:
        return f'Error: {e}'

@app.route('/')
def home():
    return 'Bot activo'

@app.route('/health')
def health():
    return 'OK'

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
                    text = u.message.text
                    name = u.message.from_user.first_name
                    print(f'[{name}] {text}', flush=True)
                    resp = preguntar_openai(text)
                    await bot.send_message(chat_id=CHAT_ID, text=resp)
                    print(f'[GPT] Respuesta enviada', flush=True)
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
