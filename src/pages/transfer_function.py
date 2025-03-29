import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pathlib
import logging

import control as ctrl

# ロギングの設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# ページ設定
st.set_page_config(
    page_title="伝達関数",
    layout="wide",
)

# ヘッダ
st.markdown('# 1自由度 質量 ばね ダンパーモデル')
st.markdown('## 伝達関数')

# モデル画像
image_path = pathlib.Path("../resource/MSD-System.png").resolve()
# logger.debug(f"画像の絶対パス: {image_path}")
# st.image(image_path, caption="モデル画像", use_container_width =False, )

# Show image in center
col1, col2, col3 = st.columns([1, 2, 1])  # 真ん中のカラムを広めに
with col2:
    st.image(image_path, use_container_width=True)  # 画像を中央カラムに配置

st.write("## 運動方程式")
st.latex(r"m\ddot{x}+ c\dot{x} + kx = F cos{\omega t}")

m = st.number_input("m: ばねの質量[kg]", value=5.0)
k = st.number_input("k: ばね係数[N/m]", value=100.0)
c = st.number_input("c: 減衰係数[N/(m/s)]", value=10.0)

# Not woking
# st.markdown(
#     "<p style='text-align: center;'><img src='/resource/model.png' width='300'></p>",
#     unsafe_allow_html=True
# )

# 式
st.write("## 伝達関数")
st.latex(r'G(s) = \frac{1}{ms^2 + cs + k}')

numerator = [1]
denominator = [m, c, k]
G = ctrl.TransferFunction(numerator, denominator)


st.write("### ボード線図")

mag, phase, omega = ctrl.bode_plot(G, dB=True, omega_limits=(0.1, 100), omega_num=500, plot=False)

# line_chartで対数グラフを表示できない
# データの作成
# df = pd.DataFrame()
# df['Frequency_Hz'] = omega
# df['Magnitude_dB'] = 20 * np.log10(mag)
# df['Phase_deg'] = np.degrees(phase)
# 
# logger.debug(f"{df=}")
# 
# グラフ描画
# st.line_chart(df, x='Frequency_Hz', y='Magnitude_dB')
# st.line_chart(df, x='Frequency_Hz', y='Phase_deg')

# pyplotで描画
# 現状日本語フォント非対応
# for font in fm.findSystemFonts():
#     logger.info(fm.FontProperties(fname=font).get_name())
# plt.rcParams['font.family'] = 'DejaVu Serif'

fig, axs = plt.subplots(2, 1, figsize=(10, 8))

# ゲイン線図
axs[0].semilogx(omega, 20 * np.log10(mag))
axs[0].grid(True)
axs[0].set_title("Gain diagram")
axs[0].set_ylabel("Magnitude [dB]")

# 位相線図
axs[1].semilogx(omega, np.degrees(phase))
axs[1].grid(True)
axs[1].set_title("Phase diagram")
axs[1].set_xlabel("Frequency(rad/s)")
axs[1].set_ylabel("Phase [deg]")

# Streamlitにプロットを表示
st.pyplot(fig)


st.markdown("### sin波入力に対する時間応答")

st.latex(r'f(t) = F\sin(\omega t)')

F = st.number_input("F: 外力[N]", value=10.0)
omega = st.number_input("ω: 外力振動角速度[rad/s]", value=5.0)

time = np.linspace(0.0, 5.0, 1000)
U = F * np.sin( omega * time)
t, y = ctrl.forced_response(G, T=time, U=U)
v = np.gradient(y, t)

# 時間応答図のプロット
fig_time, axes = plt.subplots(2, 1, figsize=(10, 8))

# fig_time.suptitle("Time response diagram")

axes[0].plot(t, y)
axes[0].grid(True)
axes[0].set_title("Time response diagram")
axes[0].set_ylabel("Displacement [m]")

axes[1].plot(t, v)
axes[1].grid(True)
axes[1].set_xlabel("Time [sec]")
axes[1].set_ylabel("Velocity [m/s]")

st.pyplot(fig_time)

