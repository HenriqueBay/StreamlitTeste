from utils import *


class home():
    def __init__(self) -> None:
        pass

    def display_home(self):
        st.title("Julio lindo")
        st.markdown("""<h4 style='text-align: left; color: black;'>
                    Escolha no menu acima os parâmetros para filtrar o cliente</h4>""", unsafe_allow_html=True)
