import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração do Streamlit
st.set_page_config(page_title="Dashboard Alzheimer e MRI", layout="wide")

# Título do Dashboard
st.title("Análise de Dados de Alzheimer e MRI")
st.markdown("""
Este dashboard permite explorar dados transversais e longitudinais de MRI relacionados ao Alzheimer.
""")


# Função para carregar os dados
@st.cache_data
def load_data():
    # Carregar dados transversais
    transversal = pd.read_csv("oasis_cross-sectional.csv")

    # Carregar dados longitudinais
    longitudinal = pd.read_csv("oasis_longitudinal.csv")

    return transversal, longitudinal


# Carregar os dados
transversal, longitudinal = load_data()

# Sidebar para filtros
st.sidebar.header("Filtros")
st.sidebar.markdown("Selecione os filtros para explorar os dados.")

# Filtro para dados transversais
st.sidebar.subheader("Dados Transversais")
idade_min_transversal, idade_max_transversal = st.sidebar.slider(
    "Faixa de Idade (Transversal)",
    min_value=int(transversal['Age'].min()),
    max_value=int(transversal['Age'].max()),
    value=(int(transversal['Age'].min()), int(transversal['Age'].max()))
)

# Filtro para dados longitudinais
st.sidebar.subheader("Dados Longitudinais")
idade_min_longitudinal, idade_max_longitudinal = st.sidebar.slider(
    "Faixa de Idade (Longitudinal)",
    min_value=int(longitudinal['Age'].min()),
    max_value=int(longitudinal['Age'].max()),
    value=(int(longitudinal['Age'].min()), int(longitudinal['Age'].max()))
)

# Aplicar filtros
transversal_filtrado = transversal[
    (transversal['Age'] >= idade_min_transversal) & (transversal['Age'] <= idade_max_transversal)]
longitudinal_filtrado = longitudinal[
    (longitudinal['Age'] >= idade_min_longitudinal) & (longitudinal['Age'] <= idade_max_longitudinal)]

# Visualizações
st.header("Análise Transversal")

# Gráfico de distribuição de idade
st.subheader("Distribuição de Idade")
fig, ax = plt.subplots()
sns.histplot(transversal_filtrado['Age'], kde=True, ax=ax)
ax.set_xlabel("Idade")
ax.set_ylabel("Frequência")
st.pyplot(fig)

# Gráfico de MMSE vs. CDR
st.subheader("MMSE vs. CDR")
fig, ax = plt.subplots()
sns.scatterplot(data=transversal_filtrado, x='MMSE', y='CDR', hue='M/F', ax=ax)
ax.set_xlabel("Mini Exame do Estado Mental (MMSE)")
ax.set_ylabel("Taxa de Demência Clínica (CDR)")
st.pyplot(fig)

# Boxplot de nWBV por grupo
st.subheader("Volume Cerebral Normalizado (nWBV) por Grupo")
fig, ax = plt.subplots()
sns.boxplot(data=transversal_filtrado, x='CDR', y='nWBV', ax=ax)
ax.set_xlabel("Taxa de Demência Clínica (CDR)")
ax.set_ylabel("Volume Cerebral Normalizado (nWBV)")
st.pyplot(fig)

# Análise Longitudinal
st.header("Análise Longitudinal")

# Gráfico de linha para MMSE ao longo do tempo
st.subheader("Evolução do MMSE ao Longo do Tempo")
fig, ax = plt.subplots()
for subject_id in longitudinal_filtrado['Subject ID'].unique():
    dados_individuo = longitudinal_filtrado[longitudinal_filtrado['Subject ID'] == subject_id]
    sns.lineplot(data=dados_individuo, x='Visit', y='MMSE', ax=ax, label=subject_id)
ax.set_xlabel("Visita")
ax.set_ylabel("Mini Exame do Estado Mental (MMSE)")
st.pyplot(fig)

# Heatmap de correlação
st.subheader("Mapa de Correlação")
fig, ax = plt.subplots()
corr = longitudinal_filtrado[['Age', 'MMSE', 'CDR', 'nWBV', 'eTIV']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# Tabela de dados
st.header("Dados Filtrados")
st.subheader("Dados Transversais")
st.write(transversal_filtrado)

st.subheader("Dados Longitudinais")
st.write(longitudinal_filtrado)