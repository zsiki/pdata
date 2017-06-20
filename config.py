""" dbtable configuration file
"""

import os
import logging
database = 'webserver'
document_root = '/var/www/html'
dbtable_root = os.path.dirname(os.path.abspath(__file__)[len(document_root):]) + '/'
js = dbtable_root + 'dbtable.js'
path = dbtable_root + 'dbtable.py/'
log_level = logging.DEBUG
log_format = '%(asctime)-15s %(levelname)s %(message)s'
log = os.path.dirname(os.path.abspath(__file__)) + '/dbtable.log'
css = dbtable_root + 'dbtable.css'