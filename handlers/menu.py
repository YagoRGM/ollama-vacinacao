# handlers/menu.py

from telebot import types


def iniciar_menu(bot, msg) -> None:
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2,
    )
    markup.add("Cobertura", "Ranking")
    markup.add("Vacinas")

    bot.send_message(
        msg.chat.id,
        (
            "Olá! 👋\n\n"
            "Sou o <b>Assistente Gotinha</b> 💉\n\n"
            "Posso ajudar com:\n"
            "• Cobertura vacinal\n"
            "• Ranking nacional\n"
            "• Vacinas por idade ou grupo"
        ),
        reply_markup=markup,
        parse_mode="HTML",
    )