# faq.py
# Respostas estáticas para perguntas frequentes sobre vacinação e saúde.
# Consultado ANTES de chamar o modelo — mais rápido e 100% previsível.

from utils.normalizar import normalizar

# ── Base de perguntas e respostas ─────────────────────────────────────────────
# Cada entrada tem:
#   "gatilhos": lista de fragmentos normalizados que ativam a resposta
#   "resposta": texto HTML enviado ao usuário

_FAQ: list[dict] = [

    # ── O que é vacinação ────────────────────────────────────────────────────
    {
        "gatilhos": ["o que e vacinacao", "o que e vacina", "conceito de vacina",
                     "definicao de vacina", "para que serve vacina",
                     "para que serve vacinacao", "como funciona vacina"],
        "resposta": (
            "💉 <b>O que é vacinação?</b>\n\n"
            "Vacinação é a administração de uma vacina ao organismo para estimular o sistema "
            "imunológico a produzir defesas contra uma doença específica.\n\n"
            "A vacina contém agentes enfraquecidos, inativados ou partes do microrganismo "
            "causador da doença. O corpo aprende a reconhecê-lo e fica preparado para "
            "combatê-lo no futuro — sem precisar adoecer de verdade."
        ),
    },

    # ── O que é cobertura vacinal ────────────────────────────────────────────
    {
        "gatilhos": ["o que e cobertura vacinal", "o que e cobertura", "conceito de cobertura",
                     "definicao de cobertura vacinal", "cobertura vacinal significa",
                     "o que significa cobertura"],
        "resposta": (
            "📊 <b>O que é cobertura vacinal?</b>\n\n"
            "Cobertura vacinal é o percentual da população-alvo que recebeu determinada vacina "
            "em um período e local específicos.\n\n"
            "Exemplo: cobertura de 90% significa que 9 em cada 10 pessoas do grupo-alvo "
            "foram vacinadas.\n\n"
            "A meta recomendada pelo Ministério da Saúde é <b>acima de 90%</b> para a maioria "
            "das vacinas do calendário nacional."
        ),
    },

    # ── O que é imunidade de rebanho ─────────────────────────────────────────
    {
        "gatilhos": ["imunidade de rebanho", "imunidade coletiva", "herd immunity",
                     "o que e imunidade de rebanho"],
        "resposta": (
            "🐑 <b>Imunidade de rebanho</b>\n\n"
            "Ocorre quando uma parcela grande o suficiente da população está imune a uma doença "
            "(por vacinação ou infecção prévia), protegendo indiretamente quem não pode ser vacinado "
            "— como recém-nascidos e imunossuprimidos.\n\n"
            "O percentual necessário varia por doença. Para sarampo, por exemplo, é preciso "
            "aproximadamente <b>95%</b> de cobertura."
        ),
    },

    # ── Calendário vacinal ───────────────────────────────────────────────────
    {
        "gatilhos": ["calendario vacinal", "calendario de vacinacao", "esquema vacinal",
                     "calendario nacional de vacinacao", "quais vacinas devo tomar",
                     "cronograma de vacinas"],
        "resposta": (
            "📅 <b>Calendário Nacional de Vacinação</b>\n\n"
            "O calendário vacinal do SUS define as vacinas recomendadas por faixa etária e grupo:\n\n"
            "• <b>Crianças (0–5 anos):</b> BCG, Hepatite B, Poliomielite, Pentavalente, Rotavírus, entre outras\n"
            "• <b>Adolescentes (9–17 anos):</b> HPV, Meningocócica, dT\n"
            "• <b>Adultos (18–59 anos):</b> Influenza, COVID-19, Hepatite B, dT\n"
            "• <b>Idosos (60+):</b> Influenza, COVID-19, Pneumocócica\n"
            "• <b>Gestantes:</b> dTpa, Influenza, Hepatite B\n\n"
            "Use o menu <b>Vacinas → Por Idade</b> para consultar por idade específica."
        ),
    },

    # ── Repouso após vacina ──────────────────────────────────────────────────
    {
        "gatilhos": ["repouso depois de vacina", "preciso ficar de repouso", "ficar em casa apos vacina",
                     "posso trabalhar depois da vacina", "posso fazer exercicio depois da vacina",
                     "academia apos vacina", "atividade fisica apos vacina",
                     "o que fazer depois de tomar vacina", "apos tomar vacina"],
        "resposta": (
            "🛌 <b>Após tomar uma vacina</b>\n\n"
            "Na maioria dos casos não é necessário repouso absoluto, mas é recomendado:\n\n"
            "• Aguardar <b>15–30 minutos</b> no local de vacinação para observação\n"
            "• Evitar esforços físicos intensos no dia da aplicação\n"
            "• Manter-se <b>hidratado</b>\n"
            "• Em caso de febre leve, prefer repouso e procurar orientação médica se persistir\n\n"
            "⚠️ Cada vacina pode ter orientações específicas. Consulte sempre o profissional de saúde."
        ),
    },

    # ── Efeitos colaterais gerais ────────────────────────────────────────────
    {
        "gatilhos": ["efeitos colaterais vacina", "reacao a vacina", "efeito adverso vacina",
                     "vacina tem efeito colateral", "efeitos da vacinacao",
                     "normal sentir dor apos vacina", "dor no braco apos vacina"],
        "resposta": (
            "⚠️ <b>Efeitos colaterais das vacinas</b>\n\n"
            "É normal sentir reações leves após a vacinação. As mais comuns são:\n\n"
            "• Dor, vermelhidão ou inchaço no local da injeção\n"
            "• Febre baixa (até 38°C)\n"
            "• Cansaço ou mal-estar leve\n"
            "• Dor de cabeça\n\n"
            "Essas reações geralmente desaparecem em <b>1 a 3 dias</b> e indicam que o "
            "organismo está respondendo à vacina.\n\n"
            "🚨 Procure atendimento médico se houver febre acima de 39°C, dificuldade para "
            "respirar, ou reação alérgica intensa."
        ),
    },

    # ── Vacina com febre ─────────────────────────────────────────────────────
    {
        "gatilhos": ["posso tomar vacina com febre", "vacina com febre", "estou com febre posso vacinar",
                     "tomar vacina doente"],
        "resposta": (
            "🌡️ <b>Vacina com febre</b>\n\n"
            "Em geral, <b>febre é uma contraindicação temporária</b> para a vacinação.\n\n"
            "Recomenda-se aguardar a melhora antes de se vacinar. Isso evita confundir sintomas "
            "da doença com possíveis reações da vacina.\n\n"
            "⚠️ Consulte sempre um profissional de saúde para avaliar seu caso específico."
        ),
    },

    # ── Vacina na gravidez ───────────────────────────────────────────────────
    {
        "gatilhos": ["vacina na gravidez", "gestante pode tomar vacina", "vacina gravida",
                     "vacina durante gestacao", "grávida pode se vacinar"],
        "resposta": (
            "🤰 <b>Vacinação na gravidez</b>\n\n"
            "Algumas vacinas são <b>recomendadas e seguras</b> durante a gestação:\n\n"
            "• <b>dTpa</b> (tétano, difteria e coqueluche) — a partir da 20ª semana\n"
            "• <b>Influenza</b> — em qualquer trimestre\n"
            "• <b>Hepatite B</b> — se não houver imunidade prévia\n\n"
            "Vacinas de vírus vivos atenuados (como febre amarela e tríplice viral) geralmente "
            "são <b>contraindicadas</b> durante a gravidez, exceto em situações de risco.\n\n"
            "⚠️ Sempre consulte seu obstetra antes de se vacinar."
        ),
    },

    # ── O que é o SUS ────────────────────────────────────────────────────────
    {
        "gatilhos": ["o que e o sus", "o que e sus", "como funciona o sus",
                     "sus oferece vacinas", "vacinas gratuitas sus"],
        "resposta": (
            "🏥 <b>SUS e vacinação</b>\n\n"
            "O Sistema Único de Saúde (SUS) oferece gratuitamente todas as vacinas do "
            "Calendário Nacional de Vacinação nos postos de saúde de todo o Brasil.\n\n"
            "As vacinas são aplicadas por profissionais capacitados, sem necessidade de "
            "agendamento na maioria dos municípios.\n\n"
            "Basta apresentar <b>documento com foto e carteira de vacinação</b> na UBS mais próxima."
        ),
    },

    # ── Posso vacinar gripado ─────────────────────────────────────────────────
    {
        "gatilhos": ["posso vacinar gripado", "estou gripado posso tomar vacina",
                     "resfriado pode tomar vacina", "vacina com resfriado"],
        "resposta": (
            "🤧 <b>Vacinar com gripe ou resfriado</b>\n\n"
            "Resfriados leves geralmente <b>não impedem</b> a vacinação.\n"
            "Porém, se houver febre, o recomendado é aguardar a melhora.\n\n"
            "⚠️ Em caso de dúvida, consulte o profissional de saúde no posto antes de se vacinar."
        ),
    },

    # ── Onde me vacinar ───────────────────────────────────────────────────────
    {
        "gatilhos": ["onde posso me vacinar", "onde tomar vacina", "como encontrar posto de vacinacao",
                     "posto de saude perto", "ubs perto", "onde fica posto de vacinacao"],
        "resposta": (
            "📍 <b>Como encontrar um posto de vacinação</b>\n\n"
            "• Procure a <b>UBS (Unidade Básica de Saúde)</b> mais próxima da sua residência\n"
            "• Pelo site ou app <b>ConecteSUS</b> você pode consultar postos e seu histórico vacinal\n"
            "• Durante campanhas, ginásios e postos volantes também aplicam vacinas\n\n"
            "O horário padrão dos postos é <b>segunda a sexta, das 7h às 17h</b>.\n"
            "Confirme com a secretaria de saúde do seu município."
        ),
    },

    # ── Vacina pode causar doença ─────────────────────────────────────────────
    {
        "gatilhos": ["vacina causa doenca", "vacina pode me deixar doente", "tomar vacina e adoecer",
                     "vacina transmite doenca", "vacina faz mal"],
        "resposta": (
            "❓ <b>Vacina pode causar doença?</b>\n\n"
            "Não. As vacinas do calendário nacional são testadas quanto à segurança e eficácia "
            "antes de serem aprovadas.\n\n"
            "• Vacinas inativadas ou de subunidades <b>não contêm vírus vivos</b> e não causam a doença\n"
            "• Vacinas de vírus atenuados contêm formas enfraquecidas que raramente causam sintomas leves\n\n"
            "Reações como febre leve ou dor local são respostas normais do sistema imunológico, "
            "não a doença em si."
        ),
    },
]

# ── Índice invertido: gatilho → resposta ──────────────────────────────────────
_INDICE: dict[str, str] = {}
for entrada in _FAQ:
    for gatilho in entrada["gatilhos"]:
        _INDICE[normalizar(gatilho)] = entrada["resposta"]


def buscar_faq(texto: str) -> str | None:
    """
    Verifica se o texto bate com algum gatilho do FAQ.
    Retorna a resposta ou None se não houver match.
    """
    texto_norm = normalizar(texto)
    for gatilho, resposta in _INDICE.items():
        if gatilho in texto_norm:
            return resposta
    return None