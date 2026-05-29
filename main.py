# main.py

import os
from dotenv import load_dotenv
import telebot

from cobertura.dados import carregar_dados
from cobertura.handler import registrar_cobertura
from vacinas.handler import registrar_vacinas
from handlers.menu import iniciar_menu
from handlers.ia_handler import processar_mensagem


# ── Config ────────────────────────────────────────────────────────────────────

load_dotenv()

TOKEN = os.getenv("TOKEN_BOT")
bot = telebot.TeleBot(TOKEN)

# Estado por usuário (modo atual no fluxo de botões)
user_states: dict = {}


# ── Dados ─────────────────────────────────────────────────────────────────────

carregar_dados()


# ── Handlers estruturados (menus/botões) ──────────────────────────────────────

registrar_cobertura(bot, user_states)
registrar_vacinas(bot, user_states)


# ── /start e /help ────────────────────────────────────────────────────────────

@bot.message_handler(commands=["start", "help"])
def start(msg):
    iniciar_menu(bot, msg)


# ── Texto livre → IA classifica e roteia ──────────────────────────────────────

@bot.message_handler(func=lambda m: True)
def mensagens(msg):
    processar_mensagem(bot, msg)


# ── Run ───────────────────────────────────────────────────────────────────────

print("🤖 Assistente Gotinha online!")
bot.infinity_polling()