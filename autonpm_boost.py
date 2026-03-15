import os
import requests
import time
import sys
import random
from datetime import datetime, timedelta, timezone

def get_now_wib():
    """Mendapatkan waktu WIB (UTC+7) secara manual"""
    tz_wib = timezone(timedelta(hours=7))
    return datetime.now(tz_wib)

# ==========================================
# 🎯 DYNAMIC CONFIGURATION
# ==========================================
# Nama package NPM lu (otomatis diambil dari GitHub Secrets)
PACKAGE_NAME = os.environ.get("TARGET_PACKAGE", "").strip()

# ==========================================
# 📚 50 TECH & PROGRAMMING QUOTES (SHORT VERSION)
# ==========================================
QUOTES = [
    '"Talk is cheap. Show me the code." – Linus Torvalds',
    '"First, solve the problem. Then, write the code." – John Johnson',
    '"Knowledge is power." – Francis Bacon',
    '"Simplicity is the soul of efficiency." – Austin Freeman',
    '"Automate the boring stuff, master the complex." – Abie Haryatmo',
    '"Empowering the cloud, one automation at a time." – Abie Haryatmo'
]

def send_telegram_notification(message):
    """Kirim pesan ke Telegram dan balikkan ID Pesan untuk editing live"""
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_ids_raw = os.environ.get("TELEGRAM_CHAT_ID")
    if not bot_token or not chat_ids_raw: return {}
    chat_ids = [c.strip() for c in chat_ids_raw.split(",") if c.strip()]
    sent_messages = {}
    for chat_id in chat_ids:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML", "disable_web_page_preview": True}
        try:
            res = requests.post(url, json=payload, timeout=15)
            if res.status_code == 200:
                sent_messages[chat_id] = res.json()['result']['message_id']
        except: pass
    return sent_messages

def edit_telegram_notification(sent_messages, new_message):
    """Edit pesan Telegram yang sudah ada (Live Update)"""
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not bot_token or not sent_messages: return
    for chat_id, msg_id in sent_messages.items():
        url = f"https://api.telegram.org/bot{bot_token}/editMessageText"
        payload = {"chat_id": chat_id, "message_id": msg_id, "text": new_message, "parse_mode": "HTML", "disable_web_page_preview": True}
        try: requests.post(url, json=payload, timeout=15)
        except: pass

def get_latest_version(pkg_name):
    """Mendapatkan versi terbaru dari package NPM"""
    try:
        res = requests.get(f"https://registry.npmjs.org/{pkg_name}", timeout=10)
        if res.status_code == 200:
            return res.json().get("dist-tags", {}).get("latest")
    except: return None
    return None

def boost_downloads(pkg_name, version, sent_msgs):
    """Simulasi download ke NPM Registry"""
    download_url = f"https://registry.npmjs.org/{pkg_name}/-/{pkg_name}-{version}.tgz"
    
    def update_status(status_text):
        msg = (f"╔════════════════════╗\n"
               f"   ⏳ <b>BOOSTING NPM</b>\n"
               f"╚════════════════════╝\n\n"
               f"🔄 <i>{status_text}</i>\n"
               f"══════════════════════\n"
               f"📦 <b>Package  :</b> {pkg_name}\n"
               f"🏷️ <b>Version  :</b> {version}\n\n"
               f"🛡️ <i>Engineered by Abie Haryatmo</i>\n"
               f"🤝 <b>Powered by XianBeeStore</b>")
        edit_telegram_notification(sent_msgs, msg)

    success_count = 0
    # Sesi tembakan wajar agar tidak di-banned NPM
    session_target = random.randint(50, 100)
    
    update_status(f"Starting session ({session_target} hits)...")
    
    for _ in range(session_target):
        try:
            with requests.get(download_url, stream=True, timeout=10) as r:
                if r.status_code == 200:
                    success_count += 1
            time.sleep(random.uniform(0.1, 0.5)) # Delay natural ala manusia
        except: pass
        
    return f"🚀 <b>{success_count} DOWNLOADS SIMULATED</b>"

def main():
    time.sleep(random.randint(1, 10))
    now_wib = get_now_wib()
    time_str = now_wib.strftime('%d/%m/%Y %H:%M:%S WIB')
    
    if not PACKAGE_NAME:
        print("❌ ERROR: TARGET_PACKAGE is empty!")
        sys.exit(1)

    init_msg = (f"╔════════════════════╗\n"
                f" ⏳ <b>INITIALIZING...</b>\n"
                f"╚════════════════════╝\n\n"
                f"<i>Contacting NPM Registry for metadata...</i>\n"
                f"🛡️ <i>Engineered by Abie Haryatmo</i>\n"
                f"🤝 <b>Powered by XianBeeStore</b>")
    sent_msgs = send_telegram_notification(init_msg)

    version = get_latest_version(PACKAGE_NAME)
    if not version:
        final_msg = "❌ <b>FAILED</b>\nPackage not found on NPM!"
        edit_telegram_notification(sent_msgs, final_msg)
        sys.exit(1)

    result_text = boost_downloads(PACKAGE_NAME, version, sent_msgs)

    selected_quote = random.choice(QUOTES)
    final_msg = (
        f"╔════════════════════╗\n"
        f" ✅ <b>SESSION COMPLETED</b>\n"
        f"╚════════════════════╝\n\n"
        f"{result_text}\n"
        f"══════════════════════\n"
        f"📦 <b>Package  :</b> {PACKAGE_NAME}\n"
        f"⏱️ <b>Time     :</b> {time_str}\n\n"
        f"#NPMBoost #OSSGrowth\n"
        f"💯 <i>Crafted by Abie Haryatmo</i>\n"
        f"🤝 <b>Powered by XianBeeStore</b>\n"
        f"<i>{selected_quote}</i>"
    )
    edit_telegram_notification(sent_msgs, final_msg)

if __name__ == "__main__":
    main()
