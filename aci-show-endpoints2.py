#!/usr/bin/env python
"""
Simple application that logs on to the APIC and displays all
of the Endpoints.
"""
import acitoolkit.acitoolkit as aci
from tabulate import tabulate


def main():
    """
    Main Show Endpoints Routine
    :return: None
    """
    # Take login credentials from the command line if provided
    # Otherwise, take them from your environment variables file ~/.profile
    description = ('Simple application that logs on to the APIC'
                   ' and displays all of the Endpoints.')
    creds = aci.Credentials('apic', description)
    args = creds.get()

    # Login to APIC
    session = aci.Session(args.url, args.login, args.password)
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to APIC')
        return

    # Download all of the interfaces
    # and store the data as tuples in a list
    data = []
    endpoints = aci.Endpoint.get(session)
    for ep in endpoints:
        epg = ep.get_parent()
        app_profile = epg.get_parent()
        tenant = app_profile.get_parent()
        data.append((ep.if_name, tenant.name))

    # Display the data downloaded
    print(tabulate(data, headers=["INTERFACE", "TENANT"]))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
