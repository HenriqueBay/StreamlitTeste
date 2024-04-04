#!/bin/bash
killall -s SIGKILL streamlit
tmux kill-server
sudo rm -rf /hub/