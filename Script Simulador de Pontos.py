import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Dashboard Razonetes", layout="wide")

# Estilo customizado (com ajustes para posicionar o SVG no lugar da bolinha)
st.markdown("""
    <style>
    /* @import url('https://fonts.googleapis.com/css2?family=General+Sans:wght@400;600;700&display=swap'); */
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

    /* Estilo para tooltips customizadas */
    .tooltip {
        position: relative;
        display: inline-flex; /* Alterado para inline-flex para alinhar o conteúdo interno */
        align-items: center; /* Centraliza verticalmente o texto e a porcentagem dentro do tooltip */
        cursor: help;
        /* Remova paddings/margins extras que possam causar desalinhamento */
        padding: 0;
        margin: 0;
    }

    .tooltip .tooltiptext {
        visibility: hidden;
        width: 300px;
        background-color: #1e2130;
        color: white;
        text-align: left;
        border-radius: 6px;
        padding: 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%; /* Acima do elemento */
        left: 50%;
        margin-left: -150px; /* Centraliza a tooltip */
        opacity: 0;
        transition: opacity 0.3s;
        border: 1px solid #2f0; /* Borda verde */
        font-size: 12px;
        line-height: 1.4;
    }

    .tooltip .tooltiptext::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: #2f0 transparent transparent transparent; /* Seta para baixo, cor verde */
    }

    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }

    /* ****************************************************** */
    /* NOVOS ESTILOS PARA SUBSTITUIR A BOLINHA PELO ÍCONE SVG */
    /* ****************************************************** */

    /* AJUSTE AQUI: Movendo o título "Premissas" para a esquerda */
    h3 {
        font-family: 'General Sans', sans-serif;
        font-weight: 700;
        color: white;
        margin-left: -20px; /* Valor ajustado para mover para a esquerda */
    }

    .premissas-list {
        list-style: none; /* Remove as bolinhas padrão */
        padding-left: 0; /* Remove o padding padrão da lista */
        /* AJUSTE AQUI: Movendo a lista de premissas para a esquerda */
        margin-left: -20px; /* Valor ajustado para mover para a esquerda */
    }

    .premissas-list li {
        position: relative; /* Essencial para posicionar o ícone SVG */
        padding-left: 25px; /* Espaço para o ícone. Ajuste este valor se precisar de mais/menos espaço entre ícone e texto. */
        margin-bottom: 8px; /* Espaçamento entre os itens da lista */
        font-size: 14px; /* Garante que o texto esteja no tamanho desejado */
        display: flex; /* Usar flexbox para melhor alinhamento do texto e conteúdo */
        align-items: center; /* Centraliza verticalmente o conteúdo do li (texto e tooltip) */
        flex-wrap: nowrap; /* Impede que o texto quebre para a próxima linha */
        line-height: 1.2; /* Pode ajustar a altura da linha para o texto, se necessário */
    }

    .premissas-list li .st-help-icon-container.list-bullet-icon {
        position: absolute; /* Posicionamento absoluto dentro do li */
        left: 0px; /* Posiciona o ícone no início do li. Se precisar de ajuste fino para a esquerda, use um valor negativo como -2px. */
        top: 50%; /* Centraliza verticalmente */
        transform: translateY(-50%); /* Ajuste fino para centralizar com base na altura do próprio ícone */
        width: 16px; /* Tamanho do ícone */
        height: 16px; /* Tamanho do ícone */
        cursor: help; /* Muda o cursor */
        flex-shrink: 0; /* Impede que o ícone diminua */
        line-height: 0; /* Remove qualquer altura de linha implícita do contêiner do ícone */
    }

    /* Estilo para o SVG em si */
    .st-help-icon-container svg {
        width: 100%;
        height: 100%;
        overflow: visible;
        color: #888; /* Cor padrão para o SVG */
        display: block; /* Garante que o SVG não adicione espaço extra abaixo por ser inline */
        vertical-align: middle; /* Ajuda a alinhar o SVG se por algum motivo ele ainda agir como inline */
    }

    .st-help-icon-container svg path {
        stroke-width: 1.8;
    }
    .st-help-icon-container svg path[d*="M12 22C"],
    .st-help-icon-container svg path[d*="M9.09 9C"],
    .st-help-icon-container svg path[d*="M12 18H12.01"]
    {
        stroke: currentColor;
    }
    .st-help-icon-container svg path[d*="M9.09 9C"] { /* Interrogação */
        fill: currentColor;
        stroke: none;
    }
    .st-help-icon-container svg path[d*="M12 22C"] { /* Círculo */
        fill: none;
    }
    </style>
""", unsafe_allow_html=True)

