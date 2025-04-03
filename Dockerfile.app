FROM python:3.9.18
WORKDIR /app
COPY . .

ENV PIPENV_VENV_IN_PROJECT=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get -y update && \
	apt-get -y install git curl zsh && \
	wget -c https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
	dpkg -i google-chrome-stable_current_amd64.deb || apt-get -y install -f && \
	dpkg -i google-chrome-stable_current_amd64.deb && echo "chrome installation complete" && \
	wget https://storage.googleapis.com/chrome-for-testing-public/135.0.7049.42/linux64/chromedriver-linux64.zip && \
	unzip chromedriver-linux64.zip && \
	chsh -s /bin/zsh && \
	curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -o install.sh && \
	chmod +x install.sh && \
	yes | sh install.sh && \
	rm install.sh && \
	cp .env.example .env

RUN apt-get -y install nodejs && \
	apt-get -y install npm && \
	npm install -g n && \
	n 18.19 && \
	hash -r && \
	npm install && \
	npx husky init

RUN pip install pipenv && \
	pipenv install --ignore-pipfile
