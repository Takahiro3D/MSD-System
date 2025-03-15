FROM python:3.10.13-slim-bullseye

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git && \
    rm -rf /var/lib/apt/lists/* &&\
    pip install -U pip && \
    pip install streamlit && \
    pip install plotly && \
    pip install sympy

WORKDIR /src/

EXPOSE 8501

CMD ["/bin/bash"]
