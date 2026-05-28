from telebot import types

def registrar_faq(bot):

    @bot.message_handler(
        func=lambda m:
        m.text == "FAQ"
    )
    def faq(msg):

        markup = (
            types.ReplyKeyboardMarkup(
                resize_keyboard=True
            )
        )

        markup.add(
            "Documentos Necessários"
        )

        markup.add(
            "Reações Comuns"
        )

        bot.send_message(
            msg.chat.id,
            "📌 FAQ",
            reply_markup=markup
        )

    @bot.message_handler(
        func=lambda m:
        m.text ==
        "Documentos Necessários"
    )
    def docs(msg):

        bot.send_message(
            msg.chat.id,
            "📄 Documento com foto e carteira de vacinação."
        )

    @bot.message_handler(
        func=lambda m:
        m.text ==
        "Reações Comuns"
    )
    def reacoes(msg):

        bot.send_message(
            msg.chat.id,
            "🤒 Febre leve e cansaço por até 3 dias."
        )