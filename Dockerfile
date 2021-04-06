FROM ubuntu:18.04
RUN apt-get -y update \
  && apt-get -y upgrade \
  && apt-get install -y locales curl python3-distutils \
  && apt-get install -y unzip\
  && apt-get install -y openjdk-8-jdk \
  && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
  && python3 get-pip.py \
  && pip install -U pip \
  && pip install psycopg2-binary \
  && pip3 install tabula-py \
  && mkdir /code\
  && rm -rf /var/lib/apt/lists/* \
  && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8\
  && rm get-pip.py


ENV LANG en_US.utf8
WORKDIR /code
ADD requirements.txt /code
# requirements.txtからパッケージのインストール
RUN pip install -r requirements.txt

# matplotlibで日本語を使うための設定
WORKDIR /
RUN curl -L  "https://moji.or.jp/wp-content/ipafont/IPAexfont/IPAexfont00401.zip" > font.zip \
  && unzip font.zip\
  && touch /usr/local/lib/python3.6/dist-packages/matplotlib/mpl-data/fonts/ttf/ipaexg.ttf\
  && cp IPAexfont00401/ipaexg.ttf /usr/local/lib/python3.6/dist-packages/matplotlib/mpl-data/fonts/ttf/ipaexg.ttf \
  && echo "font.family : IPAexGothic" >>  /usr/local/lib/python3.6/dist-packages/matplotlib/mpl-data/matplotlibrc \
  && rm -r ./root/.cache

# サーバーを立てる場所に移動
WORKDIR /TableImageToCsv/TITC
# これでbashとか使わずにrunするだけでサーバーが立つ
CMD  python3 manage.py runserver 0:8000

