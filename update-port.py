# This script will prompt the user to select an organization, switch & port
# to be configured. The script will read in port roles from a vlans.yml file
# and prompt the user to select which port role should be assigned before
# confirming the change and updating the port config

# Configure your API key ENV variable using 'export MERAKI_DASHBOARD_API_KEY=YOUR_KEY'

# Usage: python update-port.py

import meraki
import os
import re
import pprint
from ruamel.yaml import YAML

# Read in vlans.yml file
yaml=YAML(typ='safe')
with open("vlans.yml") as file:
    port_roles = yaml.load(file)

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

# Filter a list of devices for only a specific type
def get_product(devices, type):
    return list(filter(lambda device: re.match(type, device['model']), devices))

# Filter org_devices for just switches
org_switches = get_product(org_devices, "MS")

# Print the list of switches in the organization
def print_switches(switches):
    for i, switch in enumerate(switches):
        print (i, ":", switch['name'], "/", switch['serial'])

# Prompt the user for the switch and port to be modified as well as the desired role
print_switches(org_switches)
source_switch = org_switches[int(input("Which switch would you like to modify? "))]
source_port = int(input("Which port would you like to update? "))
for i, role in enumerate(port_roles):
    print (i, ":", role)
role_input = int(input("Which port role should be assigned to the port? "))

# Prepare the port config based on the input role and the yaml configuration
port_config = port_roles[list(port_roles.keys())[role_input]]
