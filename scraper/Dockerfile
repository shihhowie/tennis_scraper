FROM amazon/aws-lambda-python:3.9

RUN yum install -y \
    unzip \
    libxcb \
    libxcb-devel \
    alsa-lib \
    atk \
    cups-libs \
    gtk3 \
    libXcomposite \
    libXcursor \
    libXdamage \
    libXi \
    libXtst \
    pango \
    xorg-x11-fonts-Type1 \
    xorg-x11-fonts-misc \
    fontconfig \
    freetype \
    libXrandr \
    libXrender \
    libXScrnSaver \
    libxshmfence \
    mesa-libgbm \
    libatomic \
    libnss3 \
    libgconf-2

COPY ./chrome-installer.sh ./chrome-installer.sh
RUN chmod +x ./chrome-installer.sh
RUN ./chrome-installer.sh

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY scraper.py ./
COPY sql_util.py ./
CMD ["scraper.lambda_handler"]