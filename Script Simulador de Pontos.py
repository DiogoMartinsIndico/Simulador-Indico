import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Dashboard Razonetes", layout="wide")

# Estilo customizado
st.markdown("""
    <style>
    <!-- @import url('https://fonts.googleapis.com/css2?family=General+Sans:wght@400;600;700&display=swap'); -->
    body, .stApp {
        background-color: #12141d;
        color: white;
        font-family: 'General Sans', sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'General Sans', sans-serif;
        font-weight: 700;
        color: white;
    }
    .css-1v0mbdj, .css-18e3th9, .block-container {
        background-color: #12141d !important;
    }
    .stTextInput > div > input,
    .stNumberInput input,
    .stSelectbox select,
    .stSlider > div {
        background-color: #1e2130;
        color: white;
    }
    .stDataFrame {
        background-color: #1e2130 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Funções auxiliares
def parse_input(input_str):
    try:
        return float(input_str.replace(".", "").replace(",", "."))
    except:
        return 0.0

def format_number_br(value):
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- Simulador ---
st.markdown("<h1 style='text-align: center;'>Simulador de Pontos Fidelidade</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px; margin-top: -10px;'>Ajuste os parâmetros à esquerda para simular o impacto dos pontos na performance da loja.</p>", unsafe_allow_html=True)
st.markdown("<hr style='margin-top:20px;margin-bottom:20px;'>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    with st.expander("Editar Parâmetros da Simulação", expanded=True):
        with st.container():
            col_in1, col_in2 = st.columns(2)

            with col_in1:
                vendas_loja_input = st.text_input(
                    "Faturamento Total (R$)",
                    value="0,00",
                    help="Total de vendas brutas da loja no período analisado. Use ponto para milhar e vírgula para decimal."
                )
                vendas_loja = parse_input(vendas_loja_input)

            with col_in2:
                valor_produto_input = st.text_input(
                    "Preço Unitário",
                    value="0,00",
                    help="Preço médio do produto. Use ponto para milhar e vírgula para decimal."
                )
                valor_produto = parse_input(valor_produto_input)

            col_in3, col_in4 = st.columns(2)

            with col_in3:
                pontos_necessarios_input = st.text_input(
                    "Pontos de Corte",
                    value="0",
                    help="Quantidade de pontos exigida para trocar por um produto."
                )
                pontos_necessarios = int(parse_input(pontos_necessarios_input))

            with col_in4:
                pontos_por_real_input = st.text_input(
                    "Pontos por R$1",
                    value="0",
                    help="Número de pontos dados a cada R$1 em vendas."
                )
                pontos_por_real = parse_input(pontos_por_real_input)

        # Premissas
        pct_vendas_identificadas = 0.35
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("Premissas")
        st.markdown(""" 
            <div style='font-size: 14px;'>
                <ul>
                  <li><strong>Vendas identificadas:</strong> <span style='color: #2f0'>35%</span></li>
                  <li><strong>Valor do Ponto provisionado:</strong> <span style='color: #2f0'>5%</span></li>
                  <li><strong>Pontos da loja resgatados:</strong> <span style='color: #2f0'>25%</span></li>
                  <li><strong>Pontos emitidos resgatados na própria loja:</strong> <span style='color: #2f0'>65%</span></li>
                  <li><strong>QTD de pontos resgatados de outras lojas:</strong> <span style='color: #2f0'>300.000</span></li>
                  <li><strong>Lift:</strong> <span style='color: #2f0'>2.50%</span></li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

# --- Cálculos
valor_ponto_provisionado = 0.05
pct_resgate_loja = 0.25
pct_resgatado_proprio = 0.65
pct_resgatado_fora = 1 - pct_resgatado_proprio
lift = 0.0250
breakage = 1 - pct_resgate_loja

reais_identificados = vendas_loja * pct_vendas_identificadas
pontos_dados = reais_identificados * pontos_por_real
valor_pontos_provisionados = reais_identificados * valor_ponto_provisionado
pontos_resgatados_loja = pontos_dados * pct_resgate_loja
valor_por_ponto = valor_produto / pontos_necessarios if pontos_necessarios else 0

pontos_outras_lojas_resgatados_na_loja = 300_000.0
carga_tributaria = 0.095

total_resgatado_propria_loja = pontos_outras_lojas_resgatados_na_loja + (pontos_resgatados_loja * pct_resgatado_proprio)
valor_pontos_dados_balde = reais_identificados * valor_por_ponto
pontos_proprios_resgatados = pontos_resgatados_loja * pct_resgatado_proprio
valor_pontos_resgatados_balde = pontos_proprios_resgatados * valor_por_ponto
saldo_1 = valor_pontos_dados_balde - valor_pontos_resgatados_balde

reembolso_outras_lojas = pontos_outras_lojas_resgatados_na_loja * valor_por_ponto
saldo_2 = saldo_1 + reembolso_outras_lojas

pontos_loja_resgatados_fora = pontos_resgatados_loja * pct_resgatado_fora
custo_resgate_fora = pontos_loja_resgatados_fora * valor_por_ponto

saldo_3 = saldo_2 - custo_resgate_fora
saldo_4 = saldo_3 * (1 - breakage)

net_loja = reembolso_outras_lojas - custo_resgate_fora

valor_pontos_provisionados_resgatados = pontos_resgatados_loja * valor_por_ponto
ganho_tributario = valor_pontos_provisionados_resgatados * carga_tributaria

lift_aplicado = lift * reais_identificados
ganho_programa = net_loja + lift_aplicado + ganho_tributario
ganho_pct_final = ganho_programa / vendas_loja if vendas_loja else 0

# --- Tabela Resultado
df_simulador = pd.DataFrame({
    "Parâmetro": [
        "Ganho % final do programa",
        "Ganho do programa",
        "Lift Aplicado",
        "Ganho tributário oriundo do provisionamento"
    ],
    "Valor": [
        ganho_pct_final * 100,
        ganho_programa,
        lift_aplicado,
        ganho_tributario
    ]
})
df_simulador["Valor"] = df_simulador["Valor"].apply(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

with col2:
    with st.container():
        st.markdown("<h3 style='text-align: center;'>Detalhamento Completo</h3>", unsafe_allow_html=True)
        st.dataframe(df_simulador, use_container_width=True, hide_index=True)
