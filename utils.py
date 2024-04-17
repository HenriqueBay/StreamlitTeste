import base64
from pathlib import Path

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

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def img_to_html(img_path,width, posX, posY):
    img_html = "<img src='data:image/png;base64,{}' width='{}' style='horizontal-align:middle;margin:{}px {}px'>".format(
        img_to_bytes(img_path),
        width,
        posX,
        posY
    )
    return img_html
