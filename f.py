from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "BOT_TOKEN"
CHANNEL = "@deutschlernenuzbek"
ADMIN_ID = 123456789  # o'z telegram id

state = {}

main_keyboard = ReplyKeyboardMarkup(
    [["📢 Reklama"]],
    resize_keyboard=True
)

admin_keyboard = ReplyKeyboardMarkup(
[
["➕ Tugma qo‘shish","✏️ Matn o‘zgartirish"],
["📊 Statistika","❌ Panel yopish"]
],
resize_keyboard=True
)

type_keyboard = ReplyKeyboardMarkup(
[
["🗣 Sprechen","🎧 Hören"],
["📖 Lesen","✍ Schreiben"],
["🧠 Test","🎙 Jonli efir"]
],
resize_keyboard=True
)

ads = {
"🗣 Sprechen":"🇩🇪 Nemis tilida gapirishni o‘rganmoqchimisiz? Bu kanal orqali sprechen mashqlari bilan nutqingizni rivojlantiring.\n\n👉 {}",

"🎧 Hören":"🇩🇪 Nemis tilida eshitib tushunishni rivojlantiring. Audio materiallar va hören mashqlari shu yerda.\n\n👉 {}",

"📖 Lesen":"🇩🇪 Nemis tilida o‘qish ko‘nikmasini rivojlantirish uchun lesen mashqlari va matnlar.\n\n👉 {}",

"✍ Schreiben":"🇩🇪 Nemis tilida yozishni rivojlantirish uchun schreiben mashqlari.\n\n👉 {}",

"🧠 Test":"🇩🇪 Nemis tilini tekshirib ko‘rish uchun testlar.\n\n👉 {}",

"🎙 Jonli efir":"🇩🇪 Nemis tili bo‘yicha jonli efir va darslar.\n\n👉 {}"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bot ishlayapti",
        reply_markup=main_keyboard
    )

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.id == ADMIN_ID:
        await update.message.reply_text(
            "Admin panel",
            reply_markup=admin_keyboard
        )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat = update.message.chat_id
    text = update.message.text

    if text == "📢 Reklama":
        state[chat] = "link"
        await update.message.reply_text("Reklama uchun link yuboring")
        return

    if chat in state and state[chat] == "link":
        state[chat] = text
        await update.message.reply_text(
            "Reklama turini tanlang",
            reply_markup=type_keyboard
        )
        return

    if chat in state:

        link = state[chat]

        if text in ads:

            msg = ads[text].format(link)

            await context.bot.send_message(CHANNEL,msg)

            await update.message.reply_text("Reklama kanalga yuborildi ✅")

            del state[chat]

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.id == ADMIN_ID:
        users = len(state)
        await update.message.reply_text(f"Faol foydalanuvchilar: {users}")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(MessageHandler(filters.TEXT, handle))
app.add_handler(MessageHandler(filters.Regex("📊 Statistika"), stats))

app.run_polling()