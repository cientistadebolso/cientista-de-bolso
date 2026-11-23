import streamlit as st
import streamlit.components.v1 as components
import html
import json
import os
import uuid
from datetime import date, datetime
from io import BytesIO

# =========================================================
# CIENTISTA DE BOLSO — versão ampliada
# Banco compartilhado opcional: Supabase
# =========================================================

st.set_page_config(page_title="Cientista de Bolso", page_icon="🔬", layout="centered")

st.markdown("""
<style>
.stApp {background-color:#F5F8F5;}
h1,h2,h3 {color:#315F52;}
p,label,li {color:#34463F;line-height:1.7;}
.stButton>button {min-height:48px;border-radius:14px;font-size:16px;
 border:1px solid #A9C9BA;background:#E5F0E9;color:#285747;}
.stTextInput input,.stTextArea textarea {font-size:17px;border-radius:12px;}
.stRadio label {font-size:16px;}
div[data-testid="stFileUploader"] {border:1px dashed #A9C9BA;border-radius:12px;}
.small-help {background:#EAF3ED;padding:10px 14px;border-radius:14px;margin:4px 0;}
</style>
""", unsafe_allow_html=True)

# ---------- Dados das investigações ----------
investigacoes = {
    "pao": {
        "titulo": "Por que o pão cresce?", "emoji": "🍞",
        "hipoteses": ["O fermento produz um gás.", "A farinha aumenta de tamanho.", "O pão cresce sozinho."],
        "materiais": ["Um copo transparente.", "Água morna, nunca quente.", "Fermento biológico seco.", "Um pouco de açúcar.", "Uma colher."],
        "passos": ["Coloque um pouco de água morna no copo.", "Acrescente uma pequena quantidade de fermento.", "Coloque uma pitada de açúcar.", "Misture devagar.", "Observe o que acontece durante alguns minutos."],
        "sensoriais": ["BARULHO: pode haver um pequeno som de bolhas.", "ÁGUA: pode molhar a colher e as mãos.", "CHEIRO: o fermento pode ter um cheiro próprio.", "TEXTURA: a mistura pode ficar um pouco grudenta.", "VISUAL: podem aparecer bolhas e espuma."],
        "observacoes": ["Apareceram bolhas?", "A mistura mudou de tamanho?", "Apareceu espuma?", "O que você observou?"],
        "explicacao": "O fermento biológico tem seres vivos muito pequenos chamados leveduras. Eles usam o açúcar e produzem um gás chamado gás carbônico. Na massa do pão, esse gás fica preso em pequenos espaços e faz a massa aumentar de tamanho. No forno, o pão assa.",
        "curta": "O fermento tem seres vivos muito pequenos. Eles produzem um gás. Esse gás forma bolhas na massa e faz o pão crescer.",
        "cuidado": "Faça a experiência com um adulto. Não beba a mistura. Não use água quente. A experiência demonstra a ação do fermento, mas não substitui o preparo do pão.",
        "apoio": ["bolhas", "espuma", "fermento", "cresceu", "gás"]
    },
    "poca": {
        "titulo": "Para onde vai a água da poça?", "emoji": "💧",
        "hipoteses": ["A água vira vapor e vai para o ar.", "A água entra no chão.", "A água desaparece completamente."],
        "materiais": ["Dois pratos iguais.", "Um pouco de água.", "Um local com sol.", "Um local com sombra."],
        "passos": ["Coloque a mesma quantidade de água nos dois pratos.", "Deixe um prato em um local com sol.", "Deixe o outro em um local com sombra.", "Observe os pratos depois de algum tempo.", "Compare a quantidade de água."],
        "sensoriais": ["BARULHO: não é esperada uma mudança de som.", "ÁGUA: pode molhar as mãos.", "CHEIRO: não é esperado cheiro diferente.", "TEXTURA: a água é líquida e pode molhar a pele.", "TEMPERATURA: o prato no sol pode ficar quente."],
        "observacoes": ["Qual prato perdeu mais água?", "A quantidade de água mudou?", "O sol fez diferença?", "O que você observou?"],
        "explicacao": "O calor ajuda a água líquida a passar para o estado gasoso. Esse processo se chama evaporação. A água continua existindo, mas fica misturada ao ar como vapor de água. O sol pode acelerar a evaporação.",
        "curta": "O calor faz parte da água passar para o ar em forma de vapor. Esse processo se chama evaporação. A água não desapareceu.",
        "cuidado": "Faça a experiência com um adulto. Não deixe os pratos em locais de passagem. Não olhe diretamente para o sol. Não use água quente.",
        "apoio": ["água", "sol", "sombra", "evaporou", "vapor"]
    },
    "coracao": {
        "titulo": "Por que o coração acelera quando corremos?", "emoji": "❤️",
        "hipoteses": ["O coração bate mais rápido para levar sangue pelo corpo.", "O coração fica cansado e para de funcionar.", "O coração bate mais rápido porque fazemos barulho."],
        "materiais": ["Um relógio ou cronômetro.", "Um local seguro para ficar em pé.", "A ajuda de um adulto."],
        "passos": ["Sente-se e descanse por alguns minutos.", "Com ajuda de um adulto, perceba os batimentos no pulso.", "Conte os batimentos durante 30 segundos, se conseguir.", "Marche devagar no mesmo lugar por 30 segundos.", "Pare, descanse e perceba novamente os batimentos."],
        "sensoriais": ["BARULHO: não é esperado barulho especial.", "MOVIMENTO: você vai movimentar as pernas.", "SUOR: o corpo pode ficar um pouco suado.", "TEMPERATURA: o corpo pode ficar mais quente.", "TOQUE: pode ser necessário tocar o pulso."],
        "observacoes": ["O coração bateu mais rápido depois do movimento?", "Sua respiração mudou?", "O que aconteceu depois do descanso?", "O que você observou?"],
        "explicacao": "Quando fazemos atividade física, os músculos precisam de mais oxigênio e nutrientes. O coração bombeia o sangue mais rapidamente para ajudar a levar essas substâncias pelo corpo. Depois do descanso, os batimentos costumam diminuir novamente.",
        "curta": "Quando corremos, os músculos precisam de mais oxigênio. O coração bate mais rápido para ajudar a levar sangue aos músculos.",
        "cuidado": "Esta atividade é opcional. Não é necessário correr. Faça apenas movimentos confortáveis, com supervisão de um adulto. Pare se sentir dor, tontura, falta de ar fora do habitual ou desconforto. Não force a contagem dos batimentos.",
        "apoio": ["coração", "rápido", "sangue", "respiração", "descanso"]
    }
}

