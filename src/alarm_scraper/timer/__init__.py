import datetime
import logging
from ..scraper import scrape_and_insert
import os

import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info("The timer is past due!")

    if os.environ.get("timerenabled", "1") == "1":
        logging.info("About to generate at %s", utc_timestamp)
        scrape_and_insert()
    else:
        logging.info("generate not enabled")
