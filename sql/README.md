Use sqlite cli to interact with sql database files

see https://sqlite.org/cli.html for documentation.

`
$> sqllite3 DBFILE
    .tables    
    .schema tbName
    .read sql_file
    .header on
    .exit
`

datetime functions:
    datetime('now', 'localtime') 
    datetime('now', 'localtime', '+60 minutes')  -- now+1hour
