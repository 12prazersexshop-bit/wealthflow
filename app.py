import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ===============================
# CONFIGURAÇÃO MOBILE-FIRST
# ===============================
st.set_page_config(
    page_title="WealthFlow",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===============================
# ESTILO MOBILE
# ===============================
st.markdown("""
<style>
body {
    background-color: #f7f9fc;
}
h1, h2, h3 {
    text-align: center;
}
.block-container {
    padding-top: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# TÍTULO
# ===============================
st.title("💰 WealthFlow")
st.subheader("Planejador de Riqueza • Inspirado em Pai Rico, Pai Pobre")

st.divider()

# ===============================
# CONFIGURAÇÕES (MOBILE FRIENDLY)
# ===============================
with st.expander("⚙️ Configurações Financeiras", expanded=True):
    nome_usuario = st.text_input("Seu nome")
    renda_mensal = st.number_input("Renda mensal (R$)", min_value=0.0, value=5000.0)
    despesas_mensais = st.number_input("Despesas mensais (R$)", min_value=0.0, value=3000.0)
    ativos_iniciais = st.number_input("Ativos iniciais (R$)", min_value=0.0, value=10000.0)
    taxa_retorno_anual = st.slider(
        "Retorno anual esperado (%)",
        min_value=0.0,
        max_value=30.0,
        value=8.0,
        step=0.5
    ) / 100
    anos_projetados = st.slider("Anos de projeção", 1, 40, 15)

# ===============================
# EDUCAÇÃO FINANCEIRA
# ===============================
with st.expander("📘 Princípios do Pai Rico"):
    st.markdown("""
    - **Ativos** colocam dinheiro no seu bolso  
    - **Passivos** tiram dinheiro do seu bolso  
    - Renda passiva compra liberdade  
    - Educação financeira é o ativo nº 1
    """)

# ===============================
# ATIVOS E PASSIVOS (STACK MOBILE)
# ===============================
st.header("📊 Seus Ativos e Passivos")

ativos_texto = st.text_area(
    "Ativos (Nome: Valor)",
    "Ações: 5000\nImóveis: 20000\nPoupança: 3000",
    height=160
)

passivos_texto = st.text_area(
    "Passivos (Nome: Valor)",
    "Empréstimo: 15000\nCartão de crédito: 2000",
    height=160
)

def parse(texto):
    dados = {}
    for linha in texto.split("\n"):
        if ":" in linha:
            k, v = linha.split(":", 1)
            try:
                dados[k.strip()] = float(v.strip())
            except:
                pass
    return dados

ativos = parse(ativos_texto)
passivos = parse(passivos_texto)

total_ativos = sum(ativos.values()) + ativos_iniciais
total_passivos = sum(passivos.values())
patrimonio = total_ativos - total_passivos

st.success(f"💼 Patrimônio atual: **R$ {patrimonio:,.2f}**")

# ===============================
# FLUXO DE CAIXA
# ===============================
fluxo = renda_mensal - despesas_mensais

if fluxo >= 0:
    st.info(f"💵 Fluxo de caixa mensal positivo: **R$ {fluxo:,.2f}**")
else:
    st.warning(f"⚠️ Fluxo de caixa negativo: **R$ {fluxo:,.2f}**")

# ===============================
# GRÁFICO ATIVOS VS PASSIVOS
# ===============================
if total_ativos > 0 or total_passivos > 0:
    fig_pie = px.pie(
        values=[total_ativos, total_passivos],
        names=["Ativos", "Passivos"],
        hole=0.45
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ===============================
# PROJEÇÃO FINANCEIRA
# ===============================
st.header("📈 Projeção de Patrimônio")

meses = np.arange(0, anos_projetados * 12 + 1)
taxa_mensal = taxa_retorno_anual / 12
pat = patrimonio
hist = []

for m in meses:
    if m > 0:
        pat = pat * (1 + taxa_mensal) + fluxo
    hist.append(pat)

df = pd.DataFrame({
    "Ano": meses / 12,
    "Patrimônio": hist
})

fig_line = px.line(
    df,
    x="Ano",
    y="Patrimônio",
)
st.plotly_chart(fig_line, use_container_width=True)

# ===============================
# INDEPENDÊNCIA FINANCEIRA
# ===============================
st.header("🏁 Independência Financeira")

meta = despesas_mensais * 12 / 0.04
st.write(f"🎯 Meta (Regra dos 4%): **R$ {meta:,.2f}**")

if patrimonio >= meta:
    st.balloons()
    st.success("🎉 Você já atingiu a independência financeira!")
else:
    if fluxo <= 0 or taxa_retorno_anual <= 0:
        st.warning("Com os dados atuais, a meta não será atingida.")
    else:
        aporte_anual = fluxo * 12
        anos = np.log((meta * taxa_retorno_anual + aporte_anual) /
                      (patrimonio * taxa_retorno_anual + aporte_anual)) / np.log(1 + taxa_retorno_anual)
        st.info(f"⏳ Tempo estimado: **{anos:.1f} anos**")

# ===============================
# FOOTER
# ===============================
st.caption("WealthFlow • Versão Mobile Comercial • © 2026")
