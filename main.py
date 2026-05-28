import os
import threading

from dotenv import load_dotenv
from flask import Flask
import telebot

from handlers.menu import registrar_menu
from handlers.cobertura_handler import registrar_cobertura
from handlers.vacina_handler import registrar_vacinas
from handlers.faq_handler import registrar_faq
from handlers.ia_handler import registrar_ia

from cobertura import carregar_dados

# =========================
# CONFIG
# =========================

load_dotenv()

TOKEN = os.getenv("TOKEN_BOT")

bot = telebot.TeleBot(TOKEN)

user_states = {}

# =========================
# FLASK
# =========================

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Gotinha online ✅"

# =========================
# CARREGAR DADOS
# =========================

print("Carregando dados...")
carregar_dados()
print("Dados carregados.")

# =========================
# REGISTRAR HANDLERS
# =========================

registrar_menu(bot)
registrar_cobertura(bot, user_states)
registrar_vacinas(bot, user_states)
registrar_faq(bot)
registrar_ia(bot)

# =========================
# START
# =========================

if __name__ == "__main__":

    bot.remove_webhook()

    port = int(os.environ.get("PORT", 8080))

    t = threading.Thread(
        target=lambda: app.run(
            host="0.0.0.0",
            port=port,
            debug=False,
            use_reloader=False
        )
    )

    t.daemon = True
    t.start()

    print("🚀 Bot Gotinha iniciado!")

    bot.infinity_polling()