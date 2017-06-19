"""
    Python module to handle temporal point data
"""
import logging
import re
import datetime
import psycopg2
import json
import config     # some configuration settings (database, js)

def index(req, table="pdata", order="id"):
    """ creates main html page
        :param req: request data (not used)
        :param table: table name in database
        :param order: sort order of table data
        :returns: html string
    """
    res = """<!doctype html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title> Table list </title>
            <link rel="stylesheet" href="http://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
            <link href="{2}" rel="stylesheet"  type="text/css"/>
            <script type="text/javascript" src="http://code.jquery.com/jquery-3.2.1.min.js" >
            </script>
            <script type="text/javascript" src="http://code.jquery.com/ui/1.12.1/jquery-ui.min.js">
            </script>
            <script type="text/javascript">path="{0}";</script>
            <script type="text/javascript" src="{1}">
            </script>
        </head>
        <body>
            <div id="dia" title="Hello">
                <form>
                    <fieldset>
                    <label for="id">Point ID</label><br />
                    <input type="text" name="id" id="id" size="15"><br />
                    <label for="easting">Easting</label><br />
                    <input type="text" name="easting" id="easting" size="15"><br />
                    <label for="northing">Northing</label><br />
                    <input type="text" name="northing" id="northing" size="15"><br />
                    <label for="elev">Elevation</label><br />
                    <input type="text" name="elev" id="elev" size="15"><br />
                    <label for="d1">Date</label><br />
                    <input type="text" name="d1" id="d1" size="15"><br />
                    <label for="d2">Time</label><br />
                    <input type="text" name="d2" id="d2" size="15">
                    </fieldset>
                </form>
            </div>

            <p class="buttonclass"><input type="button" name="ref" value="Refresh" id="ref">&nbsp;
               <input type="button" name="upd" value="Update" id="upd">&nbsp;
               <input type="button" name="del" value="Delete" id="del">&nbsp;
               <input type="button" name="ins" value="Insert" id="ins">&nbsp;
	           <input type="button" name="sel" value="Select" id="sel">&nbsp;
               <input type="button" name="filt" value="Filter" id="filt">&nbsp;
            </p><div id="dbtable">
        """.format(config.path, config.js, config.css)
    return res + dbtable(req, table, order) + "</div></body></html>"

def dbtable(req, table, order="id", idFilt='', eastingFilt='', northingFilt='', elevFilt='', 
            d1Filt = '', d2Filt = ''):
    """ returns html table of point data from database

        :param req: request data (not used)
        :param table: table name in database
        :param order: sort order of table data
        :param idFilt: filter to query the point id's
        :param eastingFilt: filter for the easting coords
        :param northingFilt: filter for the northing coords
        :param elevFilt: filter for the elevations
        :param d1Filt: first part (year-month-day) of the date filter
        :param d2Filt: second part (hour-minute_second) of the date filter 
        :returns: html string
    """
    logging.basicConfig(format=config.log_format, filename=config.log)
    conn = psycopg2.connect(database=config.database)
    if not conn:
        msg = "Cannot connect to database :("
        logging.error(msg)
        return msg

    sql = "select * from {0} ".format(table)

    query = ""
    # Filtering the database.
    if idFilt != "" or eastingFilt != "" or northingFilt != "" or elevFilt != "" or d1Filt != "" or d2Filt != "":
        query += "where "

    # Point ID filter
    if idFilt != "":
        query += "id ~ '{0}' and ".format(idFilt)

    # Easting filter
    if eastingFilt != "":
        query += "easting {0} and ".format(eastingFilt)

    # Northing filter
    if northingFilt != "":
        query += "northing {0} and ".format(northingFilt)

    # Elevation filter
    if elevFilt != "":
        query += "elev {0} and ".format(elevFilt)

    # Year-Month-Day filter
    if d1Filt != "":
        d1FiltMod = re.subn(r'(\d{4}\-\d{2}\-\d{2})', r"'\1'", d1Filt)[0]
        query += "to_char(d, 'YYYY-MM-DD') {0} and ".format(d1FiltMod)

    # Hour-Minute-Second filter
    if d2Filt != "":
        d2FiltMod = re.subn(r'(\d{2}\:\d{2}\:\d{2})', r"'\1'", d2Filt)[0]
        query += "to_char(d, 'HH24:MI:SS') {0}".format(d2FiltMod)

    # Strip the ending 'and' of the SQL and close it
    query = query.strip(" and ")
    sql += query

    if order is not None and len(order.strip()):
        sql += " order by {0}".format(order)
    logging.debug(sql)
    cur = conn.cursor()
    cur.execute(sql)
    # hibakezeles!!!!

    res = """
             <table border="1">
             <tr><th>&nbsp;</th><th>ID</th><th>Easting</th><th>Northing</th><th>Elevation</th><th>Time</th></tr>
        """
    for row in cur:
        res += """<tr><td><input type="checkbox" name="{0}|{3}"></td>
               <td>{0}</td><td>{1}</td>
               <td>{2}</td>
               <td>{3}</td>
               <td>{4}</td></tr>""".format(row[0], row[1], row[2], row[3], row[4])
    res += "</table>"
    cur.close()
    return res

