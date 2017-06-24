# pdata
point data handler application

The aim of this project to create a simple application to handle point data 
(id, coordiates, date and time) in a relational database from a browser.

## Functions

+ Refresh
+ Update
+ Delete
+ Insert
+ Select
+ Filter

### Refresh

Synchronize content with the database.

### Update

Update a single selected record.

### Delete

Delete all marked rows from database and refresh.

### Insert

Insert a new record into the database and refresh.

### Select

Mark rows by complex condition, useful to use together with delete.

### Filter

Show only rows which pass the complex filter.

## Filtering options

+ The point id's are stored as strings in the database, so any valid RegEx matching criterion can be used for filtering. E. g. `^1.*$` or `^1.*` will only show rows where the id's begin with one (1, 11, 12, 132, 123A, ...).

+ When filtering the coordinates (easting, northing and elevation), the valid expressions are <, >, =, <=, >=, <>, !=, AND, OR, BETWEEN x AND y. The coordinate values can be given with or without the decimal point, depending on the value. E. g. `<= 125. AND > 99.523` is a valid expression that gives back only the rows where the corresponding coordinate is less than or equal to 125 and greater than 99.523.

+ Filtering the date and the time values can be done in the same way as filtering the coordinates. The accepted operators are the same, but the format of the date or time given has to match up with the format used in the database, i. e. dates are accepted in the YYYY-MM-DD and time is accepted in the HH:MM:SS format. Neither the dates, nor the time has to be enclosed in ' '. A valid expression for the date would be `BETWEEN 2017-02-02 AND 2017-01-01`, and one for the time would be `<= 12:00:05`. 
