import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Agenda de Eventos",
    page_icon= "📌",
    layout="centered"
)

st.markdown(
    """
    <style>
    img {
        margin-top: 30px !important;
        width: 100% !important;
        height: auto !important;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Imagem no topo
st.image("img_cnj.png", use_container_width=True)

st.markdown("<h3 style='text-align: center;'>Gabinete Conselheiro Rodrigo Badaró</h3>", unsafe_allow_html=True)

st.divider()

# Formulário abaixo da imagem
st.subheader("Inserir Eventos")
with st.form("form_evento"):
    data = st.date_input("Data do evento", format="DD/MM/YYYY", key="data_input")
    hora = st.time_input("Hora do evento", step=60, key="hora_input")
    evento = st.text_input("Descrição do evento")
    adicionar = st.form_submit_button("Adicionar evento")

    if adicionar and evento.strip():
        novo_evento = pd.DataFrame({
            "Data": [data],
            "Hora": [hora.strftime("%H:%M")],
            "Evento": [evento]
        })
        if "eventos" not in st.session_state:
            st.session_state.eventos = pd.DataFrame(columns=["Data", "Hora", "Evento"])
        st.session_state.eventos = pd.concat([st.session_state.eventos, novo_evento], ignore_index=True)
        st.success("✅ Evento adicionado!")

# Seção de edição de eventos
st.subheader("Editar Evento")

if "eventos" not in st.session_state or len(st.session_state.eventos) == 0:
    st.info("Nenhum evento para editar.")
else:
    df_eventos = st.session_state.eventos.copy()
    df_eventos['DataHora'] = pd.to_datetime(df_eventos['Data'].astype(str) + ' ' + df_eventos['Hora'])
    df_eventos = df_eventos.sort_values('DataHora').reset_index()
    df_eventos = df_eventos.reset_index(drop=True)

    indice_evento = st.selectbox(
        "Selecione o evento",
        options=df_eventos.index,
        format_func=lambda i: f"{df_eventos.at[i,'Data'].strftime('%d/%m/%Y')} - {df_eventos.at[i,'Hora']} - {df_eventos.at[i,'Evento']}"
    )

    data_edit = st.date_input(
        "Nova data",
        value=df_eventos.at[indice_evento, "Data"],
        key="edit_data",
        format="DD/MM/YYYY"
    )
    hora_edit = st.time_input(
        "Nova hora",
        value=datetime.strptime(df_eventos.at[indice_evento, "Hora"], "%H:%M").time(),
        key="edit_hora",
        step=60
    )
    evento_edit = st.text_input(
        "Nova descrição",
        value=df_eventos.at[indice_evento, "Evento"],
        key="edit_evento"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Salvar alterações"):
            original_idx = df_eventos.at[indice_evento, 'index']
            st.session_state.eventos.at[original_idx, "Data"] = data_edit
            st.session_state.eventos.at[original_idx, "Hora"] = hora_edit.strftime("%H:%M")
            st.session_state.eventos.at[original_idx, "Evento"] = evento_edit
            st.success("Evento atualizado!")

    with col2:
        if st.button("🗑️ Excluir evento"):
            original_idx = df_eventos.at[indice_evento, 'index']
            st.session_state.eventos = st.session_state.eventos.drop(original_idx).reset_index(drop=True)
            st.warning("Evento excluído!")
