import streamlit as st
import pandas as pd
import json
import time
from utils import *
from database import DBConnection
from st_aggrid import AgGrid, AgGridTheme, GridUpdateMode, GridOptionsBuilder, AgGrid, GridOptionsBuilder, GridUpdateMode

connection = DBConnection()


@st.cache_data
def get_df_customers():
    try:
        cursor = connection.cursor()
        columns = ['dn', 'regional', 'distrito',
                   'rtv', 'atendimento', 'nome_cliente']
        select_columns = ', '.join(columns)
        cursor.execute(f'SELECT {select_columns} FROM teib.fetch_data limit 1000')
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)
        return df
    except Exception as e:
        st.error(f'Erro de conexão: {str(e)}')
        return None
    finally:
        cursor.close()


@st.cache_data
def get_df_products():
    try:
        cursor = connection.cursor()
        columns = ['id_marca', 'marca', 'preco_24_25']
        select_columns = ', '.join(columns)
        cursor.execute(
            f'SELECT {select_columns} FROM teib.fetch_product_price')
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)
        return df
    except:
        st.error('Error de conexão')
        return None
    finally:
        cursor.close()


def main():

    st.set_page_config(page_title='Tracking EIB', layout='wide')

    # Session state initialization
    if 'customer_selection' not in st.session_state:
        st.session_state['customer_selection'] = None
    if 'visibility' not in st.session_state:
        st.session_state.visibility = 'visible'
        st.session_state.disabled = False

    # Load bootstrap
    st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

    # Load custom css
    with open('main.css') as f:
        st.write(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    # Header
    image = 'bayer-logo-0.png'
    st.image(image, use_column_width=False, width=100)
    st.title('Tracking EIB')
    st.markdown('''<h4 style="text-align: left; color: black;">Não repara a bagunça, estamos em construção! :3</h4>''', unsafe_allow_html=True)
    st.page_link('pages\info.py',
                 label='Para informações de uso e regras, clique aqui⚠️')

    # Content
    if connection:
        df_customers = get_df_customers()

        if df_customers is not None:
            st.container()

            st.write('## Aplique os filtros para obter seu cliente:')

            # Customer selection
            selected_rows = [st.session_state['customer_selection']['selectedItems'][0]['_selectedRowNodeInfo']['nodeRowIndex']] \
                if st.session_state['customer_selection'] is not None \
                and len(st.session_state['customer_selection']['selectedItems']) > 0 \
                else []

            # Dynamic main columns
            listPanel, detailPanel = st.columns(2, gap='medium')

            # Customer panel
            with listPanel:
                gd = GridOptionsBuilder.from_dataframe(df_customers)
                gd.configure_pagination(
                    enabled=True, paginationAutoPageSize=False, paginationPageSize=100)
                gd.configure_side_bar(True)
                gd.configure_default_column(editable=False, groupable=True)
                gd.configure_selection(selection_mode="single", use_checkbox=True, pre_selected_rows=selected_rows)
                gridoptions = gd.build()
                gridoptions['alwaysShowHorizontalScroll'] = True
                gridoptions['alwaysShowVerticalScroll'] = True
                gridoptions['suppressHorizontalScroll'] = False
                gridoptions['supressVerticalScroll'] = False

                AgGrid(df_customers,
                    key='customer_selection',
                    gridOptions=gridoptions,
                    update_mode=GridUpdateMode.SELECTION_CHANGED,
                    allow_unsafe_jscode=True,
                    height=600,
                    theme=AgGridTheme.BALHAM)

            # Detail panel
            if detailPanel is not None:

                def save_changes():
                        time.sleep(2)  # ! Fake delay
                        with detailPanel:
                            st.success('Os dados foram salvos')
                        st.session_state['customer_selection'] = None

                with detailPanel:
                    customer = st.session_state['customer_selection']['selectedItems'][0]
                    products = get_df_products()

                    st.code(json.dumps(customer, indent=4))

                    st.button('Salvar dados', on_click=save_changes)
# Main method call


if __name__ == '__main__':
    main()
