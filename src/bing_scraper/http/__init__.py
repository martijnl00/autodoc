import logging

from ..scraper import scrape_and_insert
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    scrape_and_insert()

    return func.HttpResponse(f"Hello, This HTTP triggered function executed successfully.")
