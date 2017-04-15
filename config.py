""" dbtable configuration file
"""
import os

database = "siki"                   # name of postgres database
document_root = "/var/www/html"     # document root of the web server
dbtable_root = os.path.dirname(os.path.abspath(__file__)[len(document_root):])
js = dbtable_root + "dbtable.js"   # absolute path to js module (doc root)
path = dbtable_root + "dbtable.py/"# absolute path to py module (doc root)
