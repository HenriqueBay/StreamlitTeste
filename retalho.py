

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
'''
