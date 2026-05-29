# cobertura/handler.py
# Handlers do Telegram para o módulo de cobertura vacinal.
# Toda lógica de dados fica em cobertura/dados.py.

from telebot import types

from cobertura.dados import (
    buscar_cobertura_estado,
    buscar_cobertura_municipio,
    ranking_estados,
)
from utils.estados import REGIOES, NOMES_ESTADOS


# ── Lista plana de todas as siglas ─────────────────────────────────────────────

_TODAS_SIGLAS = [uf for ufs in REGIOES.values() for uf in ufs]


def registrar_cobertura(bot, user_states: dict) -> None:
    """Registra todos os handlers relacionados à cobertura no bot."""

    # ── Menu de cobertura ─────────────────────────────────────────────────────

    @bot.message_handler(func=lambda m: m.text in ("Cobertura", "Cobertura Vacinal"))
    def menu_cobertura(msg):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add("Por Estado", "Por Município", "Ranking de Estados 🇧🇷", "⬅️ Voltar")

        bot.send_message(
            msg.chat.id,
            "Como deseja consultar a cobertura?",
            reply_markup=markup,
        )

    # ── Fluxo: Por Estado ─────────────────────────────────────────────────────

    @bot.message_handler(func=lambda m: m.text == "Por Estado")
    def escolher_regiao_estado(msg):
        user_states[msg.chat.id] = {"modo": "estado"}
        _enviar_menu_regioes(bot, msg)

    # ── Fluxo: Por Município ──────────────────────────────────────────────────

    @bot.message_handler(func=lambda m: m.text == "Por Município")
    def escolher_regiao_municipio(msg):
        user_states[msg.chat.id] = {"modo": "municipio"}
        _enviar_menu_regioes(bot, msg)

    # ── Seleção de Região → exibe estados da região ───────────────────────────

    @bot.message_handler(func=lambda m: m.text in REGIOES)
    def mostrar_estados_da_regiao(msg):
        siglas = REGIOES[msg.text]

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for uf in siglas:
            markup.add(f"{NOMES_ESTADOS[uf]} ({uf})")
        markup.add("⬅️ Voltar")

        bot.send_message(
            msg.chat.id,
            "Escolha o estado:",
            reply_markup=markup,
        )

    # ── Seleção de Estado ─────────────────────────────────────────────────────

    @bot.message_handler(
        func=lambda m: any(
            f"({uf})" in m.text for uf in _TODAS_SIGLAS
        )
    )
    def processar_estado(msg):
        # Extrai a sigla do texto "Nome do Estado (XX)"
        uf = msg.text.strip()[-3:-1]
        modo = user_states.get(msg.chat.id, {}).get("modo")

        if modo == "municipio":
            user_states[msg.chat.id]["uf"] = uf
            bot.send_message(msg.chat.id, "Digite o nome do município:")
            bot.register_next_step_handler(msg, _processar_municipio, bot, user_states)
            return

        # modo == "estado"
        resposta = buscar_cobertura_estado(uf)
        bot.send_message(msg.chat.id, resposta)

    # ── Ranking ───────────────────────────────────────────────────────────────

    @bot.message_handler(func=lambda m: m.text in ("Ranking", "Ranking de Estados 🇧🇷"))
    def ranking(msg):
        resposta = ranking_estados()
        bot.send_message(msg.chat.id, resposta, parse_mode="HTML")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _enviar_menu_regioes(bot, msg) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for regiao in REGIOES:
        markup.add(regiao)
    markup.add("⬅️ Voltar")
    bot.send_message(msg.chat.id, "Escolha a região:", reply_markup=markup)


def _processar_municipio(msg, bot, user_states: dict) -> None:
    municipio = msg.text.strip()
    uf = user_states.get(msg.chat.id, {}).get("uf")

    if not uf:
        bot.send_message(msg.chat.id, "⚠️ Estado não encontrado. Tente novamente.")
        return

    resposta = buscar_cobertura_municipio(uf, municipio)
    bot.send_message(msg.chat.id, resposta)