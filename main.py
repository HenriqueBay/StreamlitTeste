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

# Aplicativo Streamlit
def main():
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
            st.write('## Filtros')

            # Organizar os filtros em três colunas
            col1, col2, col3, col4, col5, col6 = st.columns(6)

            # Filtrar por dn, regional, distrito, rtv, atendimento e cliente
            with col1:
                unique_dns = df_table['dn'].unique()
                selected_dn = st.selectbox('DN:', ['Todos'] + list(unique_dns))

            with col2:
                selected_region = st.selectbox('Região:', ['Todos'] + list(df_table['regional'].unique()))

            with col3:
                districts = df_table['distrito'].unique()
                selected_district = st.selectbox('Distrito:', ['Todos'] + list(districts))

            with col4:
                rtvs = df_table['rtv'].unique()
                selected_rtv = st.selectbox('RTV:', ['Todos'] + list(rtvs))

            with col5:
                atendimentos = df_table['atendimento'].unique()
                selected_atendimento = st.selectbox('Atendimento:', ['Todos'] + list(atendimentos))

            with col6:
                clients = df_table['nome_cliente'].unique()
                selected_client = st.selectbox('Cliente:', ['Todos'] + list(clients))

            # Adicionar duas listas suspensas
            with col1:
                selected_option1 = st.selectbox("Nome do Promotor", ['Opção 1A', 'Opção 1B', 'Opção 1C'])
            with col2:
                selected_option2 = st.selectbox("Status Negociação 24/25", ['Selecione...','Negociação em Aberto', 'Negociação Fechada'])

            # Filtrar o DataFrame baseado nos filtros selecionados
            filtered_df = df_table[(df_table['dn'] == selected_dn) | (selected_dn == 'Todos')]
            filtered_df = filtered_df[(df_table['regional'] == selected_region) | (selected_region == 'Todos')]
            filtered_df = filtered_df[(df_table['distrito'] == selected_district) | (selected_district == 'Todos')]
            filtered_df = filtered_df[(df_table['rtv'] == selected_rtv) | (selected_rtv == 'Todos')]
            filtered_df = filtered_df[(df_table['atendimento'] == selected_atendimento) | (selected_atendimento == 'Todos')]
            filtered_df = filtered_df[(df_table['nome_cliente'] == selected_client) | (selected_client == 'Todos')]

            # Inserir dados selecionados no DataFrame
            df_with_options = pd.DataFrame({
                'Nome do Promotor': [selected_option1] * len(filtered_df),
                'Status Negociação 24/25': [selected_option2] * len(filtered_df)
            })

            # Concatenar o DataFrame com os dados filtrados e as opções selecionadas
            final_df = pd.concat([filtered_df, df_with_options], axis=1)

            # Exibir dados filtrados
            if not final_df.empty:
                st.write("### Dados Filtrados:")
                st.write(final_df)
                
                # Exibir o AgGrid para o cliente selecionado
                if selected_client != 'Todos':
                    st.header(f'Dados do Cliente: {selected_client}')
                    criar_aggrid(selected_client)
            else:
                st.write("Nenhum resultado encontrado.")

#------------------------------------------------------------------------
def criar_aggrid(selected_client):
    # Aqui você pode usar o cliente selecionado para filtrar os dados conforme necessário
    # Por exemplo:
    # df_cliente = df_table[df_table['nome_cliente'] == selected_client]
    
    # Suponha que você tenha o DataFrame para o cliente selecionado
    # Criar DataFrame com 15 linhas para exemplo
    produtos = ['Produto 1', 'Produto 2', 'Produto 3', 'Produto 4', 'Produto 5',
                'Produto 6', 'Produto 7', 'Produto 8', 'Produto 9', 'Produto 10',
                'Produto 11', 'Produto 12', 'Produto 13', 'Produto 14', 'Produto 15']

    df = pd.DataFrame({'Produto': produtos})
    df['Quantidade'] = ''
    df['Observações'] = ''

    # Configurar as opções da grade
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=True)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_grid_options(domLayout='normal')
    gridOptions = gb.build()

    # Renderizar a grade
    AgGrid(df, gridOptions=gridOptions, height=400)

if __name__ == "__main__":
    main()
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

