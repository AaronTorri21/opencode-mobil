import os, threading, asyncio, json, urllib.request
from flask import Flask, request
from telegram import Bot

TOKEN = '8974361808:AAGopgWcPlEGHINuJETOWo6nwoxtEfKc_jM'
CHAT_ID = 8710878580
GROQ_KEY = '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'
bot = Bot(token=TOKEN)
app = Flask(__name__)

def preguntar_groq(texto):
    url = 'https://api.groq.com/openai/v1/chat/completions'
    data = json.dumps({
        'model': 'llama-3.3-70b-versatile',
        'messages': [{'role': 'user', 'content': texto}]
    }).encode()
    try:
        req = urllib.request.Request(url, data=data, headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {GROQ_KEY}'
        })
        r = urllib.request.urlopen(req, timeout=30)
        resp = json.loads(r.read())
        return resp['choices'][0]['message']['content']
    except Exception as e:
        return f'Error: {e}'



