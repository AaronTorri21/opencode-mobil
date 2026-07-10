import os, asyncio
from flask import Flask, request
from telegram import Bot

TOKEN = '8974361808:AAGopgWcPlEGHINuJETOWo6nwoxtEfKc_jM'
bot = Bot(token=TOKEN)
app = Flask(__name__)

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
            asyncio.run(bot.send_message(chat_id=chat_id, text=f'Dijiste: {text}'))
            print(f'[ECO] Respuesta enviada a {chat_id}', flush=True)
    except Exception as e:
        print(f'Error webhook: {e}', flush=True)
    return 'OK', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)