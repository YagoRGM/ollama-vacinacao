Eu quero criar uma mini versao do meu projeto (bot para acompanhamento sobre vacinacao, contendo proximas vacinas, cobertura vacinal, faq, ubs proximas, e um pouco mais) porem esta meio dificil impementar a inguagem natural com esse bot, atualemnte é feito atraves de botoes e comando com /), agora eu quero criar um mini projeto experimental usando Ollama para estudar, validar e definir a melhor arquitetura de IA para o projeto real do bot de vacinação (“Bot Gotinha”).

O objetivo principal NÃO é criar um sistema complexo logo de início, mas sim construir um ambiente simples, controlado e fácil de entender, focado em aprender como modelos locais funcionam na prática, e no final definir qual o melhor modelo que eu testar que vai ser o melhor para implementar no projeto completo, o que preciso definir, como prompts, tools  etc,para que nao de erros, e o bot seja minimamente inteigente, e saiba quando deve chamar funcoes e quais parametros enviar, quando a pergunta fugir do tema, relacione a mensagem atual/ultima recebida com mensagens antigas do mesmo usuario para nao perder o contexto, ex:
user: qual cobertura vacinal de sao paulo
bot: 88%(exemplo)
user: e do rio de janeiro
bot: a do rio é de 79%(correto pois relaiconou que era cobertura vacina que estav sendo referida pelo usuario, atraves da mensagem anterior)

Em resumo o bot deve funcionar como uma conversa mesmo, que o bot responda perguntas sobre o tema, chame funcoes prontaas, e essas coidsas entende

O projeto deve funcionar como um laboratório de IA aplicado ao contexto de vacinação pública.

---

# Objetivo central do projeto

Construir um assistente local em Python que:

* utiliza um modelo pequeno rodando no Ollama
* entende perguntas do usuário
* decide se deve:

  * responder normalmente
  * ou chamar uma função Python
* executa funções relacionadas à vacinação
* retorna respostas confiáveis e controladas

A ideia é separar claramente:

```txt id="95qv3o"
IA = decisão/intenção
Python = lógica/regras/dados
```

---

# Arquitetura desejada

O fluxo do sistema deve funcionar assim:

```txt id="ngcpxm"
Usuário
↓
Modelo IA analisa pergunta
↓
Decide qual função chamar
↓
Python executa a lógica
↓
Python monta resposta
↓
Usuário recebe resultado
```

A IA não deve ser responsável pela lógica do sistema nem pela geração livre de respostas críticas, apenas pela identificação da intenção do usuário.

---

# Tecnologias do projeto

## Linguagem

* Python

## IA local

* Ollama

## Modelo recomendado

* `qwen2.5:1.5b`

Porque:

* leve
* rápido
* roda em computadores simples
* bom para instruções e tool calling básico

---

# Objetivo técnico do laboratório

O projeto serve para estudar:

* tool calling manual
* engenharia de prompt
* roteamento de intenções
* integração IA + Python
* arquitetura de agentes
* limitações de modelos pequenos
* separação entre IA e lógica de negócio

---

# Funcionalidades que o sistema deve simular

O mini projeto deve representar as principais funcionalidades do projeto real do bot de vacinação.

## 1. Cobertura vacinal

Consulta de cobertura por:

* cidade
* estado
* ranking de todos os estados br

Exemplos:

```txt id="w7n15o"
Qual a cobertura vacinal de Campinas?
```

```txt id="hj6mwb"
Qual a cobertura da vacina de Sergipe?
```

---

## 2. Vacinas recomendadas por idade

O sistema deve indicar vacinas com base na idade informada.

Exemplo:

```txt id="3z1w91"
Quais vacinas uma criança de 5 anos deve tomar?
```

---

## 3. Vacinas recomendadas por grupo

Consulta baseada em grupos prioritários.

Exemplos:

* idosos
* gestantes
* adultos
* criancas e adolescentes
* recem nascidos

---

## 4. Informações sobre postos

Consulta de:

