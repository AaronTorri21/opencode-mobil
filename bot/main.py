import os, json, urllib.request, asyncio
from flask import Flask, request
from telegram import Bot

TOKEN = '8974361808:AAGopgWcPlEGHINuJETOWo6nwoxtEfKc_jM'
bot = Bot(token=TOKEN)
app = Flask(__name__)
OPENAI_KEY = os.environ.get('OPENAI_KEY', '')

def preguntar_openai(texto):
    url = 'https://api.openai.com/v1/chat/completions'
    data = json.dumps({
        'model': 'gpt-4o-mini',
        'messages': [{'role': 'user', 'content': texto}]
    }).encode()
    req = urllib.request.Request(url, data=data, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_KEY}'
    })
    r = urllib.request.urlopen(req, timeout=30)
    resp = json.loads(r.read())
    return resp['choices'][0]['message']['content']

@app.route('/')
def home():
    return 'Bot activo'

@app.route('/health')
def health():
    return 'OK'

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = request.get_json()
        if update and 'message' in update and 'text' in update['message']:
            text = update['message']['text']
            chat_id = update['message']['chat']['id']
            name = update['message']['from']['first_name']
            print(f'[{name}] {text}', flush=True)
            resp = preguntar_openai(text)
            asyncio.run(bot.send_message(chat_id=chat_id, text=resp))
            print(f'[GPT] Respuesta enviada a {chat_id}', flush=True)
    except Exception as e:
        asyncio.run(bot.send_message(chat_id=chat_id if 'chat_id' in dir() else 8710878580, text=f'Error: {e}'))
        print(f'Error webhook: {e}', flush=True)
    return 'OK', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)