def get_supabase():
    """Conecta se os segredos do Supabase estiverem configurados."""
    try:
        from supabase import create_client
        url = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL"))
        key = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY"))
        if url and key:
            return create_client(url, key)
    except Exception:
        return None
    return None

supabase = get_supabase()

def save_submission(record):
    if supabase:
        try:
            supabase.table("respostas_alunos").upsert(record, on_conflict="id").execute()
            return True
        except Exception as exc:
            st.error("Não foi possível salvar no banco compartilhado. Confira a configuração do Supabase.")
            st.caption(str(exc))
            return False
    st.session_state.setdefault("envios_locais", [])
    st.session_state.envios_locais.append(record)
    return True

def update_record(record_id, changes):
    if supabase:
        try:
            supabase.table("respostas_alunos").update(changes).eq("id", record_id).execute()
            return True
        except Exception:
            return False
    for item in st.session_state.get("envios_locais", []):
        if item.get("id") == record_id:
            item.update(changes)
            return True
    return False

def load_records():
    if supabase:
        try:
            result = supabase.table("respostas_alunos").select("*").order("atualizado_em", desc=True).execute()
            return result.data or []
        except Exception:
            st.warning("Não foi possível consultar o banco compartilhado.")
    return st.session_state.get("envios_locais", [])

def speak(text):
    safe = json.dumps(text, ensure_ascii=False)
    components.html(f"""
    <button onclick='window.speechSynthesis.cancel();let u=new SpeechSynthesisUtterance({safe});
    u.lang="pt-BR";u.rate=0.88;window.speechSynthesis.speak(u);'
    style="background:#E5F0E9;color:#285747;border:1px solid #A9C9BA;
    border-radius:12px;padding:10px 16px;font-size:16px;width:100%;cursor:pointer;">
    🔊 Ouvir enunciado</button>""", height=52)

def audio_bytes(upload):
    if upload is None:
        return None
    return upload.getvalue()

# ---------- Cabeçalho ----------
st.title("🔬 Cientista de Bolso")
st.markdown("Toda pergunta pode virar uma descoberta!")
st.markdown("Aqui, vamos observar, pensar e investigar uma coisa de cada vez.")
st.divider()

