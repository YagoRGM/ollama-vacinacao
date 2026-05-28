from telebot import types

def registrar_menu(bot):

    @bot.message_handler(
        commands=["start", "help"]
    )
    def start(msg):

        markup = (
            types.ReplyKeyboardMarkup(
                resize_keyboard=True
            )
        )

        markup.add("Início")
        markup.add("Vacinas")
        markup.add("Cobertura Vacinal")
        markup.add("FAQ")

        bot.send_message(
            msg.chat.id,
            "Olá! 👋\n\nSou o Assistente Gotinha 💉",
            reply_markup=markup
        )