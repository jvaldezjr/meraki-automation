# meraki-automation
Meraki Dashboard Automation Scripts
## port-clone.py

This script will prompt the user to select an organization, source switch, source port and destination switch and port to clone a port config, before confirming if the user would like to proceed with the change.

Usage: python port-clone.py

## update-port.py

This script will prompt the user to select an organization, switch & port to be configured. The script will read in port roles from a vlans.yml file and prompt the user to select which port role should be assigned before confirming the change and updating the port config.

Usage: python update-port.py

## vlans.yml

This example YAML file contains a dictionary of port configurations with the first level key being the port role. You can update this to have any arbitrary value for the port roles / configurations.
