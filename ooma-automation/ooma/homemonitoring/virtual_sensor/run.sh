#!/usr/bin/env bash


chmod 777 *
python settings.py

echo $PATH

python ./test_scripts/create_oss_hms_acc.py
