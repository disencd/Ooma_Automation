#!/usr/bin/env bash


chmod 777 *
python settings.py

python ./test_scripts/create_oss_hms_acc.py
