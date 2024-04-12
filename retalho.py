

'''
def region_data(connection, table_name):
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT  FROM {table_name}")
        table_data = cursor.fetchall()
        cursor.close()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(table_data, columns=columns)
        return df
    except Exception as e:
        st.error(f"Erro ao obter dados da tabela {table_name}: {e}")
        return None


# ----------------------AGgrid

class ColetorDeDados:
    def __init__(self, conn):
        self.conn = conn


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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

def criar_aggrid(selected_client, connection):
    with connection.cursor() as cursor:
        # Consulta SQL para obter os nomes das marcas e os preços correspondentes
        sql = "SELECT marca, preco_24_25 FROM teib.fetch_product_price"
        cursor.execute(sql, (selected_client,))
        data = cursor.fetchall()  # Lista de tuplas contendo marca e preço

    # Criar DataFrame com os dados obtidos
    df = pd.DataFrame(data, columns=['Marca', 'Preço'])

    # Configurar as opções da grade
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        groupable=True, value=True, enableRowGroup=True, editable=True)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_grid_options(domLayout='normal')
    gridOptions = gb.build()

    # Renderizar a grade
    AgGrid(df, gridOptions=gridOptions, height=400)
    
    
    
    
    
def criar_aggrid(connection,selected_client):
    with connection.cursor() as cursor:
        sql = "SELECT marca, preco_24_25 FROM teib.fetch_product_price"
        cursor.execute(sql, (selected_client,))
        data = cursor.fetchall()

    df = pd.DataFrame(data, columns=['Marca', 'Preço'])
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(
        groupable=True, value=True, enableRowGroup=True, editable=True)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_grid_options(domLayout='normal')
    gridOptions = gb.build()

    # Renderizar a grade
    AgGrid(df, gridOptions=gridOptions, height=400)

'''
