import streamlit as st
from home import *
from utils import *


import streamlit as st

# Título da página
st.title("Arrastão de Vendas Brasil - Crop Protection")

# Cria um container centralizado
with st.container():
    # Adiciona texto informativo
    st.write("""
        Fonte de informações: 

        **Informação**                  **Descrição**                                                               **Fonte**

        * Indice Tecnológico FC2 -    - Indice utilizado para o calculo do Potencial do cliente (sem Roundup)       -   - BI
        * Escoamento (Sell Out)  -    - Valor de escoamento realizado nas safras anteriores                         -   - Pegasus (Painel de Escoamento)
        * Compra (Sell In)       -    - Valor de escoamento realizado nas safras anteriores                         -   - SAP Hana (OTB)
        * Preço Budget 23/24 FC2 -    - Preço net que será usado para construção do  valor Negociação Produtos BRL  -   - Sales Plan
        * Roundup                -    - Na analise na Aba – Arrastão de Vendas Vol. não sera precificado            -   - 
        * Carteira EIB 23/24     -    - Clientes selecionandos para a Experência Integrada Bayer                    -   - Field Marketing

    Antes de iniciar o preenchimento da planilha , é importante ressaltar que como padrão, todas as células editáveis são as células em amarelo. (Retirar)""")
st.write("""

        **Como utilizar?**

        **Aba – Arrastão de Venda BRL**
        
        * Preencher o nome completo de cada Promotor (Coluna G)
        * Revisar e ajustar caso necessáro ou selecionar qual tipo de Acesso do cliente – Venda Direta ou Venda Indireta (Coluna K)
        * Revisar o Sell Out + Sell In identificado da Safra 22/23 - Campo editável para revisão e ajuste caso necessário (Coluna M)
        * Selecionar o Status da Negociação 22/23  – Se a negociação está: Não iniciado; Em negociação, Fechado; Perdido (Coluna Q)
        * Preencher com a data que está sendo feita a atualização desta planilha (Coluna R)
     
        **Aba – Arrastão de Venda Vol.**

        * Selecionar o produto e volume para cada cliente Safra 23.24 (Coluna N em diante)
        * Selecionar o produto e volume previsto para cada cliente Safra 24/25 (Coluna P em diante)
    Checar barra de rolagem nos campos de informação!""")

# Formatação do container (opcional)
st.markdown("""
        <style>
            .container {
                border: 1px solid #ddd;
                padding: 20px;
                border-radius: 10px;
                width: 80%;
                margin: 0 auto;
            }
        </style>
    """, unsafe_allow_html=True)
