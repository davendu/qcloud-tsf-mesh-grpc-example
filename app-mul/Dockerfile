FROM python:3-slim

RUN  python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip && python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple grpcio grpcio-tools

ADD code /root/app/
WORKDIR /root/app/
# Build proto files
RUN python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/calc.proto

EXPOSE 9000

ENTRYPOINT "sh" "start.sh"
