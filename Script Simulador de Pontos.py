import streamlit as st
import pandas as pd
from io import BytesIO
import re # Adicionado para expressões regulares

st.set_page_config(page_title="Dashboard Razonetes", layout="wide")

# --- Google Tag Manager (GTM) --- 
st.markdown(
    f"""
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','GTM-569WGVK3');</script>
    <!-- End Google Tag Manager -->
    """,
    unsafe_allow_html=True
)

# --- CSS CUSTOMIZADO COM AJUSTE FINAL ---
st.markdown("""
    <style>
    /* Configurações gerais do tema escuro */
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
    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label {
        color: white;
    }
    
    /* CSS para o ícone de ajuda (?) */
    div[data-testid="stTooltipIcon"] svg {
        stroke: white !important;
    }
    div[data-testid="stTooltipIcon"] svg path[d^="M12 22C"] {
        fill: none !important;
    }

    /* CSS para o layout das premissas */
    .premise-block { 
        margin-bottom: 10px; 
    }
    .premise-title { 
        font-weight: normal;
        font-size: 14px;
        margin: 0; 
        padding: 0; 
    }
    .premise-caption { 
        color: #888; 
        font-size: 12px;
        margin: 0; 
        padding: 0; 
        line-height: 1.2; 
    }

    /* CSS para a tabela customizada */
    .custom-table {
        width: 100%;
        border-collapse: collapse; 
    }
    .custom-table td {
        padding: 8px; 
        border-top: 1px solid black; 
        color: white; 
        vertical-align: middle; 
        font-size: 14px;
    }
    .custom-table tr:first-child td {
        border-top: none; 
    }

    /* CSS para os campos de input */
    div[data-testid="stTextInput"] input {
        background-color: #1e2130;
        color: white;
        border-color: #31333F;
    }

    /* --- CÓDIGO ADICIONADO: Regras de CSS para o aviso --- */
    
    /* 1. Ajusta o PADDING (altura) do contêiner do alerta */
    div[data-testid="stAlert"] {
        padding: 0.5rem 1rem !important;
    }

    /* 2. Ajusta a FONTE e remove a margem do texto dentro do alerta */
    div[data-testid="stAlert"] p {
        font-size: 14px !important;
        margin-bottom: 1 !important;
    }

    </style>
""", unsafe_allow_html=True)

# --- Funções auxiliares ---
def parse_input(input_str):
    # Função ajustada para ser mais robusta
    if not isinstance(input_str, str) or not input_str:
        return 0.0
    try:
        return float(str(input_str).replace(".", "").replace(",", "."))
    except (ValueError, TypeError):
        return 0.0

def format_number_br(value):
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- CÓDIGO ADICIONADO: INICIALIZAÇÃO DO SESSION_STATE ---
if 'vendas_input' not in st.session_state:
    st.session_state.vendas_input = ""
if 'produto_input' not in st.session_state:
    st.session_state.produto_input = ""
if 'pontos_input' not in st.session_state:
    st.session_state.pontos_input = ""
if 'real_input' not in st.session_state:
    st.session_state.real_input = ""
if 'show_warning' not in st.session_state:
    st.session_state.show_warning = False

# --- CÓDIGO ADICIONADO: FUNÇÃO DE CALLBACK PARA LIMPEZA E AVISO ---
def clean_and_warn():
    vendas_antes = st.session_state.vendas_input
    produto_antes = st.session_state.produto_input
    pontos_antes = st.session_state.pontos_input
    real_antes = st.session_state.real_input

    vendas_depois = re.sub(r'[^0-9.,]', '', vendas_antes)
    produto_depois = re.sub(r'[^0-9.,]', '', produto_antes)
    pontos_depois = re.sub(r'[^0-9]', '', pontos_antes)
    real_depois = re.sub(r'[^0-9.,]', '', real_antes)

    st.session_state.vendas_input = vendas_depois
    st.session_state.produto_input = produto_depois
    st.session_state.pontos_input = pontos_depois
    st.session_state.real_input = real_depois

    if (vendas_antes != vendas_depois or
        produto_antes != produto_depois or
        pontos_antes != pontos_depois or
        real_antes != real_depois):
        st.session_state.show_warning = True
    else:
        st.session_state.show_warning = False

# --- Seção de Introdução ---
with st.expander("Sobre o Simulador de Pontos", expanded=False):
    st.markdown("""
    Este simulador foi criado para mostrar como um programa de fidelidade pode gerar ganhos financeiros, aumentar as vendas e oferecer benefícios fiscais.

    **Por que usar?**
    * Identifica oportunidades de otimização no relacionamento com o cliente.
    * Ajuda na tomada de decisões estratégicas.
    * Simula o ROI do programa, mostrando o impacto no faturamento.

    **Como usar?**
    1.  Preencha os dados do seu negócio (faturamento, preço médio, pontos por real, etc.).
    2.  Veja as premissas já configuradas (vendas identificadas, taxa de resgate, etc.).
    3.  Analise os resultados:
        * Ganho Tributário
        * Lift nas vendas
        * Ganho total e % do programa
    
    OBS: Passe o mouse sobre os campos para ver explicações sobre premissas e parâmetros.

    **Benefícios principais**
    * Projeção de ganhos.
    * Otimização do programa.
    * Melhor planejamento estratégico.
    * Entendimento claro da relação entre ponto, custo e retorno.
    """)

# --- Layout Principal ---
col1, col2 = st.columns([1, 1])