* endereço
* localização simplificada

---

## 5. Efeitos colaterais

Consulta de efeitos comuns de determinadas vacinas.

---

## 6. Respostas normais

Quando a pergunta não exigir ferramenta, o modelo deve responder normalmente.

Exemplo:

```txt id="4wdrby"
O que é vacinação?
```

---

# Estrutura desejada do projeto

O sistema deve ser modular e organizado.

Exemplo:

```txt id="p8c6yr"
mini-bot-vacina/
│
├── main.py
├── prompts.py
├── tools.py
├── database.py
├── utils.py
└── requirements.txt
```

---

# Estratégia de desenvolvimento

Você quer começar:

* simples
* controlado
* sem frameworks complexos

E evitar inicialmente:

* LangChain
* RAG
* banco vetorial
* multiagentes
* Docker
* Kubernetes

Porque o foco é entender e analisar modelos de agentes disponiveis no ollama e definir um padrao/ prompt para o agente dar a melhor resposta possivel.

---

# Estratégia da IA

A IA deve:

## Apenas decidir intenções

Exemplo:

```txt id="yjlwm5"
CALL_TOOL:consultar_cobertura_cidade:Campinas
```

## O Python deve:

* executar a função
* tratar dados
* montar resposta final

Isso torna o sistema:

* mais confiável
* mais previsível
* mais fácil de debugar
* menos sujeito a alucinações

---

# Objetivo futuro

Esse laboratório servirá como base para:

* integração com Telegram
* conexão com scraping
* leitura de CSV/Excel
* APIs públicas de vacinação
* evolução para um agente mais inteligente

---

# Resultado esperado

Ao final, o projeto deve permitir que vocês:

* entendam como integrar IA local em aplicações reais
* descubram os limites dos modelos pequenos
* validem a arquitetura do bot Gotinha
* decidam se vale continuar com Ollama local
* criem uma base sólida para evoluir o projeto real de vacinação


como esta esse mini projeto na versao atual

main.py
import ollama

from prompts import SYSTEM_PROMPT

from tools import *


def executar_tool(resposta):

    partes = resposta.split(":")

    nome = partes[1]
    parametro = partes[2]

    if nome == "consultar_cobertura_cidade":
        return consultar_cobertura_cidade(parametro)

    elif nome == "consultar_cobertura_estado":
        return consultar_cobertura_estado(parametro)

    elif nome == "consultar_cobertura_vacina":
        return consultar_cobertura_vacina(parametro)

    elif nome == "vacinas_por_idade":
        return vacinas_por_idade(parametro)

    elif nome == "vacinas_por_grupo":
        return vacinas_por_grupo(parametro)

    elif nome == "horario_posto":
        return horario_posto()

    elif nome == "endereco_posto":
        return endereco_posto(parametro)

    elif nome == "efeitos_colaterais":
        return efeitos_colaterais(parametro)

    return "Ferramenta não encontrada"


def montar_resposta(tool, parametro, resultado):

    if tool == "consultar_cobertura_cidade":
        return f"A cobertura vacinal de {parametro} é {resultado}"

    elif tool == "consultar_cobertura_estado":
        return f"A cobertura vacinal do estado {parametro} é {resultado}"

    elif tool == "consultar_cobertura_vacina":
        return f"A cobertura da vacina {parametro} é {resultado}"

    elif tool == "vacinas_por_idade":
        return f"As vacinas recomendadas para {parametro} anos são: {', '.join(resultado)}"

    elif tool == "vacinas_por_grupo":
        return f"As vacinas recomendadas para o grupo {parametro} são: {', '.join(resultado)}"

    elif tool == "horario_posto":
        return resultado

    elif tool == "endereco_posto":
        return f"Posto encontrado em {parametro}: {resultado}"

    elif tool == "efeitos_colaterais":
        return f"Efeitos colaterais comuns da vacina {parametro}: {', '.join(resultado)}"

    return str(resultado)


