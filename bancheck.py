import requests
import telebot     

BOT_TOKEN = ''
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

def is_valid_uid(uid):
    return uid.isdigit() and 8 <= len(uid) <= 11

def check_ban_status(uid):
    url = f'https://ff.garena.com/api/antihack/check_banned?lang=en&uid={uid}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'authority': 'ff.garena.com',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'referer': 'https://ff.garena.com/en/support/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'x-requested-with': 'B6FksShzIgjfrYImLpTsadjS86sddhFH',
    }
    resp = requests.get(url, headers=headers)
    data = resp.json().get('data', {})
    period = int(data.get('period', 0))
    if period == 0:
        return f"<b>UID:</b> <code>{uid}</code>\n<b>Status:</b> Not Banned 😎"
    else:
        return f"<b>UID:</b> <code>{uid}</code>\n<b>Status:</b> Permanently Banned 😕"

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "<b>👋 Welcome to Ban check Bot!</b>\n<b>Create by Heart Less</b>\nUse <b>/bancheck &lt;uid&gt;</b> to check ban status.\nExample:\n<code>/bancheck 123456789</code>")

@bot.message_handler(commands=['check'])
def handle_bancheck(message):
    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "<b>Usage:</b> /bancheck &lt;uid&gt;")
        return
    uid = args[1]
    if not is_valid_uid(uid):
        bot.reply_to(message, "<b>Invalid UID!</b>\nUID must be 8 to 11 digits and only numbers.")
        return
    result = check_ban_status(uid)
    bot.reply_to(message, result)

bot.polling()
