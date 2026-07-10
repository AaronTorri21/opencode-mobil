import os, json, urllib.request, time
from flask import Flask, request

TOKEN = '8974361808:AAGopgWcPlEGHINuJETOWo6nwoxtEfKc_jM'
OPENAI_KEY = os.environ.get('OPENAI_KEY', '')
app = Flask(__name__)

def send_telegram(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = json.dumps({'chat_id': chat_id, 'text': text}).encode()
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req, timeout=15)

def preguntar_openai(texto):
    for intento in range(5):
        try:
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
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(10)
            else:
                raise
    return 'Error: Límite de velocidad. Espera un momento y vuelve a intentar.'

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
            send_telegram(chat_id, resp)
            print(f'[GPT] Respuesta enviada a {chat_id}', flush=True)
    except Exception as e:
        try:
            chat_id = update['message']['chat']['id']
        except:
            chat_id = 8710878580
        send_telegram(chat_id, f'Error: {e}')
        print(f'Error webhook: {e}', flush=True)
    return 'OK', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)