# ---------- Navegação ----------
modo = st.sidebar.radio("Acesso", ["👧 Área do aluno", "👩‍🏫 Área do professor"])

if modo == "👧 Área do aluno":
    st.subheader("📖 Como está a leitura?")
    nivel = st.radio("O professor escolhe o nível da criança:",
                     ["Ainda não leio", "Estou começando a ler", "Já leio bem"],
                     key="nivel_leitura")

    with st.container(border=True):
        st.subheader("🧒 Antes de começar")
        c1, c2 = st.columns(2)
        with c1:
            nome = st.text_input("Nome completo *", key="aluno_nome")
        with c2:
            turma = st.text_input("Turma *", key="aluno_turma")
        data_atividade = st.date_input("Data", value=date.today(), key="data_atividade")

    st.subheader("🔎 O que você quer descobrir?")
    opcoes = {"Por que o pão cresce?": "pao",
              "Para onde vai a água da poça?": "poca",
              "Por que o coração acelera quando corremos?": "coracao"}
    escolha = st.selectbox("Escolha uma pergunta:", ["Escolha uma pergunta..."] + list(opcoes))
    pergunta_personalizada = st.text_input("Ou escreva sua própria pergunta:")
    chave = opcoes.get(escolha)

    if pergunta_personalizada.strip():
        texto_pergunta = pergunta_personalizada.strip()
        p = texto_pergunta.lower()
        if "pão" in p or "pao" in p:
            chave = "pao"
        elif "poça" in p or "poca" in p or "água" in p or "agua" in p:
            chave = "poca"
        elif "coração" in p or "coracao" in p:
            chave = "coracao"
        else:
            chave = None
    else:
        texto_pergunta = escolha if escolha != "Escolha uma pergunta..." else ""

    if st.button("🔬 COMEÇAR A INVESTIGAR", use_container_width=True):
        if not nome.strip() or not turma.strip():
            st.error("Preencha seu nome completo e sua turma antes de começar.")
        elif not texto_pergunta:
            st.warning("Escolha ou escreva uma pergunta primeiro.")
        elif not chave:
            st.warning("Esta pergunta ainda não tem uma investigação pronta. Por enquanto, escolha uma das três perguntas disponíveis.")
        else:
            st.session_state.atividade_id = str(uuid.uuid4())
            st.session_state.investigacao = chave
            st.session_state.etapa = 0
            st.session_state.respostas = {}
            st.session_state.reacoes = {}
            st.session_state.iniciada_em = datetime.now().isoformat(timespec="seconds")
            st.session_state.concluida = False
            st.rerun()

    if st.session_state.get("investigacao"):
        dados = investigacoes[st.session_state.investigacao]
        etapa = st.session_state.get("etapa", 0)
        st.divider()
        st.subheader(f'{dados["emoji"]} {dados["titulo"]}')
        st.progress((etapa + 1) / 4, text=f"Etapa {etapa + 1} de 4")

        respostas = st.session_state.setdefault("respostas", {})
        reacoes = st.session_state.setdefault("reacoes", {})
        labels_reacao = ["😍 Achei muito legal", "🤔 Fiquei curioso", "🆘 Preciso de ajuda"]

        if etapa == 0:
            st.markdown("## 1. 💭 Eu acho que...")
            enunciado = "O que você acha que vai acontecer?"
            st.write(enunciado); speak(enunciado)
            respostas["hipotese"] = st.radio("Escolha sua ideia:", dados["hipoteses"], key="resp_hipotese")
        elif etapa == 1:
            st.markdown("## 2. 🧪 Vamos testar!")
            enunciado = "Antes de começar, vamos conhecer a experiência."
            st.write(enunciado); speak(enunciado)
            st.markdown("### Como será a experiência?")
            for aviso in dados["sensoriais"]:
                st.info(aviso)
            st.warning(dados["cuidado"])
            st.markdown("### Materiais")
            for material in dados["materiais"]:
                st.write("☐ " + material)
            st.markdown("### Passo a passo")
            for i, passo in enumerate(dados["passos"], 1):
                st.write(f"**{i}.** {passo}")
        elif etapa == 2:
            st.markdown("## 3. 👀 O que aconteceu?")
            for pergunta in dados["observacoes"]:
                st.write("• " + pergunta)
                speak(pergunta)
            respostas["observacao"] = st.text_area("Minhas observações:",
                placeholder="Eu observei que...", height=130, key="texto_observacao")
            st.markdown("**Palavras que podem ajudar:**")
            apoio = st.session_state.get("apoio_palavras", "")
            cols = st.columns(len(dados["apoio"]))
            for i, palavra in enumerate(dados["apoio"]):
                with cols[i]:
                    if st.button(palavra, key=f"apoio_{etapa}_{i}"):
                        st.session_state.apoio_palavras = (apoio + " " + palavra).strip()
                        st.session_state.texto_observacao = (st.session_state.get("texto_observacao", "") + " " + palavra).strip()
                        st.rerun()
            foto = st.file_uploader("📷 Envie uma foto ou desenho do experimento",
                                    type=["png", "jpg", "jpeg"], key="foto_experimento")
            if foto:
                st.image(foto, caption="Registro visual do experimento", use_container_width=True)
                st.session_state.foto_nome = foto.name
                st.session_state.foto_bytes = foto.getvalue()
            audio = st.audio_input("🎙️ Grave um áudio contando o que observou", key="audio_observacao")
            if audio:
                st.audio(audio)
                st.session_state.audio_bytes = audio.getvalue()
        else:
            st.markdown("## 4. 💡 O que descobrimos!")
            explicacao = dados["curta"] if nivel == "Ainda não leio" else dados["explicacao"]
            st.success(explicacao)
            speak("O que descobrimos? " + explicacao)
            respostas["descoberta"] = st.text_area("O que você aprendeu?",
                placeholder="Eu descobri que...", height=110, key="texto_descoberta")
            st.markdown("### Como foi sua aprendizagem?")
            enunciado = "Você entendeu por que isso acontece?"
            st.write(enunciado); speak(enunciado)
            respostas["autoavaliacao"] = st.radio("Escolha uma opção:",
                ["Sim", "Mais ou menos", "Ainda tenho dúvidas"], key="autoavaliacao")

        st.divider()
        st.caption("Como você se sentiu nesta etapa?")
        reacoes[etapa] = st.radio("Escolha uma reação:", labels_reacao,
                                  horizontal=False, key=f"reacao_{etapa}",
                                  label_visibility="collapsed")
        if reacoes[etapa] == "🆘 Preciso de ajuda":
            st.warning("Seu professor poderá ver que você precisa de ajuda.")

        c1, c2 = st.columns(2)
        with c1:
            if etapa > 0 and st.button("← VOLTAR", use_container_width=True):
                st.session_state.etapa -= 1
                st.rerun()
        with c2:
            if etapa < 3 and st.button("PRÓXIMO →", use_container_width=True):
                st.session_state.etapa += 1
                st.rerun()

        if etapa == 3:
            st.divider()
            if st.button("🏁 CONCLUIR E ENVIAR RESPOSTAS", use_container_width=True, type="primary"):
                if not st.session_state.get("aluno_nome", "").strip() or not st.session_state.get("aluno_turma", "").strip():
                    st.error("Precisamos do nome completo e da turma para enviar.")
                else:
                    registro = {
                        "id": st.session_state.atividade_id,
                        "nome": st.session_state.aluno_nome.strip(),
                        "turma": st.session_state.aluno_turma.strip(),
                        "data_atividade": str(st.session_state.data_atividade),
                        "investigacao": st.session_state.investigacao,
                        "titulo": dados["titulo"],
                        "nivel_leitura": nivel,
                        "respostas": respostas,
                        "reacoes": reacoes,
                        "foto_nome": st.session_state.get("foto_nome"),
                        "audio_presente": bool(st.session_state.get("audio_bytes")),
                        "status": "Concluída",
                        "etapa_atual": 4,
                        "iniciada_em": st.session_state.get("iniciada_em"),
                        "atualizado_em": datetime.now().isoformat(timespec="seconds"),
                        "feedback_professor": "",
                        "missao_extra": ""
                    }
                    if save_submission(registro):
                        st.session_state.registro_final = registro
                        st.session_state.concluida = True
                        st.success("Atividade enviada! Parabéns, Pequeno Cientista!")
                        st.balloons()

        if st.session_state.get("concluida") and st.session_state.get("registro_final"):
            registro = st.session_state.registro_final
            st.divider()
            st.title("🏅 Pequeno Cientista da Fermentação")
            st.success("Sua investigação foi concluída. Veja seu resumo!")
            resumo = {
                "Cientista": registro["nome"], "Turma": registro["turma"],
                "Data": registro["data_atividade"], "Investigação": registro["titulo"],
                "Respostas": registro["respostas"], "Reações": registro["reacoes"],
                "Autoavaliação": registro["respostas"].get("autoavaliacao", "")
            }
            st.json(resumo)
            texto = "CIENTISTA DE BOLSO\nPEQUENO CIENTISTA DA FERMENTAÇÃO\n\n" + json.dumps(resumo, ensure_ascii=False, indent=2)
            st.download_button("⬇️ Baixar resumo", data=texto.encode("utf-8"),
                               file_name="resumo_pequeno_cientista.txt",
                               mime="text/plain", use_container_width=True)
            st.caption("Este resumo em texto pode ser salvo ou enviado ao professor. O PDF/imagem pode ser acrescentado em uma próxima versão.")

      # Mensagens do professor para o aluno
        if st.session_state.get("atividade_id") and supabase:
            try:
                atual = supabase.table("respostas_alunos").select("*").eq("id", st.session_state.atividade_id).limit(1).execute()
                if atual.data:
                    item = atual.data[0]
                    if item.get("feedback_professor"):
                        st.info("💬 Retorno do professor: " + item["feedback_professor"])
                    if item.get("missao_extra"):
                        st.success("🚀 Sua missão extra: " + item["missao_extra"])
            except Exception:
                pass
        except Exception:
            pass

