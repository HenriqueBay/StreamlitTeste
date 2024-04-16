import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, AgGridTheme, GridUpdateMode, GridOptionsBuilder, AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode
import os
import time
from streamlit_option_menu import option_menu
import hydralit_components as hc
from streamlit_extras.metric_cards import style_metric_cards
import base64
from st_aggrid.shared import JsCode
from pathlib import Path
import pymysql


def format_float(x):
    x = '{:,.0f}'.format(x).replace(",", ".")
    html_x = f'''
    <p style="color:black; background-color:#F0F2F6; padding: 7px; border-radius: 7px;">{x}</p>
    '''
    return html_x

def format_money(x):
    x = 'R$ {:,.0f}'.format(x).replace(",", ".")
    html_x = f'''
    <p style="color:black; background-color:#F0F2F6; padding: 7px; border-radius: 7px;">{x}</p>
    '''
    return html_x

def load_bootstrap():
    return st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def img_to_html(img_path,width, posX, posY):
    load_bootstrap()
    img_html = "<img src='data:image/png;base64,{}' width='{}' style='horizontal-align:middle;margin:{}px {}px'>".format(
      img_to_bytes(img_path),
      width,
      posX,
      posY
    )
    return img_html
