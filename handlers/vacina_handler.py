from telebot import types

from vacinas import obter_vacinas

def registrar_vacinas(
    bot,
    user_states
):

    @bot.message_handler(
        func=lambda m:
        m.text == "Vacinas"
    )
    def vacinas(msg):

        markup = (
            types.ReplyKeyboardMarkup(
                resize_keyboard=True
            )
        )

        markup.add("Crianca")
        markup.add("Adolescente")
        markup.add("Adulto")
        markup.add("Idoso")
        markup.add("Gestante")

        bot.send_message(
            msg.chat.id,
            "Escolha o grupo:",
            reply_markup=markup
        )

    @bot.message_handler(
        func=lambda m:
        m.text in [
            "Crianca",
            "Adolescente",
            "Adulto",
            "Idoso",
            "Gestante"
        ]
    )
    def grupos(msg):

        vacinas = obter_vacinas(
            msg.text
        )

        texto = (
            f"💉 Vacinas para "
            f"{msg.text}:\n\n"
        )

        for vacina in vacinas:
            texto += f"• {vacina}\n"

        bot.send_message(
            msg.chat.id,
            texto
        )