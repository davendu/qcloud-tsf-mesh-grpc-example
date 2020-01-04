#!/usr/bin/env python3
from concurrent import futures

import grpc

import calc_pb2
import calc_pb2_grpc


class Calculator(calc_pb2_grpc.CalculatorServicer):
    def Mul(self, request, context):
        for key, value in context.invocation_metadata():
            print('Received initial metadata: key=%s value=%s' % (key, value))

        return calc_pb2.OpReply(result=(request.left * request.right))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calc_pb2_grpc.add_CalculatorServicer_to_server(Calculator(), server)
    server.add_insecure_port('[::]:9000')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
