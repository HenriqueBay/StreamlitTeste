import streamlit as st
from home import *
from utils import *
from db_connector import *


# Session state

if 'doc_cliente' not in st.session_state:
    st.session_state['doc_cliente'] = None

# A IDENTAÇÃO NO CÓDIGO É A IDENTAÇÃO NO SITE

st.set_page_config(page_title="Tracking EIB", layout="wide")
image = 'bayer-logo-0.png'
st.image(image, use_column_width=False, width=100)
st.title("Tracking EIB")
st.markdown("""<h4 style='text-align: left; color: black;'>
                    Não repara a bagunça, estamos em construção! :3</h4>""", unsafe_allow_html=True)
st.page_link("pages\info.py",
             label="Para informações de uso e regras, clique aqui⚠️")

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
        column_list = ",".join(selected_columns)
        cursor.execute(f"SELECT {column_list} FROM {table_name}")
        table_data = cursor.fetchall()
        cursor.close()
        return table_data
    except Exception as e:
        st.error(f"Erro ao obter dados da tabela {table_name}: {e}")
        return None


def get_table_data2(connection, product_names, selected_columns):
    try:
        cursor = connection.cursor()
        column_list = ",".join(selected_columns)
        cursor.execute(f"SELECT {column_list} FROM {product_names}")
        table_data = cursor.fetchall()
        cursor.close()
        return table_data
    except Exception as e:
        st.error(f"Erro ao obter dados da tabela {product_names}: {e}")
        return None


def main():
    if connection:
        table_name = 'teib.fetch_data'
        selected_columns = ['dn', 'regional', 'distrito',
                            'rtv', 'atendimento', 'nome_cliente']

        table_data = get_table_data(connection, table_name, selected_columns)

        if table_data:
            c = st.container()

            listPanel, detailPanel = c.columns(2)

            # Cria tabela
            df_table = pd.DataFrame(table_data, columns=selected_columns)

            with listPanel:
                st.write('## Aplique os filtros para obter seu cliente:')

                with st.container():  # Container de filtros
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        unique_dns = df_table['dn'].unique()
                        selected_dn = st.selectbox(
                            'DN:', ['Todos'] + list(unique_dns))

                    with col2:
                        selected_region = st.selectbox(
                            'Região:', ['Todos'] + list(df_table['regional'].unique()))

                    with col3:
                        districts = df_table['distrito'].unique()
                        selected_district = st.selectbox(
                            'Distrito:', ['Todos'] + list(districts))

                    with col1:
                        rtvs = df_table['rtv'].unique()
                        selected_rtv = st.selectbox(
                            'RTV:', ['Todos'] + list(rtvs))

                    with col2:
                        atendimentos = df_table['atendimento'].unique()
                        selected_atendimento = st.selectbox(
                            'Atendimento:', ['Todos'] + list(atendimentos))

                    with col3:
                        clients = df_table['nome_cliente'].unique()
                        selected_client = st.selectbox(
                            'Cliente:', ['Todos'] + list(clients))

                    # col 1 e 2 de novo para alinhar

                    with col1:
                        selected_option1 = st.selectbox(
                            "Nome do Promotor", ['Opção 1A', 'Opção 1B', 'Opção 1C'])
                    with col2:
                        selected_option2 = st.selectbox(
                            "Status Negociação 24/25", ['Selecione...', 'Negociação em Aberto', 'Negociação Fechada'])

                filtered_df = df_table[(df_table['dn'] == selected_dn) | (
                    selected_dn == 'Todos')]
                filtered_df = filtered_df[(df_table['regional'] == selected_region) | (
                    selected_region == 'Todos')]
                filtered_df = filtered_df[(df_table['distrito'] == selected_district) | (
                    selected_district == 'Todos')]
                filtered_df = filtered_df[(df_table['rtv'] == selected_rtv) | (
                    selected_rtv == 'Todos')]
                filtered_df = filtered_df[(df_table['atendimento'] == selected_atendimento) | (
                    selected_atendimento == 'Todos')]
                filtered_df = filtered_df[(df_table['nome_cliente'] == selected_client) | (
                    selected_client == 'Todos')]

                df_with_options = pd.DataFrame({
                    'Nome do Promotor': [selected_option1] * len(filtered_df),
                    'Status Negociação 24/25': [selected_option2] * len(filtered_df)
                }, index=filtered_df.index)

                final_df = pd.concat([filtered_df, df_with_options], axis=1)

                if not final_df.empty:

                   # -------------------------- AGGRID clientes

                    df = pd.DataFrame(final_df, columns=[
                                      'dn', 'regional', 'distrito', 'rtv', 'atendimento', 'nome_cliente'])

        gd = GridOptionsBuilder.from_dataframe(df)
        gd.configure_pagination(enabled=True,
                                paginationAutoPageSize=False,
                                paginationPageSize=17000)
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
                            height=600,
                            theme=AgGridTheme.BALHAM)
        sel_row = grid_table["selected_rows"]
        if sel_row:
            selected_row = sel_row[0]
    # st.text_input(label="Nome do field",value=selected_row.get("field_name"),disabled=True)
    # st.write(selected_row.get("hectares"))
    st.dataframe(sel_row)

    # Cria detalhe

    with detailPanel:
        if selected_client:
            detailPanel.write(f"Cliente: {selected_client}")

            product_names = 'teib.fetch_product_price'
            selected_columns2 = ['id_marca', 'marca', 'preco_24_25']

            product_names = get_table_data2(
                connection, product_names, selected_columns2)


# ------------------------------------------------------------------------
# AGGRID NA ESQUERDA, COLETANDO OS LCIENTES E SELECIONANDO TUDO CERTO, E NA DIREITA UM DATA EDITOR
if __name__ == "__main__":
    main()
container.markdown("</div>", unsafe_allow_html=True)
container.markdown("<hr>", unsafe_allow_html=True)


# -----------------------Botão home


def my_function():
    window = home()
    window.display_home()


button = st.button("Salvar dados", on_click=my_function)

if button:
    st.write("Os dados foram salvos")


# Trava de preenchimento - Só é permitida a criação quando for preenchido todos os filtros
# Aba observações - Deixar criada a página aqui (Aquela aba de explicação inicial)
# Evitar erros