# Funções auxiliares
def parse_input(input_str):
    try:
        return float(str(input_str).replace(".", "").replace(",", "."))
    except ValueError:
        return 0.0

def format_number_br(value):
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# SVG EXATO do ícone de help do Streamlit
STREAMLIT_HELP_ICON_SVG = """
<svg stroke-width="2" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" color="currentColor">
    <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="1.5"></path>
    <path d="M9.09 9C9.32567 8.33777 9.7719 7.76657 10.3725 7.35036C10.9731 6.93414 11.7057 6.68149 12.45 6.62C13.2982 6.55171 14.1207 6.84587 14.747 7.42468C15.3733 8.00349 15.7663 8.82855 15.82 9.71C15.82 10.7 15.32 11.16 14.47 11.9C13.62 12.64 13.06 13.51 13.06 14.5V15" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path>
    <path d="M12 18H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path>
</svg>
"""

# --- NOVO: Adicionar a introdução dentro de um st.expander (versão concisa)
# MUDANÇA AQUI: expanded=False
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


# --- Simulador
col1, col2 = st.columns([1, 1])

with col1:
    with st.expander("Editar Parâmetros da Simulação", expanded=True):
        with st.container():
            col_in1, col_in2 = st.columns(2)
            with col_in1:
                vendas_loja_input = st.text_input(
                    "Faturamento Bruto Total Anual (R$)",
                    value="0,00",
                    help="Vendas Brutas Totais no Período Analisado"
                )
                vendas_loja = parse_input(vendas_loja_input)
            with col_in2:
                valor_produto_input = st.text_input(
                    "Preço Médio por Produto",
                    value="0,00",
                    help="Utilize o preço de um item específico ou a média dos preços entre diferentes produtos"
                )
                valor_produto = parse_input(valor_produto_input)

            col_in3, col_in4 = st.columns(2)
            with col_in3:
                pontos_necessarios_input = st.text_input(
                    "Pontuação Mínima para Resgate",
                    value="0",
                    help="Defina a quantidade mínima de pontos para resgatar um produto."
                )
                pontos_necessarios = int(parse_input(pontos_necessarios_input))
            with col_in4:
                pontos_por_real_input = st.text_input(
                    "Pontos por Real R$",
                    value="0",
                    help="Defina a quantidade de pontos atribuída a cada R$1 em vendas. Exemplo: 1 ponto para cada R$1 gasto."
                )
                pontos_por_real = parse_input(pontos_por_real_input)

        # Premissas - Com o ícone SVG EXATO do Streamlit no lugar da bolinha
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h3>Premissas</h3>", unsafe_allow_html=True) # Este H3 terá margin-left: -20px

        pct_vendas_identificadas_display = 35
        valor_ponto_provisionado_display = 5
        pct_resgate_loja_display = 25
        lift_display = 2.50

        st.markdown(f"""
            <div style='font-size: 14px;'>
                <ul class="premissas-list">
                    <li>
                        <span class="st-help-icon-container list-bullet-icon">{STREAMLIT_HELP_ICON_SVG}</span>
                        <div class="tooltip">
                            <strong>Vendas identificadas:</strong>&nbsp;<span style='color: #2f0'>{pct_vendas_identificadas_display}%</span>
                            <span class="tooltiptext">Mostra quantas vendas sabemos quem comprou. Representa a porcentagem das vendas totais onde conseguimos identificar o cliente que realizou a compra.</span>
                        </div>
                    </li>
                    <li>
                        <span class="st-help-icon-container list-bullet-icon">{STREAMLIT_HELP_ICON_SVG}</span>
                        <div class="tooltip">
                            <strong>Valor do Ponto provisionado:</strong>&nbsp;<span style='color: #2f0'>{valor_ponto_provisionado_display}%</span>
                            <span class="tooltiptext">É o valor em reais que a empresa reserva para cada ponto acumulado pelo cliente. Representa o custo financeiro que a empresa provisiona para honrar os pontos distribuídos.</span>
                        </div>
                    </li>
                    <li>
                        <span class="st-help-icon-container list-bullet-icon">{STREAMLIT_HELP_ICON_SVG}</span>
                        <div class="tooltip">
                            <strong>Pontos da loja resgatados:</strong>&nbsp;<span style='color: #2f0'>{pct_resgate_loja_display}%</span>
                            <span class="tooltiptext">Quantidade de pontos que os clientes usaram para trocar por produtos ou benefícios. Representa a porcentagem dos pontos distribuídos que efetivamente foram utilizados pelos clientes.</span>
                        </div>
                    </li>
                    <li>
                        <span class="st-help-icon-container list-bullet-icon">{STREAMLIT_HELP_ICON_SVG}</span>
                        <div class="tooltip">
                            <strong>Lift:</strong>&nbsp;<span style='color: #2f0'>{lift_display:.2f}%</span>
                            <span class="tooltiptext">É um termo usado para indicar o aumento ou melhoria em algum resultado, geralmente em vendas, conversão ou desempenho, após a aplicação de uma ação ou estratégia. Neste caso, representa o incremento nas vendas gerado pelo programa de fidelidade.</span>
                        </div>
                    </li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

# --- Cálculos (usando os valores fixos originais para os cálculos)
pct_vendas_identificadas = pct_vendas_identificadas_display / 100.0
valor_ponto_provisionado = valor_ponto_provisionado_display / 100.0
pct_resgate_loja = pct_resgate_loja_display / 100.0
lift = lift_display / 100.0


breakage = 1 - pct_resgate_loja
reais_identificados = vendas_loja * pct_vendas_identificadas
pontos_dados = reais_identificados * pontos_por_real
valor_pontos_provisionados = reais_identificados * valor_ponto_provisionado
pontos_resgatados_loja = pontos_dados * pct_resgate_loja
valor_por_ponto = valor_produto / pontos_necessarios if pontos_necessarios else 0
carga_tributaria = 0.0965
valor_pontos_dados_balde = reais_identificados * valor_por_ponto
saldo_3 = valor_pontos_dados_balde
saldo_4 = saldo_3 * pct_resgate_loja
valor_pontos_provisionados_resgatados = pontos_resgatados_loja * carga_tributaria # Correção: Multiplicar pelo valor resgatado, não provisionado
ganho_tributario = valor_pontos_provisionados_resgatados # Já é o ganho tributário após a correção acima
taxa_selic = 0.12
receita_financeira = ((saldo_3 + saldo_4) / 2) * taxa_selic
lift_aplicado = lift * reais_identificados
ganho_programa = ganho_tributario + lift_aplicado + receita_financeira
ganho_pct_final = ganho_programa / vendas_loja if vendas_loja else 0

# --- Tabela Resultado
df_simulador = pd.DataFrame({
    "Parâmetro": [
        "Ganho Tributário",
        "Lift Aplicado",
        "Ganho do Programa",
        "Ganho % Final do Programa"
    ],
    "Valor": [
        ganho_tributario,
        lift_aplicado,
        ganho_programa,
        ganho_pct_final * 100
    ]})

df_simulador["Valor"] = df_simulador.apply(
    lambda row: f"{row['Valor']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + "%"
    if row["Parâmetro"] == "Ganho % Final do Programa"
    else ("R$ " + f"{row['Valor']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")),
    axis=1
)

with col2:
    with st.container():
        st.markdown("<h3 style='text-align: center;'>Detalhamento Completo</h3>", unsafe_allow_html=True)
        st.dataframe(df_simulador, use_container_width=True, hide_index=True)

        # Adição das definições dos termos dentro de um expander
        with st.expander("Definições dos Termos"): # A caixa expansível existente
            st.markdown("""
            **Ganho Tributário:** É o benefício fiscal que a empresa obtém ao reconhecer provisões, reduzindo impostos a pagar.

            **Lift Aplicado:** É o aumento real nos resultados que foi obtido após a implementação de uma ação, campanha ou estratégia.

            **Ganho do Programa:** É o benefício total que a empresa obtém com a implementação de um programa, como aumento de vendas, redução de custos ou melhorias no relacionamento com clientes.

            **Ganho % Final do Programa:** É a porcentagem total de melhora ou lucro que o programa gerou no resultado final da empresa.
            """)
