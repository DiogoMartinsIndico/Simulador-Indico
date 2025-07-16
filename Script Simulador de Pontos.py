import streamlit as st
import pandas as pd
from io import BytesIO

# --- CONFIGURAÇÃO DA PÁGINA E ESTILO CUSTOMIZADO ---
st.set_page_config(page_title="Dashboard Razonetes", layout="wide")

# --- ESTILO CUSTOMIZADO (VERSÃO FINAL E CORRIGIDA) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=General+Sans:wght@400;600;700&display=swap' );

        /* FUNDO E FONTE GERAL */
        .stApp, .main {
            background-color: #12141d !important;
            font-family: 'General Sans', sans-serif;
        }

        /* TEXTOS */
        body, p, div, span, li {
            color: #FAFAFA !important;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #FAFAFA !important;
            font-weight: 700;
        }
        label {
             color: #A0A0A0 !important;
        }

        /* CONTAINERS E INPUTS */
        .st-emotion-cache-1r4qj8v {
            background-color: #1e2130 !important;
        }
        .stTextInput input, .stNumberInput input {
            background-color: #2a2f45 !important;
            color: #FAFAFA !important;
            border: 1px solid #4a5474 !important;
            border-radius: 5px;
        }
        
        /* ESTILO ESPECÍFICO E FORÇADO PARA TABELAS (st.table) */
        table {
            width: 100%;
            background-color: #1e2130 !important; /* Fundo da tabela */
            color: #FAFAFA !important;
            border-radius: 10px;
            overflow: hidden; /* Garante que o border-radius aplique nos cantos */
        }
        th { /* Cabeçalho da tabela */
            background-color: #2a2f45 !important;
            color: #FAFAFA !important;
            font-weight: bold;
            text-align: left;
            padding: 12px !important;
        }
        td { /* Células da tabela */
            background-color: #1e2130 !important;
            color: #FAFAFA !important;
            padding: 12px !important;
            border-top: 1px solid #2a2f45; /* Linha separadora entre as linhas */
        }
        
        hr {
            border-color: #4a5474 !important;
        }
    </style>
""", unsafe_allow_html=True)


# --- Funções auxiliares ---
def parse_input(input_str):
    try:
        return float(str(input_str).replace(".", "").replace(",", "."))
    except (ValueError, TypeError):
        return 0.0

def format_number_br(value):
    if not isinstance(value, (int, float)):
        return "0,00"
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- Layout do Simulador ---
st.markdown("<h1 style='text-align: center;'>Simulador de Pontos Fidelidade</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px; margin-top: -10px;'>Ajuste os parâmetros à esquerda para simular o impacto dos pontos na performance da loja.</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    with st.expander("Editar Parâmetros da Simulação", expanded=True):
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            vendas_loja_input = st.text_input(
                "Faturamento Total (R$)", value="0,00",
                help="Total de vendas brutas da loja. Use ponto para milhar e vírgula paraCom certeza. Sem mais delongas, aqui está o script completo e final.

Ele contém todas as correções, incluindo o CSS aprimorado e a troca do `st.dataframe` pelo `st.table` para garantir que a tabela também fique com o fundo escuro.

Copie, cole e execute.

```python
import streamlit as st
import pandas as pd
from io import BytesIO

# --- CONFIGURAÇÃO DA PÁGINA E ESTILO CUSTOMIZADO ---
# st.set_page_config deve ser o primeiro comando do Streamlit a ser executado.
st.set_page_config(page_title="Dashboard Razonetes", layout="wide")

# --- ESTILO CUSTOMIZADO (VERSÃO FINAL) ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=General+Sans:wght@400;600;700&display=swap' );

        /* FUNDO E FONTE GERAL */
        .stApp, .main {
            background-color: #12141d !important;
            font-family: 'General Sans', sans-serif;
        }

        /* TEXTOS */
        body, p, div, span, li {
            color: #FAFAFA !important;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #FAFAFA !important;
            font-weight: 700;
        }
        label {
             color: #A0A0A0 !important;
        }

        /* CONTAINERS E INPUTS */
        .st-emotion-cache-1r4qj8v {
            background-color: #1e2130 !important;
        }
        .stTextInput input, .stNumberInput input {
            background-color: #2a2f45 !important;
            color: #FAFAFA !important;
            border: 1px solid #4a5474 !important;
            border-radius: 5px;
        }
        
        /* ESTILO ESPECÍFICO E FORÇADO PARA TABELAS (st.table) */
        table {
            width: 100%;
            background-color: #1e2130 !important; /* Fundo da tabela */
            color: #FAFAFA !important;
            border-radius: 10px;
            overflow: hidden; /* Garante que o border-radius aplique nos cantos */
        }
        th { /* Cabeçalho da tabela */
            background-color: #2a2f45 !important;
            color: #FAFAFA !important;
            font-weight: bold;
            text-align: left;
            padding: 12px;
        }
        td { /* Células da tabela */
            background-color: #1e2130 !important;
            color: #FAFAFA !important;
            padding: 12px;
            border-top: 1px solid #2a2f45; /* Linha separadora entre as linhas */
        }
        
        hr {
            border-color: #4a5474 !important;
        }
    </style>
""", unsafe_allow_html=True)


