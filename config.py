""" dbtable configuration file
"""
import os
import logging

database = "webserver"                   # name of postgres database
document_root = "/var/www/html"     # document root of the web server
dbtable_root = os.path.dirname(os.path.abspath(__file__)[len(document_root):]) + "/"
css = dbtable_root + "dbtable.css"	# absolute path to css module (doc root)
js = dbtable_root + "dbtable.js"  	 # absolute path to js module (doc root)
path = dbtable_root + "dbtable.py/"	# absolute path to py module (doc root)
log_level = logging.DEBUG
log_format = "%(asctime)-15s %(levelname)s %(message)s"
# file for log messages (writeable by apache user!!!!)
log = os.path.dirname(os.path.abspath(__file__)) + "/dbtable.log"
