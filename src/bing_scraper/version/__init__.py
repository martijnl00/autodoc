import azure.functions as func
from ..scraper import VERSION


def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(f"Version:{VERSION}")
