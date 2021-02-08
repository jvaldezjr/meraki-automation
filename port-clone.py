import meraki
import os

dashboard = meraki.DashboardAPI(os.environ['MERAKI_DASHBOARD_API_KEY'])

orgs = dashboard.organizations.getOrganizations()

for i, org in enumerate(orgs):
    print (i, ":", org['name'])

selected_org = input("Which organization would you like to select? ")

print(orgs[int(selected_org)]['id'])
