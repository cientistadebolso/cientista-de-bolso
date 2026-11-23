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
