"""
    Python module to handle temporal point data
"""
import logging
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

            <!-- Dialog box for data filtering --!>
            <div id="filtDia" title="Data filtering">
                <form>
                    <fieldset>
                    <p>RegEx can be used for ID filtering.</p>
                    <label for="id">Point ID</label>&nbsp;
                    <input type="text" name="minId" id="filtId" size="15"><br />
                    <label for="minEasting">Min. Easting</label>&nbsp;
                    <input type="text" name="minEasting" id="filtMinEasting" size="15">&nbsp;
                    <label for="maxEasting">Max. Easting</label>&nbsp;
                    <input type="text" name="maxEasting" id="filtMaxEasting" size="15"><br />
                    <label for="minNorthing">Min. Northing</label>&nbsp;
                    <input type="text" name="minNorthing" id="filtMinNorthing" size="15">&nbsp;
                    <label for="maxNorthing">Max. Northing</label>&nbsp;
                    <input type="text" name="maxNorthing" id="filtMaxNorthing" size="15"><br />
                    <label for="minElev">Min. Elevation</label>&nbsp;
                    <input type="text" name="minElev" id="filtMinElev" size="15">&nbsp;
                    <label for="maxElev">Max. Elevation</label>&nbsp;
                    <input type="text" name="maxElev" id="filtMaxElev" size="15"><br />
                    <label for="d">Earliest Date</label>&nbsp;
                    <input type="text" name="minD" id="filtMinD" size="15">&nbsp;
                    <label for="d">Latest Date</label>&nbsp;
                    <input type="text" name="maxD" id="filtMaxD" size="15">&nbsp;                    </fieldset>
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

def dbtable(req, table, order="id"):
    """ returns html table of point data from database

        :param req: request data (not used)
        :param table: table name in database
        :param order: sort order of table data
        :returns: html string
    """
    logging.basicConfig(format=config.log_format, filename=config.log)
    conn = psycopg2.connect(database=config.database)
    if not conn:
        msg = "Cannot connect to database :("
        logging.error(msg)
        return msg

    sql = "select * from {0}".format(table)
    if order is not None and len(order.strip()):
        sql += " order by {0}".format(order)
    logging.debug(sql)
    cur = conn.cursor()
    cur.execute(sql)
    # hibakezeles!!!!

    res = """
             <table border="1">
             <tr><th>&nbsp;</th><th>ID</th><th>Easting</th><th>Northing</th><th>Time</th></tr>
        """
    for row in cur:
        res += """<tr><td><input type="checkbox" name="{0}|{3}"></td>
               <td>{0}</td><td>{1}</td>
               <td>{2}</td>
               <td>{3}</td></tr>""".format(row[0], row[1], row[2], row[4])
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
    
# Data filter function for the database backend.
def dbfilt(req, table, id="", minEasting=-1e10, maxEasting=1e10, 
           minNorthing=-1e10, maxNorthing=1e10, minElev=-1e10, maxElev=1e10, 
           minD='1900-01-01 00:00:00', maxD='2200-12-31 24:00:00'):
    """ Filter database table with the given paramters.
        :param req: request object from apache
        :param table: table name
        :param id: filtering condition for point ID
        :param maxEasting: maximum threshold for easting coordinates
        :param minEasting: minimum threshold for easting coordinates
        :param maxNorthing: maximum threshold for northing coordinates
        :param minNorthing: minimum threshold for northing coordinates
        :param minElev: minimum threshold for elevations
        :param maxElev: maximum threshold for elevations 
        :param minD: starting date
        :param maxD: ending date
        :return res: HTML code containing the rows that satisfy the conditions
        :return rcount: number of rows satisfying the condition
    """

    # Check if arguments are empty and change them to the default settings.
    if minEasting == "": minEasting = -1e10
    if maxEasting == "": maxEasting = 1e10
    if minNorthing == "": minNorthing = -1e10
    if maxNorthing == "": maxNorthing = 1e10
    if minElev == "": minElev = -1e10
    if maxElev == "": maxElev = 1e10
    if minD == "": minD = '1900-01-01 00:00:00'
    if maxD == "": maxD = '2200-12-31 24:00:00' 

    logging.basicConfig(format=config.log_format, filename=config.log)
    conn = psycopg2.connect(database=config.database)
    
    # On connection error.
    if not conn:
        msg = "Cannot connect to database."
        logging.error(msg)
        return msg

    # Create cursor.
    cur = conn.cursor()

    # Create SQL with the specified filtering conditions.
    sql = "select * from {0} where id ~ '{1}' and "\
          "easting between {2} and {3} and northing between {4} and {5} and "\
          "elev between {6} and {7} and d between '{8}' and '{9}';".format(table, id, 
            minEasting, maxEasting, minNorthing, maxNorthing, minElev, maxElev, minD, maxD)

    # Execute SQL query.
    cur.execute(sql)

    # Create HTML for each row.
    res = """
         <table border="1">
         <tr><th>&nbsp;</th><th>ID</th><th>Easting</th><th>Northing</th><th>Time</th></tr>
    """
    for row in cur:
        res += """<tr><td><input type="checkbox" name="{0}|{3}"></td>
               <td>{0}</td><td>{1}</td>
               <td>{2}</td>
               <td>{3}</td></tr>""".format(row[0], row[1], row[2], row[4])
    res += "</table>"

    # Number of rows in the query return.
    rcount = cur.rowcount

    # Close cursor and connection.
    cur.close(), conn.close()

    # Create JSON from the results
    filtData = json.dumps({"filtHTML": res, 
                           "rcount": "{0} row(s) matched the filter.".format(rcount)})

    return filtData