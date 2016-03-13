#!/bin/bash

set -e
set -o pipefail
set -x

BASE_DIR=/home/ec2-user/gascrape
BIN=${BASE_DIR}/download_profiles.py
DATA_DIR=${BASE_DIR}/data
INPUT_DIR=${DATA_DIR}/actors-100
OUTPUT_DIR=${DATA_DIR}/profiles/actors-100

# kajibu.test
CLIENT_ID=a229b66040dd4bb8010b
CLIENT_SECRET=b835ee03871cb8a2fbd8b63a7d63aecb084f9253

for i in {10..14}
do
  ${BIN}\
    --user_file=${INPUT_DIR}/actors-$i\
    --download_base_dir=${OUTPUT_DIR}\
    --client_id=${CLIENT_ID}\
    --client_secret=${CLIENT_SECRET}
done

