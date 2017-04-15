"""
    Python module to handle temporal point data
"""
import psycopg2
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
            <link href="/dbtable/dbtable.css" rel="stylesheet"  type="text/css"/>
            <script type="text/javascript" src="http://code.jquery.com/jquery-3.2.1.min.js" >
            </script>
            <script type="text/javascript" src="http://code.jquery.com/ui/1.12.1/jquery-ui.min.js">
            </script>
            <script type="text/javascript">path="%s";</script>
            <script type="text/javascript" src="%s">
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
                    <input type="text" name="d1" id="d1" size="15">
                    </fieldset>
                </form>
            </div>
            <p><input type="button" name="ref" value="Refresh" id="ref">&nbsp;
               <input type="button" name="upd" value="Update" id="upd">&nbsp;
               <input type="button" name="del" value="Delete" id="del">&nbsp;
               <input type="button" name="ins" value="Insert" id="ins">&nbsp;
            </p><div id="dbtable">
        """ % (config.path, config.js)
    return res + dbtable(req, table, order) + "</div></body></html>"

def dbtable(req, table, order="id"):
    """ returns html table of point data from database

        :param req: request data (not used)
        :param table: table name in database
        :param order: sort order of table data
        :returns: html string
    """
    conn = psycopg2.connect(database=config.database)
    if not conn:
        return "Cannot connect to database :("

    sql = "select * from %s" % table
    if order is not None and len(order.strip()):
        sql += " order by %s" % order

    cur = conn.cursor()
    cur.execute(sql)
    # hibakezeles!!!!

    res = """
             <table border="1">
             <tr><th>&nbsp;</th><th>ID</th><th>Easting</th><th>Northing</th><th>Time</th></tr>
        """
    for row in cur:
        res += """<tr><td><input type="checkbox" name="%s|%s"></td>
               <td>%s</td><td>%.3f</td>
               <td>%.3f</td>
               <td>%s</td></tr> """ % \
               (row[0], row[4], row[0], row[1], row[2], row[4])
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
    conn = psycopg2.connect(database=config.database)
    if not conn:
        return "Cannot connect to database :("
    sql = "delete from %s where (id, d) in (" % (table)
    keys = ids.strip(";").split(";")
    for key in keys:
        i, d = key.split("|")
        sql += "('%s', '%s')" % (i, d)
    sql += ")"
    cur = conn.cursor()
    cur.execute(sql)
    n = cur.rowcount
    conn.commit()
    cur.close()
    return "%d lines deleted" % n
