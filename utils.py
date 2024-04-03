import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, AgGridTheme, GridUpdateMode, GridOptionsBuilder, ColumnsAutoSizeMode
import os
import time
from streamlit_option_menu import option_menu
import hydralit_components as hc
from streamlit_extras.metric_cards import style_metric_cards
import base64
from st_aggrid.shared import JsCode
from pathlib import Path


def kpi(box_color, font_color, fontsize,text_font_size ,align, icon, text, value):
    if box_color == "good":
        wch_colour_box = (137,211,41)
    elif box_color == "bad":
        wch_colour_box = (255,49,98)
    if font_color == "black":
        wch_colour_font = (0,0,0)
    elif font_color == "white":
        wch_colour_font = (255,255,255)
    fontsize = fontsize
    valign = align
    iconname = icon
    sline = text
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    i = value

    htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                                {wch_colour_box[1]}, 
                                                {wch_colour_box[2]},1); 
                            color: rgb({wch_colour_font[0]}, 
                                    {wch_colour_font[1]}, 
                                    {wch_colour_font[2]}, 1); 
                            font-size: {fontsize}px; 
                            border-radius: 7px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:25px;'>
                            <i class="{iconname}"></i> {i}
                            </style><BR><span style='font-size: {text_font_size}px; 
                            margin-top: 10;'>{sline}</style></span></p>"""

    return st.markdown(lnk + htmlstr, unsafe_allow_html=True)


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
