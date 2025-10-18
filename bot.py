import telebot
from telebot import types
import os
import time

BOT_TOKEN = os.getenv("8435110689:AAFnCH_-9Px7Dw_FucKrfyBVGVvQb96v11E")
ADMIN_ID = int(os.getenv("ADMIN_ID", "171062109"))  # o‘zingizning Telegram ID

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

PART1 = [
    {"audio": "", "opts": ["الساعة", "إشارة المرور", "الطريق"], "ans": "إشارة المرور"},
    {"audio": "", "opts": ["A2", "B2", "C2"], "ans": "B2"},
    {"audio": "", "opts": ["A", "B", "C"], "ans": "C"},
    {"audio": "", "opts": ["A", "B", "C"], "ans": "B"},
    {"audio": "", "opts": ["A", "B", "C"], "ans": "A"},
    {"audio": "", "opts": ["A", "B", "C"], "ans": "C"},
    {"audio": "", "opts": ["A", "B", "C"], "ans": "B"},
    {"audio": "", "opts": ["A", "B", "C"], "ans": "A"}
]

@bot.message_handler(commands=['start'])
def start(msg):
    cid = msg.chat.id
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🎧 Boshlash", "📊 Natijamni ko‘rish")
    bot.send_message(cid, "Assalomu alaykum! CEFR tinglab tushunish testiga xush kelibsiz.", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "🎧 Boshlash")
def start_part1(msg):
    cid = msg.chat.id
    user_data[cid] = {"i": 0, "answers": []}
    send_question(cid, 0)

def send_question(cid, idx):
    if idx >= len(PART1):
        answers = user_data[cid]["answers"]
        wrongs = []
        for i, a in enumerate(answers):
            if a != PART1[i]["ans"]:
                wrongs.append(str(i+1))
        if not wrongs:
            bot.send_message(cid, "✅ Ajoyib! Barcha javoblar to‘g‘ri!")
        else:
            bot.send_message(cid, "❌ Siz xato qilgan savollar: " + ", ".join(wrongs))
        return

    q = PART1[idx]
    kb = types.InlineKeyboardMarkup()
    for o in q["opts"]:
        kb.add(types.InlineKeyboardButton(o, callback_data="ans|%d|%s" % (idx, o)))
    kb.add(types.InlineKeyboardButton("🔁 Qayta eshitish", callback_data="rep|%d" % idx))

    if q["audio"]:
        bot.send_audio(cid, q["audio"])
        time.sleep(0.5)
        bot.send_audio(cid, q["audio"])

    bot.send_message(cid, "Savol %d / %d. Javobni tanlang:" % (idx+1, len(PART1)), reply_markup=kb)

@bot.callback_query_handler(func=lambda c: True)
def callback(call):
    cid = call.message.chat.id
    parts = call.data.split("|")

    if parts[0] == "rep":
        idx = int(parts[1])
        q = PART1[idx]
        if q["audio"]:
            bot.send_audio(cid, q["audio"])
        else:
            bot.send_message(cid, "Audio hali mavjud emas.")
        bot.answer_callback_query(call.id, "Qayta eshittirildi.")
        return

    if parts[0] == "ans":
        idx = int(parts[1])
        opt = parts[2]
        user_data[cid]["answers"].append(opt)
        bot.answer_callback_query(call.id, "Javob qabul qilindi.")
        send_question(cid, idx + 1)

bot.infinity_polling()
