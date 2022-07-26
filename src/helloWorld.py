import urllib3
import idna
import requests
import psycopg2

from .python_packages import send_mail_v2

"""This is a very simple helloWorld python script"""
def helloWorld( msg ):
    """
    This is a simple function that prints a message
 
    :param msg: The string to print
    """
 
    print( msg )
 
helloWorld( 'Hello World!!!!' )