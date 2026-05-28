from telebot import types

from cobertura import (
    buscar_cobertura_estado,
    buscar_cobertura_municipio,
    ranking_estados
)

from utils.estados import REGIOES

def registrar_cobertura(
    bot,
    user_states
):

    @bot.message_handler(
        func=lambda m:
        m.text == "Cobertura Vacinal"
    )
    def menu_cobertura(msg):

        markup = (
            types.ReplyKeyboardMarkup(
                resize_keyboard=True
            )
        )

        markup.add("Estado")
        markup.add("Município")
        markup.add("Ranking de Estados 🇧🇷")
        markup.add("Voltar ao Menu Principal")

        bot.send_message(
            msg.chat.id,
            "Como deseja consultar?",
            reply_markup=markup
        )

    @bot.message_handler(
        func=lambda m:
        m.text == "Estado"
    )
    def escolher_regiao(msg):

        user_states[msg.chat.id] = {
            "modo": "estado"
        }

        markup = (
            types.ReplyKeyboardMarkup(
                resize_keyboard=True
            )
        )

        for regiao in REGIOES:
            markup.add(regiao)

        bot.send_message(
            msg.chat.id,
            "Escolha a região:",
            reply_markup=markup
        )

    @bot.message_handler(
        func=lambda m:
        m.text == "Município"
    )
    def municipio(msg):

        user_states[msg.chat.id] = {
            "modo": "municipio"
        }

        markup = (
            types.ReplyKeyboardMarkup(
                resize_keyboard=True
            )
        )

        for regiao in REGIOES:
            markup.add(regiao)

        bot.send_message(
            msg.chat.id,
            "Escolha a região:",
            reply_markup=markup
        )

    @bot.message_handler(
        func=lambda m:
        m.text in REGIOES.keys()
    )
    def mostrar_estados(msg):

        estados = REGIOES[msg.text]

        markup = (
            types.ReplyKeyboardMarkup(
                resize_keyboard=True
            )
        )

        for estado in estados:
            markup.add(estado)

        bot.send_message(
            msg.chat.id,
            "Escolha o estado:",
            reply_markup=markup
        )

    @bot.message_handler(
        func=lambda m:
        m.text in sum(
            REGIOES.values(),
            []
        )
    )
    def processar_estado(msg):

        modo = (
            user_states
            .get(msg.chat.id, {})
            .get("modo")
        )

        estado = msg.text

        if modo == "municipio":

            user_states[msg.chat.id][
                "uf"
            ] = estado

            bot.send_message(
                msg.chat.id,
                "Digite o município:"
            )

            bot.register_next_step_handler(
                msg,
                processar_municipio
            )

            return

        resposta = (
            buscar_cobertura_estado(
                estado
            )
        )

        bot.send_message(
            msg.chat.id,
            resposta
        )

    def processar_municipio(msg):

        municipio = msg.text

        uf = (
            user_states[msg.chat.id]["uf"]
        )

        resposta = (
            buscar_cobertura_municipio(
                uf,
                municipio
            )
        )

        bot.send_message(
            msg.chat.id,
            resposta
        )

    @bot.message_handler(
        func=lambda m:
        m.text ==
        "Ranking de Estados 🇧🇷"
    )
    def ranking(msg):

        resposta = ranking_estados()

        bot.send_message(
            msg.chat.id,
            resposta
        )