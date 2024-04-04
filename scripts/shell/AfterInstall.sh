#!/bin/bash
cd /mkt-hub/
mkdir tmp
cd /mkt-hub/
source /hub-env/bin/activate
pip install -r requirements.txt
tmux new -d -s st_session 'streamlit run app.py'