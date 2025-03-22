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
st.markdown('## 減衰運動')

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

st.write("## 運動方程式")
st.latex(r"m\ddot{x}+ c\dot{x} + kx = 0")

m = st.number_input("m: ばねの質量[kg]", value=5.0)
k = st.number_input("k: ばね係数[N/m]", value=100.0)
c = st.number_input("c: 減衰係数[N/(m/s)]", value=10.0)

x0 = st.number_input("x0: 初期変位量[m]", value=0.1)
# x'0 初期速度[m/s] は0.0固定

system = msd_system.System(m, c, k, x0)
system.solve()

st.write("## システム")

if system.name() == "Overdamped System":
    st.write("過減衰システム")
    st.write("変位x(t)の一般解")
    st.latex(r'x(t) = C_1 e^{\lambda_1 t} + C_2 e^{\lambda_2 t}')
    st.write("C1とC2は任意定数")
elif system.name() == "Underdamped System":
    st.write("不定減衰システム")
    st.write("変位x(t)の一般解")
    # lambda = gumma(c/2m) +- i*omega
    # st.latex(r'x(t) = e^{-\frac{c}{2m}t}(A\cos{\omega t} + B\sin{\omega t})')
    st.latex(r'x(t) = Ce^{-\frac{c}{2m}t}\cos(\omega t + \phi)')
    st.write("Cとφは任意定数")
else:
    st.write("臨海減衰システム")
    st.write("変位x(t)の一般解")
    # st.latex(r'x(t) = e^{-\frac{c}{2m}t}')
    st.latex(r'x(t) = (A_t+B)e^{-\frac{c}{2m}t}')
    st.write("AとBは任意定数")

# 定義域の指定
time = np.linspace(0.0, 5.0, 100)

# データの作成
df = pd.DataFrame()
df['Time_sec'] = time
df['Displacement_m'] = system.displacement(time)
df['Velocity_m/s'] = system.velocity(time)

logging.debug(f"{df=}")

# グラフ描画
# "[]" cannot be used
st.line_chart(df, x='Time_sec', y='Displacement_m')
st.line_chart(df, x='Time_sec', y='Velocity_m/s')
