from utils import *
from db_connector import DatabaseConnector


class rtv_2():
    def __init__(self) -> None:
        self.conn = DatabaseConnector()
        pass
    def display_rtvs_2(self):

        database_connector = DatabaseConnector()

        #@st.cache_data
        def fetch_data_from_table():
            with open('scripts/sql/fetch_data.sql', 'r') as file:
                query = file.read()
            results = self.conn.execute_query(query)
            df = pd.DataFrame(results,columns = ["id_venda_tipo","id_produto","Produto","id_dn","DN","id_regional","Regional",
                                                "Volume Mercado","id_rtv","RTV","id_periodo","Volume 22/23","id_periodo2",
                                                "Volume 23/24","id_periodo3","Volume 24/25","id_periodo4","Volume Ano Safra+1 ACP (23/24)"]).reset_index()
            return df

        def return_reg_metas():
            with open('scripts/sql/fetch_reg_data.sql', 'r') as file:
                query = file.read()
            results = self.conn.execute_query(query)
            df = pd.DataFrame(results,columns = ["id_venda_tipo","id_produto","Produto","id_dn","DN","id_regional","Regional",
                                                "Volume Mercado","Volume 22/23","Volume 23/24","Volume Reg","Volume Reg Ano Safra+1 ACP (23/24)"]).reset_index()
            return df
        
        def return_product_prices():
            with open('scripts/sql/fetch_product_prices.sql', 'r') as file:
                query = file.read()
            results = self.conn.execute_query(query)
            df = pd.DataFrame(results,columns = ["id_price","id_produto","id_periodo","Preço"]).reset_index()
            return df
        
        product_prices = return_product_prices()

        product_prices['Preço'] = product_prices['Preço'].str.replace(',', '')
        product_prices['Preço'] = product_prices['Preço'].str.replace('$', '')
        product_prices['Preço'] =  product_prices['Preço'].astype(float)
            
        
        metas_reg_original_df = return_reg_metas()
        metas_reg_source = metas_reg_original_df [["id_produto","Produto","DN","Regional","Volume Reg"]]
        metas_reg_source.fillna(0,inplace=True)
        metas_reg_source["Volume Reg"] =  metas_reg_source["Volume Reg"].astype(float)

        st.title("Metas de RTVs - Sell Out")
        
        df_source = fetch_data_from_table()
        df_source.fillna(0,inplace=True)
        df_source["Volume 23/24"] =  df_source["Volume 23/24"].astype(float)
        df_source["Volume 24/25"] =  df_source["Volume 24/25"].astype(float)
        df_source["Volume 22/23"] =  df_source["Volume 22/23"].astype(float)
        df_source["Volume Ano Safra+1 ACP (23/24)"] =  df_source["Volume Ano Safra+1 ACP (23/24)"].astype(float)

        df = df_source
        
        df = df.round(2)
        
        dns_menu_dict={
            "menu_list":['TODAS','Cereais e F&V','Culturas Especiais', 'Centro Sul','Cerrados Leste','Cerrados Oeste',
                            'KAM','Sul']
        }
        dns_selection = option_menu ("Selecione a DN para filtrar",dns_menu_dict["menu_list"],default_index=0,
                                        menu_icon="map",
        orientation="horizontal",styles= { "container": {"padding": "0!important", "background-color": "#fafafa"},
        "nav-link": {"font-size": "15px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#143c4c"}}
        )

        if dns_selection == "TODAS":
            df_dn_filtered = df
            df_reg_filtered = df_dn_filtered
            metas_reg_dn_filtered = metas_reg_source
            metas_reg_reg_filtered = metas_reg_source
        
        else:
            df_dn_filtered = df[df["DN"] == dns_selection]
            metas_reg_dn_filtered = metas_reg_source[metas_reg_source["DN"] == dns_selection]

        
            regional_list = list(set(df_dn_filtered["Regional"]))
            regional_list.insert(0,"TODAS")

            select_dict = {
                'Cereais e F&V':regional_list,
                'Culturas Especiais':regional_list, 
                'Centro Sul':regional_list,
                'Cerrados Leste':regional_list,
                'Cerrados Oeste':regional_list,
                'KAM':regional_list,
                'Sul':regional_list
            }

            regional_selection = option_menu("Selecione a Regional",select_dict[dns_selection],  
                menu_icon="map", default_index=0, orientation="horizontal",
                styles= { "container": {"padding": "0!important", "background-color": "#fafafa"},
                "nav-link": {"font-size": "15px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#143c4c"}}
                    )
            if regional_selection == "TODAS":
                df_reg_filtered = df_dn_filtered
                df_reg_filtered.sort_values(by=["Produto","DN","Regional"],inplace=True)
                metas_reg_reg_filtered = metas_reg_dn_filtered
            else:
                df_reg_filtered = df_dn_filtered[df_dn_filtered["Regional"] == regional_selection]
                df_reg_filtered.sort_values(by=["Produto","DN","Regional"],inplace=True)
                metas_reg_reg_filtered = metas_reg_dn_filtered[metas_reg_dn_filtered["Regional"] == regional_selection]


        with st.expander('',expanded=True):
            col__x,col__y,col__z,col__1,col__2 = st.columns([0.05,0.6,0.1,0.1,0.1])
            with col__x:
                st.markdown(img_to_html('assets/kpi.png',50 ,-5, 10),
                            unsafe_allow_html=True)
            with col__y:
                st.header("Indicadores de Budgets 24/25 - Regionais - Sell Out")
            st.subheader("")
            st.subheader("Legenda")
            col__a,col__b,col__c,col__d,col__e,col__f,col__g,col__h = st.columns([0.2,0.01,0.2,0.01,0.2,0.05,0.2,0.05])

            with col__a:
                st.write("⚠️ Acima/Abaixo do Budget")

            with col__c:
                st.write("✅ Budget Proposto")
                
            st.subheader("")
            product_list = list(set(df_reg_filtered["Produto"]))
            product_list.sort()
            product_list.insert(0,"Todos")


            metas_regional_grouped = df_reg_filtered.groupby(["id_produto","Produto","DN","Regional"],as_index=False).agg(budget_used = pd.NamedAgg(column="Volume 24/25",aggfunc = "sum"))
            metas_reg_grouped = metas_reg_reg_filtered.merge(metas_regional_grouped,on = ["id_produto","Produto","DN","Regional"],how="inner")            

            metas_reg_grouped.rename(columns={"Volume Reg":"Budget Total","budget_used":"Budget Utilizado"},inplace=True)
            metas_reg_grouped["Budget Disponível"] = metas_reg_grouped["Budget Total"] - metas_reg_grouped["Budget Utilizado"]
            emoji_list = ["✅","⚠️"]
            conditions_metas_dns = (metas_reg_grouped["Budget Disponível"] == 0,
                                    metas_reg_grouped["Budget Disponível"] != 0)
            metas_reg_grouped["Check"] = np.select(conditions_metas_dns,emoji_list)

            metas_reg_grouped_with_products = metas_reg_grouped.merge(product_prices,on="id_produto", how = "left")
            
            metas_reg_grouped_with_products["Budget Total $"] = metas_reg_grouped_with_products["Budget Total"] * metas_reg_grouped_with_products["Preço"]
            metas_reg_grouped_with_products["Budget Utilizado $"] = metas_reg_grouped_with_products["Budget Utilizado"] * metas_reg_grouped_with_products["Preço"]

            metas_reg_grouped_with_products["Budget Disponível $"] = metas_reg_grouped_with_products["Budget Disponível"] * metas_reg_grouped_with_products["Preço"]
            #st.dataframe(metas_reg_grouped_with_products)


            col_x,col_y,col_z,col_a = st.columns(4)

            with col__a:
                st.write("R$ Budget Total para 24/25:")
                st.markdown(format_money(metas_reg_grouped_with_products["Budget Total $"].sum()), unsafe_allow_html=True)
                select_products_budget = st.selectbox(label="Selecione o Produto",options=product_list, key = "options_budget")

            with col__c:
                st.write("R$ Budget Preenchido para 24/25:")
                st.markdown(format_money(metas_reg_grouped_with_products["Budget Utilizado $"].sum()), unsafe_allow_html=True)

            with col__e:
                st.header("")
                st.write("R$ Saldo Budget para 24/25:")
                st.markdown(format_money(metas_reg_grouped_with_products["Budget Disponível $"].sum()), unsafe_allow_html=True)

            if select_products_budget == "Todos":
                products_grouped_product_rtv = metas_reg_grouped
                products_grouped_product_rtv.sort_values(by=["Produto","DN"],inplace=True)
                

            else:
                products_grouped_product_rtv = metas_reg_grouped[metas_reg_grouped["Produto"] == select_products_budget]
                products_grouped_product_rtv.sort_values(by=["Produto","DN"],inplace=True)
            

            """
            products_grouped = df_reg_filtered.groupby(["Produto","DN","Regional"],as_index=False).agg(budget_used=pd.NamedAgg(column='Volume 24/25', aggfunc='first'))

            products_grouped.rename(columns={"total_budget":"Budget Total","budget_avaliable":"Budget Utilizado", "budget_used":"Budget Disponível"},inplace=True)
            products_grouped["Budget Disponível"] = products_grouped["Budget Total"] - products_grouped["Budget Utilizado"]
            emoji_list = ["🔵","❌","✅"]
            products_grouped["Check"] = np.random.choice(emoji_list,size=len(products_grouped))

            if select_products_budget == "Todos":
                products_grouped_product = products_grouped
                products_grouped_product.sort_values(by=["Produto","DN","Regional"],inplace=True)
                

            else:
                products_grouped_product = products_grouped[products_grouped["Produto"] == select_products_budget]
                products_grouped_product.sort_values(by=["Produto","DN","Regional"],inplace=True)
            """

            numeric_formatter = JsCode("""
                function(params) {
                    var value = params.value;
                    return typeof value === 'number' ? new Intl.NumberFormat('pt-BR').format(value) : value;
                }
            """)

            gd_budget = GridOptionsBuilder.from_dataframe(products_grouped_product_rtv)
            
            gd_budget.configure_side_bar(True)
            gd_budget.configure_default_column(filterable=True,sortable=True)
            
            gd_budget.configure_grid_options(enableRangeSelection=True)
            gd_budget.configure_column("Budget Total",valueFormatter = numeric_formatter)
            gd_budget.configure_column("Budget Utilizado",valueFormatter = numeric_formatter)
            gd_budget.configure_column("Budget Disponível",valueFormatter = numeric_formatter)
            gd_budget.configure_column("id_produto",hide=True)



            gridoptions_budget = gd_budget.build()
            gridoptions_budget['alwaysShowHorizontalScroll'] = True
            gridoptions_budget['alwaysShowVerticalScroll'] = True
            gridoptions_budget['suppressHorizontalScroll'] = False
            gridoptions_budget['supressVerticalScroll'] = False

            
            gd_budget.configure_pagination(enabled=True,
                                            paginationAutoPageSize=False,
                                            paginationPageSize=100)
            
            
            grid_response_budget = AgGrid(products_grouped_product_rtv, editable=False,
                                    gridOptions=gridoptions_budget,
                                        update_mode=GridUpdateMode.VALUE_CHANGED,
                                        height = 450,
                                        allow_unsafe_jscode=True,
                                        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
                                        theme=AgGridTheme.MATERIAL,
                                        custom_css={
                                                    ".ag-theme-material .ag-root .ag-header .ag-header-cell": {
                                                        "font-size": "13px !important",  # Font size for header cells
                                                    },
                                                    ".ag-theme-material .ag-root .ag-body .ag-cell": {
                                                        "font-size": "12px !important",  # Font size for regular cells
                                                    },
                                                    "#gridToolBar": {
                                                        "padding-bottom": "0px !important",
                                                    }
                                            }

                                                

                                        )
            
            st.header("")
            st.divider()
            st.header("")

            a_col,b_col,c_col,d_col,e_col = st.columns([0.05,0.5,0.1,0.1,0.1])
            with a_col:
                st.markdown(img_to_html('assets/prancheta.png',50 ,-5, 10),
                            unsafe_allow_html=True)
            with b_col:
                st.header("Lista de Metas de Vendas - RTVs - Sell Out")
            st.subheader("")
            st.write("Insira abaixo as Metas referentes a cada Produto para cada um dos RTVs listados abaixo.")
            st.warning("Safra 23/24 atualizada até o dia 13/03/2024",icon="⚠️")
            st.error ("LALALA")
                
            #product_list = list(set(df_reg_filtered["Produto"]))
            #product_list.sort()
            #product_list.insert(0,"Todos")
            
            colx,coly,colz,cola = st.columns(4)
            with colx:
                product_selection = st.selectbox(label="Selecione o Produto",options=product_list, key = "targets_products")

            if product_selection == "Todos":
                df_produto_filtered = df_reg_filtered
                df_produto_filtered.sort_values(by=["Produto","DN","Regional"],inplace=True)
                metas_reg_grouped_product_filtered = metas_reg_grouped
                

            else:
                df_produto_filtered = df_reg_filtered[df_reg_filtered["Produto"] == product_selection]
                df_produto_filtered.sort_values(by=["Produto","DN","Regional"],inplace=True)
                metas_reg_grouped_product_filtered = metas_reg_grouped[metas_reg_grouped["Produto"] == product_selection]

            metas_reg_grouped_product_filtered_mercado_total = metas_reg_grouped_product_filtered["Budget Total"].sum()
            metas_reg_grouped_product_filtered_mercado_24_25 = metas_reg_grouped_product_filtered["Budget Utilizado"].sum()
            metas_reg_grouped_product_filtered_mercado_avalibale = metas_reg_grouped_product_filtered["Budget Disponível"].sum()
            with coly:
                st.write("Budget Total para 24/25:")
                st.markdown(format_float(metas_reg_grouped_product_filtered_mercado_total), unsafe_allow_html=True)
            with colz:
                st.write("Volume 24/25:")
                st.markdown(format_float(metas_reg_grouped_product_filtered_mercado_24_25), unsafe_allow_html=True)
            with cola:
                st.write("Budget Disponível para 24/25:")
                st.markdown(format_float(metas_reg_grouped_product_filtered_mercado_avalibale), unsafe_allow_html=True)


            df_rtv_filtered = df_produto_filtered.merge(product_prices[["id_produto","Preço"]], on = "id_produto",how="left")

            df_rtv_filtered.rename(columns={"Volume Mercado":"Mercado Potencial (Volume)"},inplace=True)
            df_rtv_filtered = df_rtv_filtered[["id_produto","Produto","id_dn","DN","id_regional","Regional","id_rtv","RTV","Mercado Potencial (Volume)","id_periodo","Volume 22/23","id_periodo2",
                                                "Volume 23/24","id_periodo3","Volume 24/25","id_periodo4","Volume Ano Safra+1 ACP (23/24)","Preço"]]

            gd = GridOptionsBuilder.from_dataframe(df_rtv_filtered)

            cell_style_js = JsCode("""
                        function(params) {
                            var value = Number(params.value);
                            if (value > 0) {
                                return {
                                    'color': 'green'
                                };
                            } else if (value < 0) {
                                return {
                                    'color': 'red'
                                };
                            }
                            // default styling if value is 0
                            return {};
                        }
                    """)
            cell_style_percentage_js = JsCode("""
                function(params) {
                    var value = parseFloat(params.value.replace('%', '').replace(',', '.'));  // Parse the percentage value

                    if (!isNaN(value)) {
                        if (value > 0) {
                            return {'color': 'green'};
                        } else if (value < 0) {
                            return {'color': 'red'};
                        }
                    }

                    return null;  // Default styling
                }
            """)
                                        

            # Define formatter for percentage columns
            
            percentage_formatter = JsCode("""
                function(params) {
                    var value = params.value;
                    if (typeof value === 'number') {
                        return value.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' %';
                    } else {
                        return value;
                    }
                }
            """)

            numeric_formatter_money = JsCode("""
                    function(params) {
                        var value = params.value;
                        return typeof value === 'number' ? 'R$ ' + new Intl.NumberFormat('pt-BR').format(value) : value;
                    }
                """)

            
            var_22_25 = {"headerName": "Var 24/25 - 22/23", "field": "var_volume_22_25", "cellStyle": cell_style_js, "valueFormatter":numeric_formatter,
                            "valueGetter": "Number(data['Volume 24/25']) - Number(data['Volume 22/23'])", 
                            "valueSetter": "data.var_volume_22_25 = params.newValue; return true;","cellDataType":"number","type": "rightAligned","hide":"True"}
            
            
            var_23_25 = {"headerName": "Var 24/25 - 23/24", "field": "var_volume_23_25", "cellStyle": cell_style_js, "valueFormatter":numeric_formatter,
                            "valueGetter": "Number(data['Volume 24/25']) - Number(data['Volume 23/24'])", 
                            "valueSetter": "data.var_volume_23_25 = params.newValue; return true;","cellDataType":"number","type": "rightAligned"}
            
            net_24_25 = {"headerName": "Net 24/25", "field": "net_24_25", "valueFormatter":numeric_formatter_money,
                            "valueGetter": "Math.round(Number(data['Volume 24/25']) * Number(data['Preço']))", 
                            "valueSetter": "data.var_volume_23_25 = params.newValue; return true;","cellDataType":"number","type": "rightAligned"}
            
            perc_var_22_25 = {
                "headerName": "(%)Var 24/25 - 22/23",
                "field": "perc_var_volume_22_25",
                "cellStyle": cell_style_percentage_js,
                "valueFormatter": percentage_formatter,
                "valueGetter": "(Number(data['Volume 22/23']) !== 0) ? (((Number(data['Volume 24/25']) / Number(data['Volume 22/23'])) - 1) * 100).toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' %' : 'NaN'",
                "valueSetter": "data.perc_var_volume_22_25 = params.newValue.replace('.', '').replace(',', '.').replace(' %', ''); return true;",
                "cellDataType": "string",
                "type": "rightAligned",
                "hide":"True"
            }

            perc_var_23_25 = {
                "headerName": "(%)Var 24/25 - 23/24",
                "field": "perc_var_volume_23_25",
                "cellStyle": cell_style_percentage_js,
                "valueFormatter": percentage_formatter,
                "valueGetter": "(Number(data['Volume 23/24']) !== 0) ? (((Number(data['Volume 24/25']) / Number(data['Volume 23/24'])) - 1) * 100).toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' %' : 'NaN'",
                "valueSetter": "data.perc_var_volume_23_25 = params.newValue.replace('.', '').replace(',', '.').replace(' %', ''); return true;",
                "cellDataType": "string",
                "type": "rightAligned"
            }

            mkt_share_23_24 = {
                "headerName": "(%)MKT Share 23/24",
                "field": "mkt_share_23_24",
                "valueFormatter": percentage_formatter,
                "valueGetter": "(Number(data['Mercado Potencial (Volume)']) !== 0) ? (((Number(data['Volume 23/24']) / Number(data['Mercado Potencial (Volume)']))) * 100).toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' %' : 'NaN'",
                "valueSetter": "data.mkt_share_23_24 = params.newValue.replace('.', '').replace(',', '.').replace(' %', ''); return true;",
                "cellDataType": "string",
                "type": "rightAligned"
            }
            
            mkt_share_24_25 = {
                "headerName": "(%)MKT Share 24/25",
                "field": "mkt_share_24_25",
                "valueFormatter": percentage_formatter,
                "valueGetter": "(Number(data['Mercado Potencial (Volume)']) !== 0) ? (((Number(data['Volume 24/25']) / Number(data['Mercado Potencial (Volume)']))) * 100).toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2}) + ' %' : 'NaN'",
                "valueSetter": "data.mkt_share_24_25 = params.newValue.replace('.', '').replace(',', '.').replace(' %', ''); return true;",
                "cellDataType": "string",
                "type": "rightAligned"
            }

            var_mkt_share_23_25 = {
                    "headerName": "(%)Var MKT Share 24/25 - 23/24",
                    "field": "var_mkt_share_23_25",
                    "cellStyle": cell_style_percentage_js,
                    "valueFormatter": percentage_formatter,
                    "valueGetter": "(Number(data['Mercado Potencial (Volume)']) !== 0) ? ((((Number(data['Volume 24/25']) / Number(data['Mercado Potencial (Volume)'])) - (Number(data['Volume 23/24']) / Number(data['Mercado Potencial (Volume)']))) * 100)).toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 3}) + ' %' : 'NaN'",
                    "valueSetter": "data.var_mkt_share_23_25 = params.newValue.replace('.', '').replace(',', '.').replace(' %', ''); return true;",
                    "cellDataType": "string",
                    "type": "rightAligned"
                }
            

            
            gd.configure_side_bar(True)
            gd.configure_default_column(filterable=True,sortable=True)
            gd.configure_selection(selection_mode="multiple",
                                        rowMultiSelectWithClick =True,
                                        )
            
            gd.configure_column("Mercado Potencial (Volume)",valueFormatter = numeric_formatter)
            gd.configure_column("Volume 24/25", editable=True, headerClass = "custom-header",valueFormatter = numeric_formatter)
            gd.configure_column("Volume 23/24",valueFormatter = numeric_formatter)
            gd.configure_column("Volume 22/23",valueFormatter = numeric_formatter,hide=True)
            gd.configure_column("Volume Ano Safra+1 ACP (23/24)",valueFormatter = numeric_formatter)





            gd.configure_column("index", hide=True)
            gd.configure_column("id_produto", hide=True)
            gd.configure_column("id_dn", hide=True)
            gd.configure_column("id_regional", hide=True)
            gd.configure_column("id_rtv", hide=True)
            gd.configure_column("id_periodo", hide=True)
            gd.configure_column("id_periodo2", hide=True)
            gd.configure_column("id_periodo3", hide=True)
            gd.configure_column("id_periodo4", hide=True)
            gd.configure_column("Preço",hide=True)


            



            gd.configure_grid_options(enableRangeSelection=True)
            gridoptions = gd.build()
            gridoptions['alwaysShowHorizontalScroll'] = True
            gridoptions['alwaysShowVerticalScroll'] = True
            gridoptions['suppressHorizontalScroll'] = False
            gridoptions['supressVerticalScroll'] = False

            gd.configure_pagination(enabled=True,
                                            paginationAutoPageSize=False,
                                            paginationPageSize=100)
            
            gridoptions['columnDefs'].extend([net_24_25,var_23_25,perc_var_23_25,var_22_25,perc_var_22_25,mkt_share_23_24,mkt_share_24_25,var_mkt_share_23_25])


            grid_responde = AgGrid(df_rtv_filtered, editable=False,
                                    gridOptions=gridoptions,
                                        update_mode=GridUpdateMode.VALUE_CHANGED,
                                        
                                        height = 320,
                                        allow_unsafe_jscode=True,
                                        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
                                        theme=AgGridTheme.MATERIAL,
                                        enableRangeSelection=True,
                                        custom_css={
                                                    ".ag-theme-material .ag-root .ag-header .custom-header": {
                                                    "background-color": "gold !important",
                                                    "color": "black !important",
                                                    "font-size": "13px !important",
                                                    },  
                                                    ".ag-theme-material .ag-root .ag-header .ag-header-cell": {
                                                        "font-size": "13px !important",  # Font size for header cells
                                                    },
                                                    ".ag-theme-material .ag-root .ag-body .ag-cell": {
                                                        "font-size": "12px !important",  # Font size for regular cells
                                                    },
                                                    "#gridToolBar": {
                                                        "padding-bottom": "0px !important",
                                                    }
                                            },

                                        )
            
            ag_edited = grid_responde["data"]
            merged = df.merge(ag_edited,indicator=True,how="outer")
            merged = merged[merged['_merge'] == 'right_only']
            merged.drop(columns=["_merge"],inplace=True)
            merged.drop(columns=["index"],inplace=True)
            
            if not merged.empty:
                st.error("Você fez alterações, não se esqueça de Enviar e Salvar no botão mais abaixo!")
            col__p,col__q = st.columns([0.7,0.3])
            with col__p:
                st.markdown("<h5>Clique no Botão ao lado para Enviar e Salvar as Alterações!</h5>",unsafe_allow_html=True)
            with col__q:
                if st.button("Enviar e Salvar!",type="primary"):
                    
                    with st.spinner("Enviando os dados!"):
                        for index, row in merged.iterrows():
                            update_query = f"""
                            INSERT INTO dbo.fato_volumes_metas_rtv
                            (id_venda_tipo, id_produto, id_dn, id_regional, id_rtv, id_periodo, volume_rtv, is_valid)
                            VALUES (1, {row['id_produto']}, {row['id_dn']}, {row['id_regional']}, {row['id_rtv']}, 3, {row['Volume 24/25']}, true)
                            ON CONFLICT (id_venda_tipo, id_produto, id_dn, id_regional, id_rtv, id_periodo)
                            DO UPDATE SET
                                volume_rtv = EXCLUDED.volume_rtv,
                                is_valid = EXCLUDED.is_valid,
                                updated_at = now();
                        """
                            self.conn.execute_update(update_query)
                        st.success("Dados enviados!")
                        time.sleep(3)
                    
                        st.rerun()
        
        st.subheader("Expanda a seção abaixo para conferir suas alterações:")
        with st.expander('',expanded=False):
            st.dataframe(merged[["Produto","DN","Regional","RTV","Volume 24/25"]].set_index(df.columns[3]), use_container_width = True)
            

    # INSERT INTO dbo.fato_volumes_metas_rtv 
    # (id_produto, id_dn, id_regional, id_rtv, id_periodo, volume_rtv, is_valid)
    # VALUES ({row['id_produto']}, {row['id_dn']}, {row['id_regional']}, {row['id_rtv']}, 3, {row['Volume 24/25']}, true)
