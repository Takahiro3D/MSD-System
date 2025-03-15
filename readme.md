# SMD system

１自由度質量ばねダンパーシステム

## Build

``` bash
docker image build -t streamlit_server .
```

## Launch

### Docker

``` bash
docker container run -it --rm -p 8501:8501 -v ./src:/src --name streamlit_vib streamlit_server streamlit run vib.py
```

options

- -i,--interactive : Keep STDIN open even if not attached
  標準入力を開いたままにする
- -t, --tty : Allocate a pseudo-TTY(teletype)
  ターミナルを割り当てる
- -d, --detach : Run container in background and print container ID

`-itd`オプションでdockerイメージがバッググラウンド実行される。  
同時に標準入力と疑似テレタイプがオープンし対話操作が可能になる。

`--rm`オプションで終了時にイメージ自動削除

### Docker compose

``` bash
docker compose up
```

Run background

``` bash
docker compoe up -d
```

Stop container

``` bash
docker-compose down
```
