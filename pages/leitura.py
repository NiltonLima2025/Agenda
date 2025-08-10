import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Agenda de Eventos",
    page_icon= "📌",
    layout="centered"
)

# CSS para dar margem superior e ajustar tamanho da imagem
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

st.subheader("Consulta de Eventos")

if "eventos" not in st.session_state or st.session_state.eventos.empty:
    st.info("Nenhum evento cadastrado.")
else:
    eventos_filtrados = st.session_state.eventos.copy()  # Remove os filtros, usa todos os eventos

    # ---------------- ABAS ----------------
    abas = st.tabs(["📅 Diária", "📆 Semanal", "🗓️ Mensal"])

    # Diária
    with abas[0]:
        hoje = st.date_input("Escolha o dia", datetime.now().date(), key="dia", format="DD/MM/YYYY")
        eventos_dia = eventos_filtrados[eventos_filtrados["Data"] == hoje]
        st.subheader(f"Eventos do dia {hoje.strftime('%d/%m/%Y')}")
        st.table(eventos_dia.sort_values(by="Hora"))

    # Semanal
    with abas[1]:
        ref_semana = st.date_input("Data de referência da semana", datetime.now().date(), key="semana", format="DD/MM/YYYY")
        inicio_semana = ref_semana - timedelta(days=ref_semana.weekday())
        fim_semana = inicio_semana + timedelta(days=6)
        eventos_semana = eventos_filtrados[
            (eventos_filtrados["Data"] >= inicio_semana) &
            (eventos_filtrados["Data"] <= fim_semana)
        ]
        st.subheader(f"Eventos de {inicio_semana.strftime('%d/%m/%Y')} a {fim_semana.strftime('%d/%m/%Y')}")
        st.table(eventos_semana.sort_values(by=["Data", "Hora"]))

    # Mensal
    with abas[2]:
        mes_ref = st.date_input("Data de referência do mês", datetime.now().date(), key="mes", format="DD/MM/YYYY")
        inicio_mes = mes_ref.replace(day=1)
        if inicio_mes.month == 12:
            fim_mes = inicio_mes.replace(year=inicio_mes.year+1, month=1, day=1) - timedelta(days=1)
        else:
            fim_mes = inicio_mes.replace(month=inicio_mes.month+1, day=1) - timedelta(days=1)
        eventos_mes = eventos_filtrados[
            (eventos_filtrados["Data"] >= inicio_mes) &
            (eventos_filtrados["Data"] <= fim_mes)
        ]
        st.subheader(f"Eventos de {inicio_mes.strftime('%m/%Y')}")
        st.table(eventos_mes.sort_values(by=["Data", "Hora"]))
