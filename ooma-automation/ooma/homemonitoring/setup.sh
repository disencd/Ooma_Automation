#!/usr/bin/env bash


chmod 777 *
python settings.py

env

PYTHONPATH="${PYTHONPATH}/Users/Shared/Jenkins/Home/workspace/HomeSecurity/ooma-automation/ooma/homemonitoring/"
export PYTHONPATH
env

#ln -s "/Users/Shared/Jenkins/Home/workspace/HomeSecurity/ooma-automation/ooma/homemonitoring/" /usr/lib/python2.7/
