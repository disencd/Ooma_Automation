
# Home Monitoring Automation Project

Home Monitoring Automation Project includes both the client and Server testing framework using Python Scripting

## Features

- Supported platforms: x86_64, i386, OSX


## Installation
1) Install the packages from Requirements.txt File

2) Untar the OomaHomeMonitoringAutomation tarball

    tar zxvf OomaHomeMonitoringAutomation-1.0.tar.gz


## Example

See [test](test/client_hms_config.py) for pairing and triggering events

This includes

1) test hms_server_status
2) test hms_config_in_client
3) test trigger_pairing_mode - pair the door and water sensor
4) test door_sensor_status - trigger door open/close, tamper/armed, paging
5) test flood_sensor_status - trigger sensor dry/wet, tamper/armed, paging
