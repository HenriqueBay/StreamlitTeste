with container:
    nomecli, cpfcli, atendicli, nomepromot, statusneg = st.columns(5)

    with nomecli:
        option7 = st.selectbox(
            "Nome cliente",
            ("Selecionar...", "Teste1", "Teste2", "Teste3"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )

    with cpfcli:
        option8 = st.selectbox(
            "CPF Cliente",
            ("Selecionar...", "Teste11", "Teste2", "Teste3"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )

    with atendicli:
        option9 = st.selectbox(
            "Atendimento",
            ("Selecionar...", "Teste111", "Teste2", "Teste3"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )
        with nomepromot:
            option0 = st.selectbox(
                "Nome Promotor",
                ("Selecionar...", "Teste1111", "Teste2", "Teste3"),
                label_visibility=st.session_state.visibility,
                disabled=st.session_state.disabled,
            )
            with statusneg:
                option10 = st.selectbox(
                    "Status Negociação CP 24/25",
                    ("Selecionar...", "Teste1", "Teste21", "Teste3"),
                    label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                )


# Defining the options for selectboxes
options = ["Opção 1", "Opção 2", "Opção 3", "Opção 4", "Opção 5"]

# Creating the table structure
table = st.table()

# Adding rows to the table
for i in range(15):
    # Creating a unique key for each text input
    key = f"text_input_{i}"

    # Creating the first column (selectbox)
    selectbox_value = st.selectbox(
        label="Selecione", options=options, index=0, key=f"selectbox_{i}")

    # Creating the second column (text input)
    inputbox_value = st.text_input(label="Digite um valor", key=key)


# Displaying the table
st.iframe(table)



-----------------------------------------------------------------------------------------------------------------------


import streamlit as st
from home import *
from utils import *


st.set_page_config(page_title="Tracking EIB", layout="wide")
st.title("Tracking EIB")
st.markdown("""<h4 style='text-align: left; color: black;'>
                    Não repara a bagunça, estamos em construção! :3</h4>""", unsafe_allow_html=True)


load_bootstrap()


# Definindo a visibilidade e desabilitação dos elementos
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

# Criando o container e injetando código HTML com markdown
container = st.container()


# Incluindo o arquivo CSS
with open("main.css") as f:
    st.write(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Colunas e caixas de seleção dentro do container
with container:
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        option = st.selectbox(
            "DN",
            ("Selecionar...", "Cerrados Leste",
             "Cerrados Oeste", "KAM", "Centro Sul"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )

    with col2:
        option2 = st.selectbox(
            "Regional",
            ("Selecionar...", "Teste1", "Teste2", "Teste3"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )

    with col3:
        option3 = st.selectbox(
            "Distrito",
            ("Selecionar...", "Teste1", "Teste2", "Teste3"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )

    with col4:
        option4 = st.selectbox(
            "Cod. RTV",
            ("Selecionar...", "Teste1", "Teste2", "Teste3"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )

    with col5:
        option5 = st.selectbox(
            "Atendimento",
            ("Selecionar...", "Teste1", "Teste2", "Teste3"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )

    with col6:
        option6 = st.selectbox(
            "Cliente",
            ("Selecionar...", "Rafael Schmidt",
             "Jaqueline Saldanha", "Diogo Dalaqua"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )

# Fechando a tag div do container
container.markdown("</div>", unsafe_allow_html=True)
container.markdown("<hr>", unsafe_allow_html=True)


with container:
    nomecli, cpfcli, atendicli, nomepromot, statusneg = st.columns(5)

    with nomecli:
        option7 = st.selectbox(
            "Nome cliente",
            ("Selecionar...", "Teste1", "Teste2", "Teste3"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )

    with cpfcli:
        option8 = st.selectbox(
            "CPF Cliente",
            ("Selecionar...", "Teste11", "Teste2", "Teste3"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )

    with atendicli:
        option9 = st.selectbox(
            "Atendimento",
            ("Selecionar...", "Teste111", "Teste2", "Teste3"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )
        with nomepromot:
            option0 = st.selectbox(
                "Nome Promotor",
                ("Selecionar...", "Teste1111", "Teste2", "Teste3"),
                label_visibility=st.session_state.visibility,
                disabled=st.session_state.disabled,
            )
            with statusneg:
                option10 = st.selectbox(
                    "Status Negociação CP 24/25",
                    ("Selecionar...", "Teste1", "Teste21", "Teste3"),
                    label_visibility=st.session_state.visibility,
                    disabled=st.session_state.disabled,
                )
container.markdown("<hr>", unsafe_allow_html=True)

# Defining the options for selectboxes

options = ["Selecione..."]


# Adding rows to the table
for i in range(15):
    # Creating a unique key for each text input
    key = f"text_input_{i}"

    # Creating the first column (selectbox)
    selectbox_value = st.selectbox(
        label="Selecione", options=options, index=0, key=f"selectbox_{i}")

    # Creating the second column (text input)
    inputbox_value = st.text_input(label="Digite um valor", key=key)



.meu-container {
    background-color: rgb(11, 134, 40);
    /* Cor de fundo do container */
    color: white;
    /* Cor do texto */
    padding: 10px;
    /* Padding interno */
    border-radius: 5px;
    /* Borda arredondada */
}

.container {
    /* Estilos para o container */
    background-color: #d01212;
    padding: 10px;
}

.stApp {
    background-color: blueviolet;
}

#portal {
    background-color: rgb(226, 43, 43);
}

.element-container {
    background-color: blueviolet;
}

.block-container {
    background-color: rgb(110, 226, 43);
}

.st-emotion-cache-6qob1r {
    background-color: rgb(43, 58, 226);
}

.st-emotion-cache-0 {
    background-color: rgb(201, 11, 11);
}

.st-emotion-cache-1mj1rsm {
    background-color: rgb(152, 19, 19);
}

.st-emotion-cache-1l269bu {
    background-color: rgb(198, 214, 19);
}


.st-ak {
    background-color: aqua;
}