def dbdel(req, table, ids):
    """ Delete records from table, ids contains point id and date/time in the
        form point_id|datetime;point_id|datetime;...
        :param req: request object from apache
        :param table: table name
        :param ids: keys to records to delete
        :return: number of deleted rows
    """
    logging.basicConfig(format=config.log_format, filename=config.log)
    conn = psycopg2.connect(database=config.database)
    if not conn:
        msg = "Cannot connect to database :("
        logging.error(msg)
        return msg
    sql = "delete from {0} where (id, d) in (".format(table)
    keys = ids.strip(";").split(";")
    for key in keys:
        i, d = key.split("|")
        sql += "('{0}', '{1}'),".format(i, d)
    sql = sql.strip(',')
    sql += ")"
    logging.debug(sql)
    cur = conn.cursor()
    cur.execute(sql)
    msg = "{0} lines deleted".format(cur.rowcount)
    logging.info(msg)
    conn.commit()
    cur.close()
    return msg

def test(req, table, id, d):
    logging.basicConfig(format=config.log_format, filename=config.log)
    conn = psycopg2.connect(database=config.database)
    if not conn:
        msg = "Cannot connect to database :("
        logging.error(msg)
        return msg

    sql = "select id,easting,northing,elev,d from {0} where id='{1}' and d = '{2}'".format(table, id, d)
    logging.debug(sql)
    cur = conn.cursor()
    cur.execute(sql)
    if cur.rowcount == 1:
        result = json.dumps(['{}'.format(x) for x in cur.fetchone()])
    else:
        result = []

    # hibakezeles!!!
    cur.close()
    return result

def dbins(req, table, id, easting, northing, elev=None, d=None):
    """ Insert new record into table
        :param req: request object from apache
        :param table: table name
        :param id: point id
        :param easting: easting coordinate
        :param northing: northing coordinate
        :param elev: elevation
        :param d: data and time
        :return: number of deleted rows
    """
    logging.basicConfig(format=config.log_format, filename=config.log)
    conn = psycopg2.connect(database=config.database)
    if not conn:
        msg = "Cannot connect to database :("
        logging.error(msg)
        return msg
    if elev is None:
        elev = 'NULL'
    if d is None:
        d = datetime.datetime.now().isoformat(" ")
    sql = """insert into {0} (id, easting, northing, elev, d)
        values ('{1}', {2}, {3}, {4}, '{5}')
        """.format(table, id, easting, northing, elev, d)
    logging.debug(sql)
    cur = conn.cursor()
    cur.execute(sql)
    msg = "{0} lines inserted".format(cur.rowcount)
    logging.info(msg)
    conn.commit()
    cur.close()
    return msg


def dbupd(req, table, id, easting, northing, elev=None, d=None):
    """ Insert new record into table
        :param req: request object from apache
        :param table: table name
        :param id: point id
        :param easting: easting coordinate
        :param northing: northing coordinate
        :param elev: elevation
        :param d: data and time
        :return: number of deleted rows
    """
    logging.basicConfig(format=config.log_format, filename=config.log)
    conn = psycopg2.connect(database=config.database)
    if not conn:
        msg = "Cannot connect to database :("
        logging.error(msg)
        return msg
    if elev is None:
        elev = 'NULL'
    if d is None:
        d = datetime.datetime.now().isoformat(" ")
    sql = """UPDATE {0} 
            SET id='{1}', easting='{2}', northing='{3}', elev='{4}', d='{5}'
            WHERE id='{1}';
        """.format(table, id, easting, northing, elev, d)
    logging.debug(sql)
    cur = conn.cursor()
    cur.execute(sql)
    msg = "Line: '{0}' updated".format(id)
    logging.info(msg)
    conn.commit()
    cur.close()
    return msg