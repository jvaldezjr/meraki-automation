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
