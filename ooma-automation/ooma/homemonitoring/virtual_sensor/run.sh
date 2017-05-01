#!/usr/bin/env bash


chmod 777 *
sudo python settings.py

sudo python ./test_scripts/create_oss_hms_acc.py