while True:

    pergunta = input("\nVocê: ")

    resposta = ollama.chat(
        model="qwen2.5:1.5b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": pergunta
            }
        ]
    )

    conteudo = resposta["message"]["content"]

    print("\nModelo:", conteudo)

    if conteudo.startswith("CALL_TOOL"):

        partes = conteudo.split(":")

        tool = partes[1]
        parametro = partes[2]

        resultado = executar_tool(conteudo)

        resposta_final = montar_resposta(
            tool,
            parametro,
            resultado
        )

        print("\nAssistente:", resposta_final)

    else:
        print("\nAssistente:", conteudo)

tools.py
from database import *


def consultar_cobertura_cidade(cidade):
    return COBERTURA_CIDADES.get(
        cidade.lower(),
        "Cidade não encontrada"
    )


def consultar_cobertura_estado(estado):
    return COBERTURA_ESTADOS.get(
        estado.lower(),
        "Estado não encontrado"
    )


def consultar_cobertura_vacina(vacina):
    return COBERTURA_VACINAS.get(
        vacina.lower(),
        "Vacina não encontrada"
    )


def vacinas_por_idade(idade):

    idade = int(idade)

    if idade <= 1:
        return [
            "BCG",
            "Hepatite B",
            "Pentavalente"
        ]

    elif idade <= 10:
        return [
            "Febre Amarela",
            "Tríplice Viral"
        ]

    elif idade <= 18:
        return [
            "HPV",
            "Meningocócica ACWY"
        ]

    return [
        "Influenza",
        "COVID-19"
    ]


def vacinas_por_grupo(grupo):

    grupos = {
        "idoso": [
            "Influenza",
            "COVID-19"
        ],

        "gestante": [
            "dTpa",
            "Hepatite B"
        ],

        "profissional da saúde": [
            "Hepatite B",
            "Influenza"
        ]
    }

    return grupos.get(
        grupo.lower(),
        ["Grupo não encontrado"]
    )


def horario_posto():
    return "Os postos funcionam das 8h às 17h"


def endereco_posto(cidade):

    postos = {
        "campinas": "UBS Centro - Rua das Flores, 100",
        "são paulo": "UBS Paulista - Av Paulista, 500",
        "santos": "UBS Praia - Rua do Porto, 45"
    }

    return postos.get(
        cidade.lower(),
        "Posto não encontrado"
    )


def efeitos_colaterais(vacina):

    efeitos = {
        "covid": [
            "dor no braço",
            "febre",
            "cansaço"
        ],

        "influenza": [
            "dor local",
            "mal-estar"
        ]
    }

    return efeitos.get(
        vacina.lower(),
        ["Vacina não encontrada"]
    )

database.py (ficticiozao, no projeto real é pego atraves de um excel baixado atraves de scrap)
COBERTURA_CIDADES = {
    "campinas": "88%",
    "são paulo": "92%",
    "santos": "79%"
}


COBERTURA_ESTADOS = {
    "são paulo": "90%",
    "minas gerais": "87%"
}


COBERTURA_VACINAS = {
    "covid": "91%",
    "influenza": "84%",
    "hpv": "76%"
}

prompts.py
SYSTEM_PROMPT = """
Você é um assistente de vacinação.

Seu trabalho é decidir qual ferramenta chamar.

Ferramentas disponíveis:

1. consultar_cobertura_cidade(cidade)
2. consultar_cobertura_estado(estado)
3. consultar_cobertura_vacina(vacina)
4. vacinas_por_idade(idade)
5. vacinas_por_grupo(grupo)
6. horario_posto()
7. endereco_posto(cidade)
8. efeitos_colaterais(vacina)

REGRAS IMPORTANTES:

- Responda SOMENTE no formato:
CALL_TOOL:nome:parametro

EXEMPLOS:

CALL_TOOL:consultar_cobertura_cidade:Campinas

CALL_TOOL:vacinas_por_idade:15

CALL_TOOL:horario_posto:none

Se não precisar ferramenta:
responda normalmente.
"""