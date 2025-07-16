# streamlit_app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Visualizador de Dados", layout="wide")

st.title("📊 Visualizador de Arquivos CSV ou Excel")

# Upload do arquivo
uploaded_file = st.file_uploader("Faça upload do seu arquivo CSV ou Excel", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("Arquivo carregado com sucesso!")
        st.dataframe(df)

        st.subheader("📈 Estatísticas Básicas")
        st.write(df.describe())

        st.subheader("🔍 Filtros")
        col = st.selectbox("Escolha uma coluna para filtrar", df.columns)
        filtro = st.text_input("Digite o valor para filtrar")

        if filtro:
            st.write(df[df[col].astype(str).str.contains(filtro, case=False)])

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
else:
    st.info("Por favor, carregue um arquivo para começar.")
