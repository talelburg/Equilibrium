FROM python:3.8
RUN pip install flask bson click furl construct protobuf pika
COPY equilibrium/equilibrium_pb2.py /equilibrium/
COPY equilibrium/sample/* /equilibrium/sample/
COPY equilibrium/queue/* /equilibrium/queue/
COPY equilibrium/utils/* /equilibrium/utils/
COPY equilibrium/server/* /equilibrium/server/
ARG host="0.0.0.0"
ENV HOST ${host}
ARG port="8000"
ENV PORT ${port}
ARG url="rabbitmq://rabbitmq:5672"
ENV URL ${url}
CMD python -m equilibrium.server run-server -h $HOST -p $PORT $URL