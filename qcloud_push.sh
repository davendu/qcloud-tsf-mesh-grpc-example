#!/bin/bash

namespace="tsf_ACCOUNTID"
domain="ccr.ccs.tencentyun.com"
proto_dir="$(pwd)/protos"

pushd app-calc
cp -r $proto_dir ./code/protos
docker build -t $domain/$namespace/app-calc .
docker push 
popd

pushd app-mul
cp -r $proto_dir ./code/protos
docker build -t $domain/$namespace/app-mul .
docker push 
popd
