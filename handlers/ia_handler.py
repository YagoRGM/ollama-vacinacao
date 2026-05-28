import ollama

from prompts import (
    SYSTEM_PROMPT,
    PROMPT_CLASSIFICADOR
)

def registrar_ia(bot):

    @bot.message_handler(
        func=lambda m: True
    )
    def responder(msg):

        texto = msg.text

        classificacao = ollama.chat(
            model="llama3.2:latest",
            messages=[
                {
                    "role": "system",
                    "content": PROMPT_CLASSIFICADOR
                },
                {
                    "role": "user",
                    "content": texto
                }
            ]
        )

        classe = (
            classificacao["message"]
            ["content"]
            .strip()
            .upper()
        )

        if classe == "FORA_CONTEXTO":

            bot.send_message(
                msg.chat.id,
                "Posso ajudar apenas com vacinação 💉"
            )

            return

        resposta = ollama.chat(
            model="llama3.2:latest",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": texto
                }
            ]
        )

        bot.send_message(
            msg.chat.id,
            resposta["message"]["content"]
        )