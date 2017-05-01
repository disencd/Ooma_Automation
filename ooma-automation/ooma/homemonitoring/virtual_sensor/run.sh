#!/usr/bin/env bash

#cd Ooma_Automation/ooma-automation/ooma/homemonitoring/virtual_sensor/
cd ./ooma/homemonitoring/virtual_sensor/

chmod 777 *
sudo python settings.py

sudo python ./test_scripts/create_oss_hms_acc.py
