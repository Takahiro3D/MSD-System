import streamlit as st
import numpy as np
import pandas as pd
import pathlib
import logging

import msd_system

# ロギングの設定
logging.basicConfig(level=logging.INFO)

# ページ設定
st.set_page_config(
    page_title="減衰運動",
    layout="wide",
)

# ヘッダ
st.markdown('# 1自由度 質量 ばね ダンパーモデル')

st.write("以下のような1自由度の質量-ばね-ダンパーモデルシステムについてのまとめ")

# モデル画像
image_path = pathlib.Path("../resource/MSD-System.png").resolve()
# logging.debug(f"画像の絶対パス: {image_path}")
# st.image(image_path, caption="モデル画像", use_container_width =False, )

# Show image in center
col1, col2, col3 = st.columns([1, 2, 1])  # 真ん中のカラムを広めに
with col2:
    st.image(image_path, use_container_width=True)  # 画像を中央カラムに配置
    st.markdown(
        "出典: [質量-ばね-ダンパーシステムの運動を求める](https://tajimarobotics.com/damped-mass-spring-system/) ")

# Not woking
# st.markdown(
#     "<p style='text-align: center;'><img src='/resource/model.png' width='300'></p>",
#     unsafe_allow_html=True
# )

# https://tajimarobotics.com/damped-mass-spring-system-example/


st.markdown("""
- damping: 外力なしの減衰運動
- vibration: 振動入力時の定常状態の運動
- transfer functiohn: 伝達関数とボード線図
""")

