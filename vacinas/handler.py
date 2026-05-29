# vacinas/handler.py
# Handlers do Telegram para o módulo de vacinas.
# Toda lógica de dados fica em vacinas/dados.py.

from telebot import types

from vacinas.dados import (
    buscar_vacinas_por_idade,
    buscar_vacinas_por_grupo,
    buscar_efeitos_colaterais,
    buscar_info_vacina,
    listar_grupos,
    listar_vacinas,
    formatar_lista_vacinas,
)


# ── Grupos para exibição no menu ──────────────────────────────────────────────

_LABELS_GRUPO = {
    "idosos":                   "👴 Idosos",
    "gestantes":                "🤰 Gestantes",
    "criancas":                 "👶 Crianças",
    "adolescentes":             "🧒 Adolescentes",
    "adultos":                  "🧑 Adultos",
    "imunossuprimidos":         "🏥 Imunossuprimidos",
    "profissionais de saude":   "👨‍⚕️ Profissionais de Saúde",
}


def registrar_vacinas(bot, user_states: dict) -> None:
    """Registra todos os handlers relacionados a vacinas no bot."""

    # ── Menu principal de vacinas ─────────────────────────────────────────────

    @bot.message_handler(func=lambda m: m.text == "Vacinas")
    def menu_vacinas(msg):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add("💉 Por Idade", "👥 Por Grupo", "⚠️ Efeitos Colaterais", "⬅️ Voltar")

        bot.send_message(
            msg.chat.id,
            "O que você quer saber sobre vacinas?",
            reply_markup=markup,
        )

    # ── Fluxo: Por Idade ──────────────────────────────────────────────────────

    @bot.message_handler(func=lambda m: m.text == "💉 Por Idade")
    def pedir_idade(msg):
        user_states[msg.chat.id] = {"modo": "vacina_idade"}
        bot.send_message(msg.chat.id, "Digite sua idade (em anos):")
        bot.register_next_step_handler(msg, _processar_idade, bot)

    # ── Fluxo: Por Grupo ──────────────────────────────────────────────────────

    @bot.message_handler(func=lambda m: m.text == "👥 Por Grupo")
    def escolher_grupo(msg):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for label in _LABELS_GRUPO.values():
            markup.add(label)
        markup.add("⬅️ Voltar")

        bot.send_message(
            msg.chat.id,
            "Escolha o grupo:",
            reply_markup=markup,
        )

    @bot.message_handler(func=lambda m: m.text in _LABELS_GRUPO.values())
    def processar_grupo(msg):
        # Converte label de volta para chave interna
        chave = next(k for k, v in _LABELS_GRUPO.items() if v == msg.text)
        vacinas = buscar_vacinas_por_grupo(chave)
        resposta = formatar_lista_vacinas(
            f"💉 Vacinas para {msg.text}:", vacinas
        )
        bot.send_message(msg.chat.id, resposta)

    # ── Fluxo: Efeitos Colaterais ─────────────────────────────────────────────

    @bot.message_handler(func=lambda m: m.text == "⚠️ Efeitos Colaterais")
    def escolher_vacina_efeitos(msg):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for vacina in listar_vacinas():
            markup.add(vacina.title())
        markup.add("⬅️ Voltar")

        bot.send_message(
            msg.chat.id,
            "Sobre qual vacina deseja saber os efeitos colaterais?",
            reply_markup=markup,
        )

    @bot.message_handler(
        func=lambda m: m.text.lower() in listar_vacinas()
    )
    def processar_efeitos(msg):
        efeitos = buscar_efeitos_colaterais(msg.text)
        itens = "\n".join(f"  • {e}" for e in efeitos)
        resposta = f"⚠️ Efeitos colaterais de <b>{msg.text.title()}</b>:\n{itens}"
        bot.send_message(msg.chat.id, resposta, parse_mode="HTML")

    # ── Voltar ao menu principal ───────────────────────────────────────────────

    @bot.message_handler(func=lambda m: m.text == "⬅️ Voltar")
    def voltar(msg):
        from handlers.menu import iniciar_menu
        iniciar_menu(bot, msg)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _processar_idade(msg, bot) -> None:
    try:
        idade = int(msg.text.strip())
    except ValueError:
        bot.send_message(msg.chat.id, "⚠️ Digite um número válido para a idade.")
        return

    vacinas = buscar_vacinas_por_idade(idade)
    resposta = formatar_lista_vacinas(
        f"💉 Vacinas recomendadas para {idade} anos:", vacinas
    )
    bot.send_message(msg.chat.id, resposta)