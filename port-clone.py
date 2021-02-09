# This script will prompt the user to select an organization, source switch,
# source port and destination switch and port to clone a port config, before
# confirming if the user would like to proceed with the change

# Configure your API key ENV variable using 'export MERAKI_DASHBOARD_API_KEY=YOUR_KEY'

# Usage: python port-clone.py

import meraki
import os
import re
import pprint

# Instantiate the Meraki Dashboard API using the Python SDK
dashboard = meraki.DashboardAPI(os.environ['MERAKI_DASHBOARD_API_KEY'])

# Get the list of organizations that the user has priveleges on
orgs = dashboard.organizations.getOrganizations()

# Print the list of organization names
for i, org in enumerate(orgs):
    print (i, ":", org['name'])

# Prompt the user for which organization they'd like to configure
selected_org = int(input("Which organization would you like to select? "))

# Get the list of devices in the selected organization
org_devices = dashboard.organizations.getOrganizationDevices(
    orgs[selected_org]['id'], total_pages='all'
)

# Filter the list of devices for only switches
def get_product(devices, type):
    return list(filter(lambda device: re.match(type, device['model']), devices))

org_switches = get_product(org_devices, "MS")

# Print the list of switches in the organization
def print_switches(switches):
    for i, switch in enumerate(switches):
        print (i, ":", switch['name'], "/", switch['serial'])

# Get a port config and remove portId key / value pair
def get_port_config(serial, port):
    config = dashboard.switch.getDeviceSwitchPort(
        serial, port
    )
    del config['portId']
    return config

print_switches(org_switches)

# Prompt the user for the source switch and source port to be cloned
source_switch = org_switches[int(input("Which source switch would you like to select? "))]
source_port = int(input("Which source port would you like to clone? "))

# Store port config to be cloned
port_config = get_port_config(source_switch['serial'], source_port)

print_switches(org_switches)

# Get the destination switch and port to be configured
destination_switch = org_switches[int(input("Which destination switch would you like to configure? "))]
destination_port = int(input("Which destination port would you like to configure? "))

# Confirm the config about to be cloned
print(f"The following source port config will be cloned from {source_switch['name']} to {destination_switch['name']} port {destination_port}: ")
pprint.pprint(port_config)

# Get user consent to proceed
while True:
  try:
    proceed = input("Carry on? (y/n): ")
    if proceed.lower() == 'n':
        print("Quitting program...")
        quit()
    elif proceed.lower() == 'y':
      break
    print("Invalid response entered, please respond with y or n")
  except Exception as e:
    print(e)

# Configure destination port
dashboard.switch.updateDeviceSwitchPort(
    switches[destination_switch]['serial'], destination_port, **port_config
)
