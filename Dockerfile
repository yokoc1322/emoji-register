FROM python:3.7-slim AS emoji-register-prod

WORKDIR /workspace

ADD emoji-register emoji-register

RUN set -x \
  && apt-get update \
  && apt-get upgrade -y \
  && apt-get install -y \
  cmake \
  fontconfig \
  libgl1-mesa-dev \
  libglib2.0-0 \
  libglu1-mesa \
  libglu1-mesa-dev \
  libsm6 \
  libxext6 \
  libxi-dev \
  libxmu-dev \
  libxrender1 \
  wget \
  unzip \
  && cd emoji-register \
  && pip install -r requirements-not-contain-emojilib.txt \
  && pip install -r requirements-emojilib.txt \
  && sh scripts/init_font.sh \
  && rm -rf /tmp/* /var/tmp/* /root/.cache/* \
  && rm -rf /var/lib/apt/lists/*

WORKDIR emoji-register
EXPOSE 80

CMD ["python", "src/server.py"]

FROM emoji-register-prod AS emoji-register-dev

RUN set -x \
  && pip install -r requirements-dev.txt

CMD ["/bin/bash"]