with col1:
    # --- ALTERAÇÃO PRINCIPAL: Usando st.container(border=True) para substituir o st.expander ---
    with st.container(border=True):
        st.markdown("<h3>Editar Parâmetros da Simulação</h3>", unsafe_allow_html=True)

        with st.container():
            col_in1, col_in2 = st.columns(2)
            with col_in1:
                st.text_input("Faturamento Bruto Total Anual (R$)", key='vendas_input', on_change=clean_and_warn, help="Vendas Brutas Totais no Período Analisado")
            with col_in2:
                st.text_input("Preço Médio por Produto", key='produto_input', on_change=clean_and_warn, help="Utilize o preço de um item específico ou a média dos preços entre diferentes produtos")

            col_in3, col_in4 = st.columns(2)
            with col_in3:
                st.text_input("Pontuação Mínima para Resgate", key='pontos_input', on_change=clean_and_warn, help="Defina a quantidade mínima de pontos para resgatar um produto.")
            with col_in4:
                st.text_input("Pontos por Real R$", key='real_input', on_change=clean_and_warn, help="Defina a quantidade de pontos atribuída a cada 1 real em vendas. Exemplo: 1 ponto para cada 1 real gasto.")

            if st.session_state.show_warning:
                st.warning("Apenas números e caracteres monetários são permitidos. Caracteres inválidos foram removidos.")

        # --- Premissas (dentro do mesmo contêiner com borda) ---
        st.markdown("<h3>Premissas</h3>", unsafe_allow_html=True)
        pct_vendas_identificadas_display = 35
        valor_ponto_provisionado_display = 5
        pct_resgate_loja_display = 25
        lift_display = 2.50
        
        st.markdown(f"""<div class="premise-block"><p class="premise-title">Vendas identificadas: <span style='color: #2f0'>{pct_vendas_identificadas_display}%</span></p><p class="premise-caption">Percentual de vendas onde o cliente foi identificado.</p></div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="premise-block"><p class="premise-title">Valor do Ponto provisionado: <span style='color: #2f0'>{valor_ponto_provisionado_display}%</span></p><p class="premise-caption">Custo em reais que a empresa reserva para cada ponto distribuído.</p></div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="premise-block"><p class="premise-title">Pontos da loja resgatados: <span style='color: #2f0'>{pct_resgate_loja_display}%</span></p><p class="premise-caption">Percentual de pontos que os clientes efetivamente usaram para resgate.</p></div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="premise-block"><p class="premise-title">Lift: <span style='color: #2f0'>{lift_display:.2f}%</span></p><p class="premise-caption">Aumento percentual nas vendas gerado pelo programa de fidelidade.</p></div>""", unsafe_allow_html=True)

# --- Cálculos ---
# --- ALTERAÇÃO: Lendo os valores do session_state para os cálculos ---
vendas_loja = parse_input(st.session_state.vendas_input)
valor_produto = parse_input(st.session_state.produto_input)
pontos_necessarios = int(parse_input(st.session_state.pontos_input) or 0)
pontos_por_real = parse_input(st.session_state.real_input)

pct_vendas_identificadas = pct_vendas_identificadas_display / 100.0
valor_ponto_provisionado = valor_ponto_provisionado_display / 100.0
pct_resgate_loja = pct_resgate_loja_display / 100.0
lift = lift_display / 100.0
reais_identificados = vendas_loja * pct_vendas_identificadas
pontos_dados = reais_identificados * pontos_por_real
valor_pontos_provisionados = reais_identificados * valor_ponto_provisionado
pontos_resgatados_loja = pontos_dados * pct_resgate_loja
valor_por_ponto = valor_produto / pontos_necessarios if pontos_necessarios else 0
carga_tributaria = 0.0965
valor_pontos_dados_balde = reais_identificados * valor_por_ponto
saldo_3 = valor_pontos_dados_balde
saldo_4 = saldo_3 * pct_resgate_loja
ganho_tributario = saldo_4 * carga_tributaria
taxa_selic = 0.12
receita_financeira = ((saldo_3 + saldo_4) / 2) * taxa_selic
lift_aplicado = lift * reais_identificados
ganho_programa = ganho_tributario + lift_aplicado + receita_financeira
ganho_pct_final = ganho_programa / vendas_loja if vendas_loja else 0

# --- Tabela de Resultados ---
df_simulador = pd.DataFrame({
    "Parâmetro": ["Ganho Tributário", "Lift Aplicado", "Ganho do Programa", "Ganho % Final do Programa"],
    "Valor": [ganho_tributario, lift_aplicado, ganho_programa, ganho_pct_final * 100]
})
df_simulador["Valor"] = df_simulador.apply(
    lambda row: f"{row['Valor']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + "%"
    if row["Parâmetro"] == "Ganho % Final do Programa"
    else ("R$ " + f"{row['Valor']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")),
    axis=1
)

# --- Coluna da Direita ---
with col2:
    with st.container():
        st.markdown("<h3 style='text-align: center;'>Detalhamento Completo</h3>", unsafe_allow_html=True)
        
        tabela_html = df_simulador.to_html(header=False, index=False, escape=False, classes="custom-table")
        st.markdown(tabela_html, unsafe_allow_html=True)

        with st.expander("Definições dos Termos"):
            st.markdown("""
            - **Ganho Tributário:** Benefício fiscal que a empresa obtém ao reconhecer provisões.
            - **Lift Aplicado:** Aumento real nos resultados obtido pela ação.
            - **Ganho do Programa:** Benefício total do programa.
            - **Ganho % Final do Programa:** Percentual de lucro que o programa gerou.
            """)
