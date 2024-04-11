import streamlit as st
from home import *
from utils import *
import random
from db_connector import *




# A IDENTAÇÃO NO CÓDIGO É A IDENTAÇÃO NO SITE

st.set_page_config(page_title="Tracking EIB", layout="wide")
image = 'bayer-logo-0.png'
st.image(image, use_column_width=False, width=100)
st.title("Tracking EIB")
st.markdown("""<h4 style='text-align: left; color: black;'>
                    Não repara a bagunça, estamos em construção! :3</h4>""", unsafe_allow_html=True)

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

load_bootstrap()
with open("main.css") as f:
    st.write(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ----------------------------------------- Primeira parte
container = st.container()


def get_table_data(connection, table_name, selected_columns):
    try:
        cursor = connection.cursor()
        # Construir a lista de colunas para a consulta SQL
        column_list = ",".join(selected_columns)
        cursor.execute(f"SELECT {column_list} FROM {table_name}")
        table_data = cursor.fetchall()
        cursor.close()
        return table_data  # Retorna os dados da tabela
    except Exception as e:
        st.error(f"Erro ao obter dados da tabela {table_name}: {e}")
        return None

# Se a conexão foi estabelecida com sucesso
if connection:
    # Obtém dados da tabela
    table_name = 'teib.fetch_data'
    selected_columns = ['dn', 'regional', 'distrito', 'rtv', 'atendimento', 'nome_cliente']  # Lista das colunas desejadas
    table_data = get_table_data(connection, table_name, selected_columns)
    if table_data:
        st.header(f"Dados da Tabela '{table_name}':")
        df_table = pd.DataFrame(table_data, columns=selected_columns)

        # Mostrar os filtros
        st.sidebar.title('Filtros')

        # Filtrar por dn
        unique_dns = df_table['dn'].unique()
        selected_dn = st.sidebar.selectbox(
            'DN:', ['Todos'] + list(unique_dns))

        if selected_dn != 'Todos':
            filtered_df = df_table[df_table['dn'].str.startswith(selected_dn)]
        else:
            filtered_df = df_table

        # Filtrar por região
        selected_region = st.sidebar.selectbox(
            'Selecione a Região', ['Todos'] + list(filtered_df['regional'].unique()))

        if selected_region != 'Todos':
            filtered_df = filtered_df[filtered_df['regional']
                                      == selected_region]

        # Filtrar por distrito
        if selected_region != 'Todos':
            districts = filtered_df['distrito'].unique()
            selected_district = st.sidebar.selectbox(
                'Selecione o Distrito', ['Todos'] + list(districts))
            if selected_district != 'Todos':
                filtered_df = filtered_df[filtered_df['distrito']
                                          == selected_district]

        # Filtrar por RTV
        if selected_region != 'Todos':
            rtvs = filtered_df['rtv'].unique()
            selected_rtv = st.sidebar.selectbox(
                'Selecione o RTV', ['Todos'] + list(rtvs))
            if selected_rtv != 'Todos':
                filtered_df = filtered_df[filtered_df['rtv'] == selected_rtv]
                
                # Filtrar por Atendimento
        if selected_region != 'Todos':
            rtvs = filtered_df['atendimento'].unique()
            selected_atend = st.sidebar.selectbox(
                'Selecione o atendimento', ['Todos'] + list(rtvs))
            if selected_atend != 'Todos':
                filtered_df = filtered_df[filtered_df['atendimento'] == selected_atend]        

            # Filtrar por cliente
        clients = filtered_df['nome_cliente'].unique()
        selected_client = st.sidebar.selectbox(
                'Selecione o Cliente', ['Todos'] + list(clients))

        if selected_client != 'Todos':
            filtered_df = filtered_df[filtered_df['nome_cliente'] == selected_client]

       # Exibir dados filtrados
        if not filtered_df.empty:
            st.write("### Dados Filtrados:")
            st.write(filtered_df)
        else:
            st.write("Nenhum resultado encontrado.")
# Fechando a tag div do container
container.markdown("</div>", unsafe_allow_html=True)
container.markdown("<hr>", unsafe_allow_html=True)


# -----------------------Botão home


def my_function():
    window = home()
    window.display_home()


button = st.button("Salvar dados", on_click=my_function)

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
        return None
    except Exception as e:
        st.error(f"Erro ao obter dados da tabela {table_name}: {e}")
        return None


# Conecta ao banco de dados PostgreSQL
if connection:
    # Obtém dados da tabela
    table_name = 'teib.fato_tracking_eib'
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
    table_name = 'teib.fato_tracking_eib'  # Nome da tabela que você deseja buscar
    table_data = fetch_data_from_table(connection, table_name)
    if table_data is not None:
        st.header(f"Dados da Tabela '{table_name}':")
        st.write(table_data)


# -----------------Última
# initialize list of lists

'''
Teste
'''


data = [['Fazenda São João', 10], ['Talhão A', 15], ['Milho - C', 14]]

# Create the pandas DataFrame
df = pd.DataFrame(data, columns=['field_name', 'hectares'])

st.title("Teste dados de Gi")

gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_pagination(enabled=True,
                        paginationAutoPageSize=False,
                        paginationPageSize=20)
gd.configure_side_bar(True)
gd.configure_default_column(editable=False,
                            groupable=True)
gd.configure_selection(selection_mode="single",
                       use_checkbox=True)
gridoptions = gd.build()
gridoptions['alwaysShowHorizontalScroll'] = True
gridoptions['alwaysShowVerticalScroll'] = True
gridoptions['suppressHorizontalScroll'] = False
gridoptions['supressVerticalScroll'] = False


grid_table = AgGrid(df,
                    gridOptions=gridoptions,
                    update_mode=GridUpdateMode.SELECTION_CHANGED,
                    allow_unsafe_jscode=True,
                    height=500,
                    theme=AgGridTheme.BALHAM)
sel_row = grid_table["selected_rows"]
if sel_row:
    selected_row = sel_row[0]
    st.text_input(label="Nome do field", value=selected_row.get(
        "field_name"), disabled=True)
    st.write(selected_row.get("hectares"))
