import os

import logging

VERSION = "0.0.1"

def filter_data(json):
    """
    Picks out the values in json corresponding to the district.
    Structure of json given by:
    https://docs.microsoft.com/en-us/bingmaps/rest-services/locations/find-a-location-by-point

    :param json: json-formatted response from scraping
    """
    data = json['resourceSets']
    data = data[0]['resources']
    data = data[0]['address']
    adminDistrict = None
    adminDistrict2 = None
    for entry in data:
        if entry == 'adminDistrict':
            adminDistrict = data[entry]
        if entry == 'adminDistrict2':   
            adminDistrict2 = data[entry]
    if adminDistrict2 != None:
        return adminDistrict2   
    else:
        return adminDistrict

def get_district(monitor_id, lat, lon):
    """
    Scrape bing maps for information about the given <lat> and <lon>.
    Filters the response to extract the district of the site
    :param monitor_id:  The id of the current site
    :param lat:         Latitude of the site corresponding to monitor_id
    :param lon:         Longitude of the site corresponding to monitor_id
    """
    bing_maps_key =  os.environ.get('bing_maps_key')
    search_url = f'http://dev.virtualearth.net/REST/v1/Locations/{lat},{lon}?o=JSON&key={bing_maps_key}'
    headers = {"Ocp-Apim-Subscription-Key": bing_maps_key}
    # response = requests.get(search_url, headers=headers).json()
  
    # filtered_data = filter_data(response)
    district_data = 1

    return district_data

def scrape_and_insert():
    """
    Wrapper func for web scraping, filtering and insert in DB.
    """
    sql = f"""\
        SELECT monitor_id, site_name, TRUNC(lat,4), TRUNC(lon,4) FROM combined.installation
        WHERE lat NOTNULL AND lon NOTNULL;"""

    installations = []

    district_all_sites = []
    for installation in installations:
        logging.info(f"GET DISTRICT FOR {installation[1]}")

        try:
            district_site = get_district(installation[0],installation[2],installation[3])
            district_all_sites.append(district_site)
            logging.info(f"[SUCCESS] GET DISTRICT FOR {installation[1]}")

        except:
            logging.info(f"[FAIL] GET DISTRICT FOR {installation[1]}")

    try:
        # insert(district_all_sites, "combined.districts", "(%s,%s)", "(monitor_id) DO UPDATE SET district = excluded.district;")
        logging.info("[SUCCESS] insert districts")

    except:
        logging.info("[FAIL] insert districts")

            