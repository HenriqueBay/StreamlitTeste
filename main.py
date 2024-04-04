import streamlit as st
from home import *
from utils import *
import random
from db_connector import *

# A IDENTAÇÃO NO CÓDIGO É A IDENTAÇÃO NO SITE

st.set_page_config(page_title="Tracking EIB", layout="wide")
st.title("Tracking EIB")
st.markdown("""<h4 style='text-align: left; color: pink;'>
                    Não repara a bagunça, estamos em construção! :3</h4>""", unsafe_allow_html=True)

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False


load_bootstrap()
with open("main.css") as f:
    st.write(f"<style>{f.read()}</style>", unsafe_allow_html=True)
container = st.container()


regions_data = {
    'Sudeste': {
        'São Paulo': ['São Paulo', 'Guarulhos', 'Campinas', 'São Bernardo do Campo', 'Osasco'],
        'Minas Gerais': ['Belo Horizonte', 'Uberlândia', 'Contagem', 'Juiz de Fora', 'Betim'],
        'Rio de Janeiro': ['Rio de Janeiro', 'São Gonçalo', 'Duque de Caxias', 'Nova Iguaçu', 'Niterói'],
        'Espírito Santo': ['Vitória', 'Vila Velha', 'Serra', 'Cariacica', 'Cachoeiro de Itapemirim']
    },
    'Sul': {
        'Paraná': ['Curitiba', 'Londrina', 'Maringá', 'Ponta Grossa', 'Cascavel'],
        'Rio Grande do Sul': ['Porto Alegre', 'Caxias do Sul', 'Pelotas', 'Canoas', 'Santa Maria'],
        'Santa Catarina': ['Florianópolis', 'Joinville', 'Blumenau', 'São José', 'Criciúma']
    },
    # Adicione mais estados e cidades conforme necessário
}

# Carregar os dados em um DataFrame
df = pd.DataFrame({
    'Region': [region for region, states in regions_data.items() for state in states for city in states[state]],
    'State': [state for states in regions_data.values() for state, cities in states.items() for city in cities],
    'City': [city for states in regions_data.values() for state, cities in states.items() for city in cities]
})

# Selecionar região
selected_region = st.selectbox("Select Region", df['Region'].unique())

# Carregar os estados correspondentes à região selecionada
states = regions_data[selected_region]

# Criar um dropdown para selecionar o estado
selected_state = st.selectbox(
    "Select State", ['All States'] + list(states.keys()))

if selected_state != 'All States':
    cities = states[selected_state]
    selected_city = st.selectbox("Select City", ['All Cities'] + cities)

    if selected_city != 'All Cities':
        selected_number = st.selectbox("Select Number", list(range(1, 6)))
        df_filtered = df[(df['Region'] == selected_region) & (
            df['State'] == selected_state) & (df['City'] == selected_city)]
        df_filtered['Código RTV'] = selected_number
    else:
        df_filtered = df[(df['Region'] == selected_region)
                         & (df['State'] == selected_state)]
else:
    df_filtered = df[df['Region'] == selected_region]


if not df_filtered.empty:
    st.write("### DataFrame Filtrado:")
    st.write(df_filtered)
# Fechando a tag div do container
container.markdown("</div>", unsafe_allow_html=True)
container.markdown("<hr>", unsafe_allow_html=True)

# -----------------------Botão home


def my_function():
    window = home()
    window.display_home()


button = st.button("Mostrar Home", on_click=my_function)

if button:
    st.write("Os dados foram salvos")
st.page_link("pages\info.py", label="Informações")

# Trava de preenchimento - Só é permitida a criação quando for preenchido todos os filtros
# Aba observações - Deixar criada a página aqui (Aquela aba de explicação inicial)
# Evitar erros


def get_table_data(connection, table_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        table_data = cursor.fetchall()
        cursor.close()
        return table_data
    except Exception as e:
        st.error(f"Erro ao obter dados da tabela {table_name}: {e}")
        return None


# Conecta ao banco de dados PostgreSQL
if connection:
    # Obtém dados da tabela
    table_name = 'dbo.dim_regional'
    table_data = get_table_data(connection, table_name)
    if table_data:
        st.header(f"Dados da Tabela '{table_name}':")
        st.write(table_data)


def fetch_data_from_table(connection, table_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        table_data = cursor.fetchall()
        cursor.close()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(table_data, columns=columns)
        return df
    except Exception as e:
        st.error(f"Erro ao obter dados da tabela {table_name}: {e}")
        return None


# Conectar ao banco de dados PostgreSQL
if connection:
    st.success("Conectado ao banco de dados PostgreSQL.")

    # Obtém dados da tabela
    table_name = 'dbo.dim_regional'  # Nome da tabela que você deseja buscar
    table_data = fetch_data_from_table(connection, table_name)
    if table_data is not None:
        st.header(f"Dados da Tabela '{table_name}':")
        st.write(table_data)