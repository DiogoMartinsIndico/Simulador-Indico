import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Dashboard Razonetes", layout="wide")

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

    /* --- MUDANÇA AQUI: CSS PARA A NOSSA TABELA CUSTOMIZADA EM HTML --- */
    .custom-table {
        width: 100%;
        border-collapse: collapse; 
    }
    .custom-table td {
        padding: 8px; 
        border-top: 1px solid black; 
        color: white; 
        vertical-align: middle; 
        font-size: 14px; /* Adicionado para padronizar a fonte */
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
    </style>
""", unsafe_allow_html=True)

# Funções auxiliares
def parse_input(input_str):
    try:
        return float(str(input_str).replace(".", "").replace(",", "."))
    except (ValueError, TypeError):
        return 0.0

def format_number_br(value):
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

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
    with st.expander("Editar Parâmetros da Simulação", expanded=True):
        with st.container():
            col_in1, col_in2 = st.columns(2)
            with col_in1:
                vendas_loja_input = st.text_input("Faturamento Bruto Total Anual (R$)", value="", help="Vendas Brutas Totais no Período Analisado")
                vendas_loja = parse_input(vendas_loja_input)
            with col_in2:
                valor_produto_input = st.text_input("Preço Médio por Produto", value="", help="Utilize o preço de um item específico ou a média dos preços entre diferentes produtos")
                valor_produto = parse_input(valor_produto_input)

            col_in3, col_in4 = st.columns(2)
            with col_in3:
                pontos_necessarios_input = st.text_input("Pontuação Mínima para Resgate", value="", help="Defina a quantidade mínima de pontos para resgatar um produto.")
                pontos_necessarios = int(parse_input(pontos_necessarios_input))
            with col_in4:
                pontos_por_real_input = st.text_input("Pontos por Real R$", value="", help="Defina a quantidade de pontos atribuída a cada 1 real em vendas. Exemplo: 1 ponto para cada 1 real gasto.")
                pontos_por_real = parse_input(pontos_por_real_input)

        # --- Premissas ---
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
        
        # Converte o DataFrame para uma string HTML
        tabela_html = df_simulador.to_html(header=False, index=False, escape=False, classes="custom-table")
        
        # Renderiza o HTML usando st.markdown
        st.markdown(tabela_html, unsafe_allow_html=True)

        with st.expander("Definições dos Termos"):
            st.markdown("""
            - **Ganho Tributário:** Benefício fiscal que a empresa obtém ao reconhecer provisões.
            - **Lift Aplicado:** Aumento real nos resultados obtido pela ação.
            - **Ganho do Programa:** Benefício total do programa.
            - **Ganho % Final do Programa:** Percentual de lucro que o programa gerou.
            """)
