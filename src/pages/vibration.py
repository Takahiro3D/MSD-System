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
    page_title="強制振動",
    layout="wide",
)

# ヘッダ
st.markdown('# 1自由度 質量 ばね ダンパーモデル  強制振動')

# モデル画像
image_path = pathlib.Path("../resource/MSD-System.png").resolve()
# logging.debug(f"画像の絶対パス: {image_path}")
# st.image(image_path, caption="モデル画像", use_container_width =False, )

# Show image in center
col1, col2, col3 = st.columns([1, 2, 1])  # 真ん中のカラムを広めに
with col2:
    st.image(image_path, use_container_width=True)  # 画像を中央カラムに配置

st.write("運動方程式")
st.latex(r"m\ddot{x}+ c\dot{x} + kx = F cos{\omega t}")

m = st.number_input("m: ばねの質量[kg]", value=5.0)
k = st.number_input("k: ばね係数[N/m]", value=100.0)
c = st.number_input("c: 減衰係数[N/(m/s)]", value=10.0)

F = st.number_input("F: 外力[N]", value=10.0)
omega = st.number_input("ω: 外力振動角速度[rad/s]", value=5.0)

# Not woking
# st.markdown(
#     "<p style='text-align: center;'><img src='/resource/model.png' width='300'></p>",
#     unsafe_allow_html=True
# )

# 式
st.write("定常状態の一般解")
st.latex(r'x = \frac{f(\omega_0^2 - \omega^2)}{(\omega_0^2 - \omega^2)^2 + 4\omega^2\gamma^2}\cos(\omega t) + \frac{2f\omega\gamma}{(\omega_0^2 - \omega^2)^2 + 4\omega^2\gamma^2}\sin(\omega t)')
st.latex(r'(\omega_0 = \sqrt{\frac{k}{m}}, \gamma=\frac{c}{2m}, f=\frac{F}{m})')

# 定義域の指定
time = np.linspace(0.0, 3.0, 1000)

displacement, amplitude, phase = msd_system.calc_displacement_with_vibration(m, k, c, F, omega, time)

st.write(f"振幅: {amplitude:.3f}[m]")
st.write(f"位相: {phase:.3f}[rad]")

# データの作成
df = pd.DataFrame()
df['Time_sec'] = time
df['Displacement_m'] = displacement

# グラフ描画
st.line_chart(df, x='Time_sec', y='Displacement_m')
