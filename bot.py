import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# .env dosyasındaki şifreleri yükle
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq istemcisi
client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# Sohbet geçmişleri
chat_histories = {}

# --- YASAL KOMUTLAR ---
async def gizlilik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("gizlilik.txt", "r", encoding="utf-8") as f:
        await update.message.reply_text(f.read())

async def kvkk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("kvkk.txt", "r", encoding="utf-8") as f:
        await update.message.reply_text(f.read())

async def kullanim_kosullari(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("kullanim_kosullari.txt", "r", encoding="utf-8") as f:
        await update.message.reply_text(f.read())

# --- VERİ SİLME KOMUTU ---
async def verilerimi_sil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in chat_histories:
        del chat_histories[chat_id]
        await update.message.reply_text("✅ Sohbet geçmişiniz ve verileriniz başarıyla silindi. KVKK hakkınızı kullandınız.")
    else:
        await update.message.reply_text("ℹ️ Sistemde zaten kayıtlı bir veriniz bulunmuyor.")

# --- BAŞLANGIÇ VE YARDIM ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Merhaba! Ben Orion.AI. Size yardımcı olmaktan mutluluk duyarım.\n\n"
        "Yasal haklarınız ve bilgilendirmeler için:\n"
        "/gizlilik - Gizlilik Politikası\n"
        "/kvkk - KVKK Aydınlatma Metni\n"
        "/kullanim_kosullari - Kullanım Koşulları\n"
        "/verilerimi_sil - Verilerinizi silmek için"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bana istediğiniz her şeyi sorabilirsiniz. Yasal metinler için /start yazabilirsiniz.")

# --- YAPAY ZEKA SOHBETİ ---
async def ai_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_message = update.message.text

    await update.message.reply_text("Düşünüyorum...")

    if chat_id not in chat_histories:
        chat_histories[chat_id] = [
            {"role": "system", "content": "Sen Orion.AI adında, yardımcı ve profesyonel bir yapay zeka asistanısın."}
        ]
    
    chat_histories[chat_id].append({"role": "user", "content": user_message})

    try:
        response = await client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=chat_histories[chat_id]
        )
        reply = response.choices[0].message.content
        chat_histories[chat_id].append({"role": "assistant", "content": reply})
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text("Şu an yanıt veremiyorum, lütfen birazdan tekrar deneyin.")
        print(f"\n--- GROQ HATASI ---\n{type(e).__name__}: {e}\n-------------------\n")

# --- BOTU BAŞLATMA ---
def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Komutları ekle
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("gizlilik", gizlilik))
    application.add_handler(CommandHandler("kvkk", kvkk))
    application.add_handler(CommandHandler("kullanim_kosullari", kullanim_kosullari))
    application.add_handler(CommandHandler("verilerimi_sil", verilerimi_sil))
    
    # Normal mesajları yapay zekaya yönlendir
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_response))
    
    print("Orion.AI çalışıyor... Profesyonel mod aktif.")
    application.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
