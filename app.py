import streamlit as st
import streamlit.components.v1 as components
import html
import json

# ==========================================
# CIENTISTA DE BOLSO
# Primeira versão do aplicativo
# ==========================================

st.set_page_config(
    page_title="Cientista de Bolso",
    page_icon="🔬",
    layout="centered"
)

# VISUAL CALMO E ACESSÍVEL
st.markdown("""
<style>
.stApp {
    background-color: #F5F8F5;
}
h1, h2, h3 {
    color: #315F52;
}
p, label, li {
    color: #34463F;
    line-height: 1.7;
}
.stButton > button {
    min-height: 55px;
    border-radius: 14px;
    font-size: 17px;
    font-weight: 600;
    border: 1px solid #A9C9BA;
    background-color: #E5F0E9;
    color: #285747;
}
.stTextInput input, .stTextArea textarea {
    font-size: 18px;
    border-radius: 12px;
}
.stRadio label {
    font-size: 17px;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# INVESTIGAÇÕES PRONTAS
# Funcionam sem conexão com a IA
# ==========================================

investigacoes = {

    "pao": {
        "titulo": "Por que o pão cresce?",
        "emoji": "🍞",
        "hipoteses": [
            "O fermento produz um gás.",
            "A farinha aumenta de tamanho.",
            "O pão cresce sozinho."
        ],
        "materiais": [
            "Um copo transparente.",
            "Água morna, nunca quente.",
            "Fermento biológico seco.",
            "Um pouco de açúcar.",
            "Uma colher."
        ],
        "passos": [
            "Coloque um pouco de água morna no copo.",
            "Acrescente uma pequena quantidade de fermento.",
            "Coloque uma pitada de açúcar.",
            "Misture devagar.",
            "Observe o que acontece durante alguns minutos."
        ],
        "sensoriais": [
            "BARULHO: pode haver um pequeno som de bolhas.",
            "ÁGUA: pode molhar a colher e as mãos.",
            "CHEIRO: o fermento pode ter um cheiro próprio.",
            "TEXTURA: a mistura pode ficar um pouco grudenta.",
            "VISUAL: podem aparecer bolhas e espuma."
        ],
        "observacoes": [
            "Apareceram bolhas?",
            "A mistura mudou de tamanho?",
            "Apareceu espuma?",
            "O que você observou?"
        ],
        "explicacao": (
            "O fermento biológico tem seres vivos muito pequenos "
            "chamados leveduras. Eles usam o açúcar e produzem "
            "um gás chamado gás carbônico. Na massa do pão, "
            "esse gás fica preso em pequenos espaços e faz a "
            "massa aumentar de tamanho. No forno, o pão assa."
        ),
        "explicacao_curta": (
            "O fermento tem seres vivos muito pequenos. "
            "Eles produzem um gás. Esse gás forma bolhas "
            "na massa e faz o pão crescer."
        ),
        "cuidado": (
            "Faça a experiência com um adulto. Não beba a mistura. "
            "Não use água quente. A experiência demonstra a ação "
            "do fermento, mas não substitui o preparo do pão."
        )
    },

    "poca": {
        "titulo": "Para onde vai a água da poça?",
        "emoji": "💧",
        "hipoteses": [
            "A água vira vapor e vai para o ar.",
            "A água entra no chão.",
            "A água desaparece completamente."
        ],
        "materiais": [
            "Dois pratos iguais.",
            "Um pouco de água.",
            "Um local com sol.",
            "Um local com sombra."
        ],
        "passos": [
            "Coloque a mesma quantidade de água nos dois pratos.",
            "Deixe um prato em um local com sol.",
            "Deixe o outro em um local com sombra.",
            "Observe os pratos depois de algum tempo.",
            "Compare a quantidade de água."
        ],
        "sensoriais": [
            "BARULHO: não é esperada uma mudança de som.",
            "ÁGUA: pode molhar as mãos.",
            "CHEIRO: não é esperado cheiro diferente.",
            "TEXTURA: a água é líquida e pode molhar a pele.",
            "TEMPERATURA: o prato no sol pode ficar quente."
        ],
        "observacoes": [
            "Qual prato perdeu mais água?",
            "A quantidade de água mudou?",
            "O sol fez diferença?",
            "O que você observou?"
        ],
        "explicacao": (
            "O calor ajuda a água líquida a passar para o estado "
            "gasoso. Esse processo se chama evaporação. A água "
            "continua existindo, mas fica misturada ao ar como "
            "vapor de água. O sol pode acelerar a evaporação."
        ),
        "explicacao_curta": (
            "O calor faz parte da água passar para o ar "
            "em forma de vapor. Esse processo se chama "
            "evaporação. A água não desapareceu."
        ),
        "cuidado": (
            "Faça a experiência com um adulto. Não deixe os pratos "
            "em locais de passagem. Não olhe diretamente para o sol. "
            "Não use água quente."
        )
    },

    "coracao": {
        "titulo": "Por que o coração acelera quando corremos?",
        "emoji": "❤️",
        "hipoteses": [
            "O coração bate mais rápido para levar sangue pelo corpo.",
            "O coração fica cansado e para de funcionar.",
            "O coração bate mais rápido porque fazemos barulho."
        ],
        "materiais": [
            "Um relógio ou cronômetro.",
            "Um local seguro para ficar em pé.",
            "A ajuda de um adulto."
        ],
        "passos": [
            "Sente-se e descanse por alguns minutos.",
            "Com ajuda de um adulto, perceba os batimentos no pulso.",
            "Conte os batimentos durante 30 segundos, se conseguir.",
            "Marche devagar no mesmo lugar por 30 segundos.",
            "Pare, descanse e perceba novamente os batimentos."
        ],
        "sensoriais": [
            "BARULHO: não é esperado barulho especial.",
            "MOVIMENTO: você vai movimentar as pernas.",
            "SUOR: o corpo pode ficar um pouco suado.",
            "TEMPERATURA: o corpo pode ficar mais quente.",
            "TOQUE: pode ser necessário tocar o pulso."
        ],
        "observacoes": [
            "O coração bateu mais rápido depois do movimento?",
            "Sua respiração mudou?",
            "O que aconteceu depois do descanso?",
            "O que você observou?"
        ],
        "explicacao": (
            "Quando fazemos atividade física, os músculos precisam "
            "de mais oxigênio e nutrientes. O coração bombeia o "
            "sangue mais rapidamente para ajudar a levar essas "
            "substâncias pelo corpo. Depois do descanso, os "
            "batimentos costumam diminuir novamente."
        ),
        "explicacao_curta": (
            "Quando corremos, os músculos precisam de mais "
            "oxigênio. O coração bate mais rápido para ajudar "
            "a levar sangue aos músculos."
        ),
        "cuidado": (
            "Esta atividade é opcional. Não é necessário correr. "
            "Faça apenas movimentos confortáveis, com supervisão "
            "de um adulto. Pare se sentir dor, tontura, falta de ar "
            "fora do habitual ou desconforto. Não force a contagem "
            "dos batimentos."
        )
    }
}


# ==========================================
# ADAPTAÇÃO DA LINGUAGEM
# ==========================================

def adaptar_texto(texto, nivel, curto=None):

    if nivel == "Ainda não leio":
        return curto if curto else texto

    if nivel == "Estou começando a ler":
        return texto

    return texto


# ==========================================
# CABEÇALHO
# ==========================================

st.title("🔬 Cientista de Bolso")

st.markdown(
    "Toda pergunta pode virar uma descoberta!"
)

st.markdown(
    "Aqui, vamos observar, pensar e investigar "
    "uma coisa de cada vez."
)

st.divider()


# ==========================================
# ESCOLHA DO NÍVEL DE LEITURA
# ==========================================

st.subheader("📖 Como está a leitura?")

nivel = st.radio(
    "O professor escolhe o nível da criança:",
    [
        "Ainda não leio",
        "Estou começando a ler",
        "Já leio bem"
    ],
    horizontal=False
)


# ==========================================
# ESCOLHA DA PERGUNTA
# ==========================================

st.subheader("🔎 O que você quer descobrir?")

pergunta_pronta = st.selectbox(
    "Escolha uma pergunta:",
    [
        "Escolha uma pergunta pronta...",
        "Por que o pão cresce?",
        "Para onde vai a água da poça?",
        "Por que o coração acelera quando corremos?"
    ]
)

pergunta_digitada = st.text_input(
    "Ou escreva sua própria pergunta:",
    placeholder="Exemplo: Por que as folhas são verdes?"
)

if st.button("🔬 COMEÇAR A INVESTIGAR", use_container_width=True):

    pergunta = pergunta_digitada.strip() if pergunta_digitada.strip() else pergunta_pronta

    pergunta = pergunta.lower()

    if "pão" in pergunta or "pao" in pergunta:
        st.session_state.investigacao = "pao"

    elif "poça" in pergunta or "poca" in pergunta or "água" in pergunta or "agua" in pergunta:
        st.session_state.investigacao = "poca"

    elif "coração" in pergunta or "coracao" in pergunta:
        st.session_state.investigacao = "coracao"

    elif pergunta == "escolha uma pergunta pronta...":
        st.warning("Escolha ou escreva uma pergunta primeiro.")
        st.session_state.investigacao = None

    else:
        st.session_state.investigacao = None
        st.session_state.pergunta_nova = pergunta_digitada.strip()

    st.session_state.etapa = 0
    st.rerun()


# ==========================================
# MOSTRAR A INVESTIGAÇÃO
# ==========================================

if "etapa" not in st.session_state:
    st.session_state.etapa = 0

if "investigacao" not in st.session_state:
    st.session_state.investigacao = None

if st.session_state.investigacao:

    dados = investigacoes[st.session_state.investigacao]

    st.divider()

    st.subheader(
        dados["emoji"] + " " + dados["titulo"]
    )

    st.progress(
        (st.session_state.etapa + 1) / 4
    )

    etapa = st.session_state.etapa

    # CARTÃO 1
    if etapa == 0:

        st.markdown("## 1. 💭 Eu acho que...")

        st.write(
            "O que você acha que vai acontecer?"
        )

        resposta = st.radio(
            "Escolha sua ideia:",
            dados["hipoteses"],
            key="hipotese"
        )

        st.success("Minha ideia: " + resposta)

    # CARTÃO 2
    elif etapa == 1:

        st.markdown("## 2. 🧪 Vamos testar!")

        st.markdown("### Antes de começar: como será a experiência?")

        for aviso in dados["sensoriais"]:
            st.info(aviso)

        st.warning(dados["cuidado"])

        st.markdown("### Materiais")

        for material in dados["materiais"]:
            st.write("☐ " + material)

        st.markdown("### Passo a passo")

        for numero, passo in enumerate(dados["passos"], 1):
            st.write(f"**{numero}.** {passo}")

    # CARTÃO 3
    elif etapa == 2:

        st.markdown("## 3. 👀 O que aconteceu?")

        st.write(
            "Observe com atenção. Depois, responda:"
        )

        for pergunta in dados["observacoes"]:
            st.write("• " + pergunta)

        st.text_area(
            "Minhas observações:",
            placeholder="Eu observei que...",
            height=140,
            key="observacao"
        )

    # CARTÃO 4
    elif etapa == 3:

        st.markdown("## 4. 💡 O que descobrimos!")

        explicacao = adaptar_texto(
            dados["explicacao"],
            nivel,
            dados["explicacao_curta"]
        )

        st.success(explicacao)

        st.markdown("### E você?")

        st.text_area(
            "O que você aprendeu?",
            placeholder="Eu descobri que...",
            height=120,
            key="descoberta"
        )

        st.balloons = False

        st.caption(
            "Cada pessoa pode aprender no seu próprio ritmo."
        )

    # ======================================
    # BOTÕES DE NAVEGAÇÃO
    # ======================================

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if etapa > 0:
            if st.button("← VOLTAR", use_container_width=True):
                st.session_state.etapa -= 1
                st.rerun()

    with col2:
        if etapa < 3:
            if st.button("PRÓXIMO →", use_container_width=True):
                st.session_state.etapa += 1
                st.rerun()
        else:
            if st.button("COMEÇAR OUTRA INVESTIGAÇÃO", use_container_width=True):
                st.session_state.investigacao = None
                st.session_state.etapa = 0
                st.rerun()

    # ======================================
    # BOTÃO PARA OUVIR
    # ======================================

    textos_audio = [
        "Eu acho que. " + " ".join(dados["hipoteses"]),
        "Vamos testar. " + " ".join(dados["passos"]),
        "O que aconteceu? " + " ".join(dados["observacoes"]),
        "O que descobrimos. " + dados["explicacao"]
    ]

    texto_audio = json.dumps(
        textos_audio[etapa],
        ensure_ascii=False
    )

    st.markdown("### 🔊 Ouvir este cartão")

    components.html(
        f"""
        <button onclick='
            window.speechSynthesis.cancel();
            var fala = new SpeechSynthesisUtterance({texto_audio});
            fala.lang = "pt-BR";
            fala.rate = 0.85;
            window.speechSynthesis.speak(fala);
        ' style="
            background:#E5F0E9;
            color:#285747;
            border:1px solid #A9C9BA;
            border-radius:14px;
            padding:16px 24px;
            font-size:18px;
            cursor:pointer;
            width:100%;
        ">
            🔊 Ouvir o texto
        </button>
        """,
        height=75
    )

    # ======================================
    # VERSÃO PARA IMPRIMIR
    # ======================================

    st.divider()

    conteudo_impressao = f"""
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
    body {{
        font-family: Arial, sans-serif;
        color: #263C32;
        margin: 30px;
    }}
    .cartao {{
        border: 2px solid #A9C9BA;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 30px;
        min-height: 250px;
        page-break-after: always;
    }}
    h1, h2 {{ color: #315F52; }}
    li {{ margin-bottom: 12px; }}
    .resposta {{
        border-bottom: 1px solid #777;
        height: 40px;
    }}
    </style>
    </head>
    <body>
    <h1>🔬 Cientista de Bolso</h1>
    <h2>{html.escape(dados["titulo"])}</h2>

    <div class="cartao">
    <h2>1. Eu acho que...</h2>
    <p>{html.escape(" | ".join(dados["hipoteses"]))}</p>
    <p>Minha resposta:</p>
    <div class="resposta"></div>
    <div class="resposta"></div>
    </div>

    <div class="cartao">
    <h2>2. Vamos testar!</h2>
    <p><b>Avisos sensoriais:</b></p>
    <ul>
    {"".join("<li>" + html.escape(x) + "</li>" for x in dados["sensoriais"])}
    </ul>
    <p><b>Materiais:</b></p>
    <ul>
    {"".join("<li>" + html.escape(x) + "</li>" for x in dados["materiais"])}
    </ul>
    <p><b>Etapas:</b></p>
    <ol>
    {"".join("<li>" + html.escape(x) + "</li>" for x in dados["passos"])}
    </ol>
    <p><b>Cuidados:</b> {html.escape(dados["cuidado"])}</p>
    </div>

    <div class="cartao">
    <h2>3. O que aconteceu?</h2>
    <ul>
    {"".join("<li>" + html.escape(x) + "</li>" for x in dados["observacoes"])}
    </ul>
    <p>Minhas observações:</p>
    <div class="resposta"></div>
    <div class="resposta"></div>
    <div class="resposta"></div>
    </div>

    <div class="cartao">
    <h2>4. O que descobrimos!</h2>
    <p>{html.escape(dados["explicacao_curta"] if nivel == "Ainda não leio" else dados["explicacao"])}</p>
    <p>O que eu aprendi?</p>
    <div class="resposta"></div>
    <div class="resposta"></div>
    <div class="resposta"></div>
    </div>
    </body>
    </html>
    """

    st.download_button(
        "🖨️ BAIXAR CARTÕES PARA IMPRIMIR",
        data=conteudo_impressao,
        file_name="cartoes_cientista_de_bolso.html",
        mime="text/html",
        use_container_width=True
    )

    st.caption(
        "Depois de baixar, abra o arquivo no navegador "
        "e use Ctrl + P para imprimir."
    )


# ==========================================
# PERGUNTAS NOVAS
# ==========================================

elif st.session_state.get("pergunta_nova"):

    st.info(
        "Sua pergunta foi recebida: "
        + st.session_state.pergunta_nova
    )

    st.warning(
        "A inteligência artificial ainda não está conectada. "
        "Nesta primeira versão, temos três investigações "
        "prontas para funcionar sem internet. "
        "Na próxima etapa vamos conectar a IA para criar "
        "investigações sobre outras perguntas."
    )


# ==========================================
# ÁREA DO PROFESSOR
# ==========================================

st.divider()

with st.expander("👩‍🏫 ÁREA DO PROFESSOR – Conheça a proposta"):

    st.markdown("""
    ### Objetivo pedagógico

    O Cientista de Bolso foi pensado para apoiar o ensino
    de Ciências por meio da investigação, da observação
    e da construção gradual do conhecimento.

    ### Por que quatro cartões?

    **1. Eu acho que...**

    Valoriza os conhecimentos prévios e as hipóteses
    da criança.

    **2. Vamos testar!**

    Incentiva a aprendizagem pela experiência prática.
    Os avisos sensoriais antecipam características
    da atividade.

    **3. O que aconteceu?**

    Desenvolve a observação, a atenção e a comunicação
    dos resultados.

    **4. O que descobrimos!**

    Apresenta uma explicação científica simples,
    respeitando o nível de leitura.

    ### Acessibilidade

    - Frases curtas e linguagem literal.
    - Uma etapa de cada vez.
    - Organização visual previsível.
    - Cores suaves.
    - Botões grandes.
    - Apoio de áudio.
    - Antecipação de estímulos sensoriais.

    ### Atenção: revisão do professor

    As experiências e explicações devem ser conferidas
    pelo professor antes da aplicação.

    A atividade deve ser adaptada às necessidades
    individuais de cada criança.

    A IA pode cometer erros. Ela não substitui
    a avaliação pedagógica nem a supervisão de um adulto.

    ### Funcionamento sem internet

    As três investigações prontas fazem parte do próprio
    código do aplicativo e não precisam de IA para funcionar.
    """)

st.divider()

st.caption(
    "Cientista de Bolso | Aprender Ciências investigando."
)
