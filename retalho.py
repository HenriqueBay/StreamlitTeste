

'''
with detailPanel:
                if selected_client:
                    detailPanel.write(f"Cliente: {selected_client}")

                    product_names = 'teib.fetch_product_price'
                    selected_columns2 = ['id_marca', 'marca', 'preco_24_25']

                    product_names = get_table_data2(
                        connection, product_names, selected_columns2)

                    if product_names:
                        st.write(
                            "Selecione o produto e insira a quantidade:")
                        st.write("| Marca | Quantidade | Total |")
                        st.write("| --- | --- | --- |")

                    for product in product_names:
                        id_marca = product[0]
                        nome_marca = product[1]
                        valor_str = product[2]
                        valor = float(valor_str.replace('$', '').replace(
                            ',', ''))  # Convertendo valor para float

                        st.write(f"| {nome_marca} |", end='')
                        quantidade = st.number_input(
                            '', value=0, step=1, key=f'quantidade_{id_marca}')
                        total = quantidade * valor
                        st.write(f" {quantidade} | {total:.2f} |")

        else:
            detailPanel.write("Nenhum produto encontrado")

    else:
        detailPanel.write("Selecione um cliente")
        147 até 180
--------------------------------------------------------------------------------------

                    for index, product in enumerate(product_names):

                        with st.container():
                            col1, col2, col3 = st.columns(3)

                            with col1:
                                product_name = st.selectbox(
                                    'Produto:', product_names, index=product_names.index(product["name"]))

                            with col2:
                                product_quantity = st.number_input(
                                    'Quantidade:',
                                    value=product["quantity"]),

                            with col3:
                                st.write("Descrição...")

                else:
                    detailPanel.write("Selecione um cliente")
'''
