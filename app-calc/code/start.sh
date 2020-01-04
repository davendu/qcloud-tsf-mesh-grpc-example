#! /bin/bash
# Copy service register files
mkdir -p /opt/tsf/app_config/apis 
cp /root/app/spec.yaml /opt/tsf/app_config/
cp -r /root/app/apis /opt/tsf/app_config/
cd /root/app/

# Run client
python -u ./calc.py
