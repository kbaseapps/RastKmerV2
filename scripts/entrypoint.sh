#!/bin/bash

. /kb/deployment/user-env.sh

python ./scripts/prepare_deploy_cfg.py ./deploy.cfg ./work/config.properties

if [ -f ./work/token ] ; then
  export KB_AUTH_TOKEN=$(<./work/token)
fi

if [ $# -eq 0 ] ; then
  sh ./scripts/start_server.sh
elif [ "${1}" = "test" ] ; then
  echo "Run Tests"
  make test
elif [ "${1}" = "async" ] ; then
  sh ./scripts/run_async.sh
elif [ "${1}" = "init" ] ; then
  echo "Initialize module"
  cd /data
  mkdir -p kmer
  wget ftp://ftp.theseed.org/KmerClassification/Data.may1.tgz
  tar -zxvf ./Data.may1.tgz --exclude="Data.may1/kmer.table.mem_map" --exclude="Data.may1/final.kmers"
  mv ./Data.may1 V2Data
  tar -zxvf ./Data.may1.tgz Data.may1/kmer.table.mem_map -O > ./V2Data/kmer.table.mem_map
  mv ./V2Data ./kmer/
  if [ -f /data/kmer/V2Data/kmer.table.mem_map ] ; then
    if [ -f /data/kmer/V2Data/function.index ] ; then
      touch __READY__
      ls -l /data/kmer/V2Data
    else
      echo "Init failed (function.index not found)"
      ls -l .
      ls -l ./kmer
      ls -l ./kmer/V2Data
    fi
  else
    echo "Init failed  (kmer.table not found)"
      ls -l .
      ls -l ./kmer
      ls -l ./kmer/V2Data
  fi
elif [ "${1}" = "bash" ] ; then
  bash
elif [ "${1}" = "report" ] ; then
  export KB_SDK_COMPILE_REPORT_FILE=./work/compile_report.json
  make compile
else
  echo Unknown
fi