elif modo == "👩‍🏫 Área do professor":
    st.title("👩‍🏫 Painel do professor")
    st.write("Acompanhe as atividades enviadas e identifique quem sinalizou que precisa de ajuda.")
    senha_configurada = st.secrets.get("SENHA_PROFESSOR", os.getenv("SENHA_PROFESSOR", ""))
    if not senha_configurada:
        st.warning("Configure SENHA_PROFESSOR nos Secrets do Streamlit antes de usar este painel com alunos.")
        senha = st.text_input("Senha do professor", type="password")
        autenticado = False
    else:
        senha = st.text_input("Senha do professor", type="password")
        autenticado = senha == senha_configurada
    if autenticado:
        if not supabase:
            st.warning("Modo de demonstração: sem Supabase, só aparecem registros desta sessão. Para acompanhar vários alunos em tempo real, configure o banco compartilhado.")
        registros = load_records()
        if not registros:
            st.info("Ainda não há atividades enviadas.")
        else:
            st.metric("Atividades recebidas", len(registros))
            for reg in registros:
                reacoes = reg.get("reacoes") or {}
                precisa = any("Preciso de ajuda" in str(v) for v in reacoes.values())
                titulo = f'{"🆘 " if precisa else ""}{reg.get("nome","Aluno")} — {reg.get("turma","")} — {reg.get("status","Em andamento")}'
                with st.expander(titulo):
                    st.write("**Investigação:**", reg.get("titulo", ""))
                    st.write("**Data:**", reg.get("data_atividade", ""))
                    st.write("**Etapa registrada:**", reg.get("etapa_atual", "—"))
                    st.write("**Nível de leitura:**", reg.get("nivel_leitura", ""))
                    if precisa:
                        st.error("Este aluno marcou 'Preciso de ajuda' em pelo menos uma etapa.")
                    st.markdown("**Respostas**")
                    st.json(reg.get("respostas", {}))
                    st.markdown("**Reações**")
                    st.json(reacoes)
                    st.write("Foto anexada:", reg.get("foto_nome") or "Não")
                    st.write("Áudio de observação:", "Sim" if reg.get("audio_presente") else "Não")
                    feedback = st.text_area("Enviar retorno em texto", key=f"feedback_{reg.get('id')}")
                    missao = st.text_area("Liberar missão extra", key=f"missao_{reg.get('id')}",
                                          placeholder="Ex.: O que aconteceria se colocássemos menos açúcar?")
                    if st.button("Enviar retorno e missão", key=f"enviar_{reg.get('id')}"):
                        if update_record(reg.get("id"), {
                            "feedback_professor": feedback,
                            "missao_extra": missao,
                            "atualizado_em": datetime.now().isoformat(timespec="seconds")
                        }):
                            st.success("Retorno atualizado.")
                            st.rerun()
            st.caption("Use o botão de atualizar do navegador para consultar novos envios. Atualização automática em tempo real e arquivos de mídia no armazenamento compartilhado exigem configuração adicional.")
    elif senha:
        st.error("Senha incorreta.")

st.divider()
st.caption("Cientista de Bolso | Aprender Ciências investigando.")
