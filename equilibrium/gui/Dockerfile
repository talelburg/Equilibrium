FROM nikolaik/python-nodejs:latest

RUN pip install click flask
COPY ./equilibrium/gui/ /equilibrium/gui/
COPY ./equilibrium/utils/ /equilibrium/utils/

COPY ./equilibrium-gui/ /equilibrium-gui/
WORKDIR /equilibrium-gui
RUN npm install
RUN npm run build
RUN mv /equilibrium-gui/build /equilibrium/gui

WORKDIR /
ARG host
ENV HOST $host
ARG port
ENV PORT $port
ARG api_host
ENV API_HOST $api_host
ARG api_port
ENV API_PORT $api_port

CMD python -m equilibrium.gui -t run-server -h $HOST -p $PORT -H $API_HOST -P $API_PORT > /logs/$(date +%Y-%m-%d_%H-%M-%S).log
