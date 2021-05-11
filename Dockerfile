FROM python:3.8

WORKDIR /app

COPY main.py .
COPY .env .

EXPOSE 9090

# install dependencies
RUN pip3 install telebot
RUN pip3 install pyTelegramBotAPI
RUN pip3 install python-dotenv

# command to run on container start
CMD [ "python", "./main.py" ]