# --- Funções auxiliares ---
def parse_input(input_str):
    try:
        return float(str(input_str).replace(".", "").replace(",", "."))
    except (ValueError, TypeError):
        return 0.0

def format_number_br(value):
    if not isinstance(value, (int, float)):
        return "0,00"
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- Layout do Simulador ---
st.markdown("<h1 style='text-align: center;'>Simulador de Pontos Fidelidade</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px; margin-top: -10px;'>Ajuste os parâmetros à esquerda para simular o impacto dos pontos na performance da loja.</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    with st.expander("Editar Parâmetros da Simulação", expanded=True):
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            vendas_loja_input = st.text_input(
                "Faturamento Total (R$)", value="0,00",
                help="Total de vendas brutas da loja. Use ponto para milhar e vírgula para decimal."
            )
        with col_in2:
            valor_produto_input = st.text_input(
                "Preço Unitário", value="0,00",
                help="Preço médio do produto. Use ponto para milhar e vírgula para decimal."
            )

        col_in3, col_in4 = st.columns(2)
        with col_in3:
            pontos_necessarios_input = st.text_input(
                "Pontos de Corte", value="0",
                help="Quantidade de pontos exigida para trocar por um produto."
            )
        with col_in4:
            pontos_por_real_input = st.text_input(
                "Pontos por R$1", value="0",
                help="Número de pontos dados a cada R$1 em vendas."
            )
        
        vendas_loja = parse_input(vendas_loja_input)
        valor_produto = parse_input(valor_produto_input)
        pontos_necessarios = int(parse_input(pontos_necessarios_input))
        pontos_por_real = parse_input(pontos_por_real_input)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h5>Premissas</h5>", unsafe_allow_html=True)
        st.markdown(""" 
            <div style='font-size: 14px;'>
                <ul>
                  <li><strong>Vendas identificadas:</strong> <span style='color: #28a745'>35%</span></li>
                  <li><strong>Valor do Ponto provisionado:</strong> <span style='color: #28a745'>5%</span></li>
                  <li><strong>Pontos da loja resgatados:</strong> <span style='color: #28a745'>25%</span></li>
                  <li><strong>Pontos emitidos resgatados na própria loja:</strong> <span style='color: #28a745'>65%</span></li>
                  <li><strong>QTD de pontos resgatados de outras lojas:</strong> <span style='color: #28a745'>300.000</span></li>
                  <li><strong>Lift:</strong> <span style='color: #28a745'>2.50%</span></li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

# --- Cálculos ---
pct_vendas_identificadas = 0.35
valor_ponto_provisionado = 0.05
pct_resgate_loja = 0.25
pct_resgatado_proprio = 0.65
pct_resgatado_fora = 1 - pct_resgatado_proprio
lift = 0.0250
breakage = 1 - pct_resgate_loja
pontos_outras_lojas_resgatados_na_loja = 300_000.0
carga_tributaria = 0.095

reais_identificados = vendas_loja * pct_vendas_identificadas
pontos_dados = reais_identificados * pontos_por_real
valor_pontos_provisionados = reais_identificados * valor_ponto_provisionado
pontos_resgatados_loja = pontos_dados * pct_resgate_loja
valor_por_ponto = valor_produto / pontos_necessarios if pontos_necessarios else 0

pontos_proprios_resgatados = pontos_resgatados_loja * pct_resgatado_proprio
reembolso_outras_lojas = pontos_outras_lojas_resgatados_na_loja * valor_por_ponto
custo_resgate_fora = (pontos_resgatados_loja * pct_resgatado_fora) * valor_por_ponto
net_loja = reembolso_outras_lojas - custo_resgate_fora
ganho_tributario = (pontos_resgatados_loja * valor_por_ponto) * carga_tributaria
lift_aplicado = lift * reais_identificados
ganho_programa = net_loja + lift_aplicado + ganho_tributario
ganho_pct_final = (ganho_programa / vendas_loja) * 100 if vendas_loja else 0

# --- Tabela Resultado ---
df_simulador = pd.DataFrame({
    "Parâmetro": [
        "Ganho % final do programa",
        "Ganho do programa (R$)",
        "Lift Aplicado (R$)",
        "Ganho tributário (R$)"
    ],
    "Valor": [
        f"{ganho_pct_final:.2f}%",
        format_number_br(ganho_programa),
        format_number_br(lift_aplicado),
        format_number_br(ganho_tributario)
    ]
})

# Remove o cabeçalho do índice do DataFrame para uma aparência mais limpa na tabela
df_simulador.set_index('Parâmetro', inplace=True)

with col2:
    st.markdown("<h3 style='text-align: center;'>Detalhamento Completo</h3>", unsafe_allow_html=True)
    
    # Usando st.table para renderizar a tabela, que obedece melhor ao CSS
    st.table(df_simulador)
