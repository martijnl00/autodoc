import logging

from datetime import datetime

from dcp_python.error import NoDataError
from dcp_python.data_flow import insert, get_headers, get_data_by_api, get_data_from_db

VERSION = "0.1.0"

def filter_alert(rawData, filter):
    """
    Picks out the values in data corresponding to the keys given in filter.

    :param rawData: Dictionary, preferably injective meaning no list values
    :param filter:  List of keys. Keys must exactly match keys in rawData
    """

    filtered_data = []

    for entry in rawData:
        filtered_data.append({filter_key: entry[filter_key] for filter_key in filter})

    return filtered_data

def filter_alarm(json):
    """
    Filter out the datapoints for the alarms from victron api

    :param json:    The data in json format
    """

    filter = ["idAlarm", "idSite", "description", "started", "cleared", "isActive"]

    alarm = json["records"]["data"]["alarms"]
    if alarm == []:
        raise NoDataError

    filtered_data = []

    for entry in alarm:
        filtered_data.append({filter_key: entry[filter_key] for filter_key in filter})
    
    for entry in filtered_data:
        if entry["started"] == 0:
            entry["started"] = None
        else:
            entry["started"] =  datetime.fromtimestamp(entry["started"])

        entry["cleared"] = datetime.fromtimestamp(entry["cleared"])

    return filtered_data

def scrape_and_insert():
    """
    Wrapper function performing several scrapes and inserts in try catch blocks.
    """
  
    headers_sco = get_headers("sco")
    headers_vrm = get_headers("victron")[0]
        
    try:
        url = f"https://api.steama.co/alerts/?state=OPN"
        raw_alerts = get_data_by_api(url, headers_sco)

        logging.info("[SUCCESS]\t get alerts")

    except NoDataError as e:
        logging.exception("[FAIL]\t get alerts")
    else:
        try:
            filter = ["id", "site", "meter", "alert_type", "state", "created"]
            alerts = filter_alert(raw_alerts["results"], filter)   

            insert(alerts, "sco.alert", "(%s,%s,%s,%s,%s,%s)", " (alert_id) DO UPDATE SET state = excluded.state, resolved = excluded.resolved ")   
            logging.info("[SUCCESS]\t insert alerts")

        except Exception:
            logging.exception("[FAIL]\t insert alerts")
        
    victron_sites = get_data_from_db("SELECT * FROM victron.installation;")

    for site in victron_sites:
        site_id = site[0]
        name = site[1]
        
        try:
            url = f"https://vrmapi.victronenergy.com/v2/installations/{site_id}/widgets/Alarm"
            raw_alarm = get_data_by_api(url, headers_vrm)

            logging.info(name + ":\t[SUCCESS] get alarm")

        except IOError as e:
            logging.exception(name + ":\t[FAIL] get alarm")
        except NoDataError as e:
            logging.info(name + ":\t NO ALARM")

        else:
            try:
                alarm = filter_alarm(raw_alarm)
                
                insert(alarm, "victron.alarm", "(%s,%s,%s,%s,%s,%s)", "(alarm_id) DO UPDATE SET cleared = excluded.cleared, is_active = excluded.is_active ")
                
                logging.info(name + ":\t[SUCCESS] insert alarm")

            except NoDataError:
                logging.error(name + ":\t[FAIL] No alarm")
        