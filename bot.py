import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

chat_histories = {}

# --- YASAL METİNLER (Kodun içine gömüldü) ---
GIZLILIK_METNI = """Gizlilik Politikası (Orion.AI)

Bu Gizlilik Politikası, Telegram üzerinde çalışan Orion.AI botunun ("Bot") kullanıcı verilerini nasıl topladığını, kullandığını ve koruduğunu açıklar.

1. Toplanan Veriler:
Botu kullandığınızda, hizmeti sağlamak amacıyla aşağıdaki veriler işlenir:
- Telegram Kullanıcı ID'niz
- Bot ile paylaştığınız sohbet mesajları (metin)
- Botun size verdiği yanıtlar

2. Verilerin Kullanım Amacı:
Toplanan veriler yalnızca aşağıdaki amaçlarla kullanılır:
- Size yapay zeka destekli sohbet hizmeti sunmak.
- Sohbet geçmişinizi hatırlayarak daha tutarlı yanıtlar üretmek.
- Hizmetin güvenliğini ve işleyişini sağlamak.

3. Verilerin Paylaşımı:
Sohbet mesajlarınız, yanıt üretmek amacıyla Groq API gibi üçüncü taraf yapay zeka hizmet sağlayıcılarına iletilebilir. Bu sağlayıcılar, verileri yalnızca hizmeti sunmak için işler. Verileriniz pazarlama amacıyla satılmaz veya kiralanmaz.

4. Veri Saklama ve Silme:
Sohbet geçmişiniz, hizmetin işleyişi için gerekli olduğu sürece saklanır. Dilediğiniz zaman bot üzerinden /verilerimi_sil komutunu kullanarak verilerinizin silinmesini talep edebilirsiniz.

5. İletişim:
Gizlilik politikamızla ilgili sorularınız için orionai.destek@gmail.com üzerinden bizimle iletişime geçebilirsiniz."""

KVKK_METNI = """KVKK Aydınlatma Metni (Orion.AI)

İşbu Aydınlatma Metni, 6698 sayılı Kişisel Verilerin Korunması Kanunu ("KVKK") kapsamında, veri sorumlusu Orion.AI tarafından sunulan hizmetler kapsamında kişisel verilerinizin işlenmesine ilişkin olarak sizi bilgilendirmek amacıyla hazırlanmıştır.

1. İşlenen Kişisel Veriler:
- Kimlik Verisi: Telegram Kullanıcı ID'si
- İletişim Verisi: Sohbet mesajları
- İşlem Güvenliği Verisi: Bot kullanım logları

2. Kişisel Verilerin İşlenme Amaçları:
- Yapay zeka destekli sohbet hizmetinin sunulması
- Hizmet kalitesinin artırılması ve geliştirilmesi
- Yasal yükümlülüklerin yerine getirilmesi

3. Kişisel Verilerin Aktarılması:
Kişisel verileriniz, yukarıda belirtilen amaçlarla sınırlı olarak ve KVKK'nın 8. ve 9. maddelerinde öngörülen şartlara uygun olarak, yapay zeka hizmeti alınan Groq gibi yurt dışı merkezli hizmet sağlayıcılarına aktarılabilmektedir.

4. KVKK Kapsamındaki Haklarınız:
KVKK'nın 11. maddesi uyarınca; kişisel verilerinizin işlenip işlenmediğini öğrenme, işlenmişse buna ilişkin bilgi talep etme, işlenme amacını ve bunların amacına uygun kullanılıp kullanılmadığını öğrenme, eksik veya yanlış işlenmiş olması hâlinde bunların düzeltilmesini isteme ve silinmesini talep etme haklarına sahipsiniz. Bu haklarınızı kullanmak için orionai.destek@gmail.com üzerinden bizimle iletişime geçebilirsiniz."""

KULLANIM_KOSULLARI_METNI = """Kullanım Koşulları (Orion.AI)

Bu Kullanım Koşulları, Orion.AI botunu ("Bot") kullanımınıza ilişkin kuralları belirler. Botu kullanarak bu koşulları kabul etmiş sayılırsınız.

1. Hizmetin Tanımı:
Bot, kullanıcıların metin tabanlı sorularına yapay zeka kullanarak yanıt veren bir sohbet asistanıdır.

2. Kullanıcı Yükümlülükleri:
- Botu yasadışı, zararlı, tehditkar, hakaret içeren veya müstehcen amaçlarla kullanmayacağınızı kabul edersiniz.
- Bot üzerinden spam mesaj göndermeyeceğinizi, diğer kullanıcıları rahatsız etmeyeceğinizi kabul edersiniz.
- Botun güvenliğini veya işleyişini bozacak her türlü girişimden kaçınacağınızı kabul edersiniz.

3. Sorumluluk Reddi:
Bot tarafından sağlanan bilgiler yalnızca genel bilgilendirme amaçlıdır ve profesyonel tavsiye (hukuki, tıbbi, mali vb.) yerine geçmez. Botun yanıtlarının doğruluğu, eksiksizliği veya güncelliği konusunda hiçbir garanti verilmez. Botun kullanımından doğabilecek herhangi bir zarardan sorumlu tutulamayız.

4. Değişiklikler:
Bu koşullar, önceden bildirimde bulunulmaksızın zaman zaman güncellenebilir. Güncel koşullar her zaman bot üzerinden erişilebilir olacaktır.

5. İletişim:
Sorularınız için orionai.destek@gmail.com üzerinden bizimle iletişime geçebilirsiniz."""

# --- KOMUTLAR ---
async def gizlilik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(GIZLILIK_METNI)

async def kvkk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(KVKK_METNI)

async def kullanim_kosullari(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(KULLANIM_KOSULLARI_METNI)

async def verilerimi_sil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in chat_histories:
        del chat_histories[chat_id]
        await update.message.reply_text("✅ Sohbet geçmişiniz ve verileriniz başarıyla silindi. KVKK hakkınızı kullandınız.")
    else:
        await update.message.reply_text("ℹ️ Sistemde zaten kayıtlı bir veriniz bulunmuyor.")

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

def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("gizlilik", gizlilik))
    application.add_handler(CommandHandler("kvkk", kvkk))
    application.add_handler(CommandHandler("kullanim_kosullari", kullanim_kosullari))
    application.add_handler(CommandHandler("verilerimi_sil", verilerimi_sil))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_response))
    
    print("Orion.AI çalışıyor... Profesyonel mod aktif.")
    application.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
