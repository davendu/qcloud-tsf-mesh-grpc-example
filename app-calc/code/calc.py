#!/usr/bin/env python3
import random
import json
import sys
import http.server

import grpc
import calc_pb2
import calc_pb2_grpc


hostPort = 8000
servicePort = 9000
serviceHost = "multiplier"

servicePath = "{}:{}".format(serviceHost, servicePort)
preserveHeaders = ['x-request-id',
                'x-trace-service',
                'x-ot-span-context',
                'x-client-trace-id',
                'x-envoy-force-trace',
                'x-b3-traceid',
                'x-b3-spanid',
                'x-b3-parentspanid',
                'x-b3-sampled',
                'x-b3-flags']


def rpcRun(metadata):
    with grpc.insecure_channel(
            target=servicePath,
            options=[('grpc.enable_retries', 0), 
                     ('grpc.keepalive_timeout_ms', 10000)]) as channel:
        stub = calc_pb2_grpc.CalculatorStub(channel)
        l = random.randint(1,100)
        r = random.randint(1,100)
        # Metadata is used to tracking the call chain
        # Timeout in seconds.
        # Please refer gRPC Python documents for more detail. https://grpc.io/grpc/python/grpc.html
        response = stub.Mul(
            calc_pb2.OpRequest(left=l, right=r), timeout=10, metadata=metadata)
    print("client received: " + str(response.result))
    return (l,r,response.result)

class handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/v1/multiply':
            print("Client: " + str(self.client_address))
            print("Source headers: " + str(self.headers.items()))
            print("Get trace headers")
            metadata = list()
            for i in preserveHeaders:
                h = self.headers.get(i)
                if h:
                    metadata.append((i, h))
            print("Forwarding following headers: " + str(metadata))

            print("Dialing GRPC")
            m = rpcRun(metadata)
            print("Call done.")

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            msg = {
                    "result": m[2], 
                    "l": m[0], 
                    "r": m[1], 
                    "req_source": "{}:{}".format(self.client_address[0], self.client_address[1])
                    }
            print(msg)
            self.wfile.write(json.dumps(msg).encode())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            msg = {
                "status":"UP"
            }
            self.wfile.write(json.dumps(msg).encode())
        else:
            self.send_error(404, "{\"message\":\"File not found.\"}")
            return


if __name__ == '__main__':
    # Start a simple server, and loop forever
    ServerClass  = http.server.HTTPServer
    print("host port is %s"%hostPort)
    server = ServerClass(('0.0.0.0', hostPort), handler)
    server.serve_forever()
