# docker build -t free-parking-network . && docker run -p 1337:1337 -t free-parking-network
FROM node:20-buster-slim

# Install Google Chrome
RUN apt-get update \
    && apt-get install -y wget gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxss1 libx11-xcb1 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD true
ENV BROWSER_ARGS --no-sandbox
ENV BROWSER /usr/bin/google-chrome-stable

COPY package.json /app/
COPY package-lock.json /app/
RUN npm ci

COPY . /app/

ARG FLAG=GPNCTF{fake_flag}
RUN echo "$FLAG" > /flag


ENTRYPOINT ["node", "server.js"]

EXPOSE 1337
