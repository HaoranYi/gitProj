# Use sqlite cli to interact with sql database files
-------------------------------------------------------------------------------

see https://sqlite.org/cli.html for documentation.

```
$> sqllite3 DBFILE
    .open DBFILE
    .tables    
    .schema tbName
    .read sql_file
    .system cmd arg1 arg2  -- run shell command
    .header on
    .dump                  -- export db as pure sql
    .save
    .exit DBFILE
```

datetime functions:
```
    datetime('now', 'localtime') 
    datetime('now', 'localtime', '+60 minutes')  -- now+1hour
```
sqlite datetime is stored as int64. sqlite can parse string as datetime.


multiple databases

```
    attach database DBFILE as DBNAME
    detach database DBNAME
```
In sql, prefix table with DBNAME: DBNAME.tbXXX


import/export data
```
    .mode csv
    .import C:/work/data.csv tab1

    .header on
    .mode csv
    .once c:/work/dataout.csv
    select * from tab1
    .system c:/work/dataout.csv
```

archive
```
    sqlite2 ex .dump | gzip -c >ex1.dump.gz
    zcat ex1.dump.gz | sqlite ex2

    -- export db as pure sql text that can be imported in other database
    createdb ex2
    sqlite2 ex1 .dump | psql ex2  
```

shell usage
```
    sqlite3 ex1 'select * from tab1' | 
      awk '{printf "<tr><td>%s</td>%s</tr>\n", $1, $2}'
```

sqlite3_analyzer.exe: dump the space usage of the database. It generate sql
for the matrix table too.

# SQL syntax
-------------------------------------------------------------------------------

limit and order by
```
    SELECT * FROM tbl LIMIT 10
    SELECT * FROM tbl LIMIT 10 OFFSET 10

    SELECT * FROM tbl ORDER BY col1 ASC LIMIT 10
    SELECT * FROM tbl ORDER BY col1 DESC LIMIT 10
```

CTE with statement
```
    WITH tb1(name) as (
        select ...
        ), 
        tb2(time) as (
        select ...
        )
    select tb1.*, tb2.* from tb1 
    joing tb2 on ...
    where ...
```

-- generate a table of [1,1000000]
```
    WITH RECURSIVE
      cnt(x) AS (
         SELECT 1
         UNION ALL
         SELECT x+1 FROM cnt
          LIMIT 1000000
      )
    SELECT x FROM cnt;
```

-- tree org
```
    CREATE TABLE org(
      name TEXT PRIMARY KEY,
      boss TEXT REFERENCES org,
      height INT,
      -- other content omitted
    );
```

-- compute average height of people work for 'alice'
```
    WITH RECURSIVE
      works_for_alice(n) AS (
        VALUES('Alice')
        UNION
        SELECT name FROM org, works_for_alice
         WHERE org.boss=works_for_alice.n
      )
    SELECT avg(height) FROM org
     WHERE org.name IN works_for_alice;
```


-- use orderby level asc to do breadth-frist search
```
    WITH RECURSIVE
      under_alice(name,level) AS (
        VALUES('Alice',0)
        UNION ALL
        SELECT org.name, under_alice.level+1
          FROM org JOIN under_alice ON org.boss=under_alice.name
         ORDER BY 2
      )
    SELECT substr('..........',1,level*3) || name FROM under_alice;
```


-- use orderby level desc to do depth-first search
```
    WITH RECURSIVE
      under_alice(name,level) AS (
        VALUES('Alice',0)
        UNION ALL
        SELECT org.name, under_alice.level+1
          FROM org JOIN under_alice ON org.boss=under_alice.name
         ORDER BY 2 DESC
      )
    SELECT substr('..........',1,level*3) || name FROM under_alice;
```

-- family tree
```
    CREATE TABLE family(
      name TEXT PRIMARY KEY,
      mom TEXT REFERENCES family,
      dad TEXT REFERENCES family,
      born DATETIME,
      died DATETIME, -- NULL if still alive
      -- other content
    );
```


-- find ancester of alice with two recursive CTE
```
    WITH RECURSIVE
      parent_of(name, parent) AS
        (SELECT name, mom FROM family UNION SELECT name, dad FROM family),
      ancestor_of_alice(name) AS
        (SELECT parent FROM parent_of WHERE name='Alice'
         UNION ALL
         SELECT parent FROM parent_of JOIN ancestor_of_alice USING(name))
    SELECT family.name FROM ancestor_of_alice, family
     WHERE ancestor_of_alice.name=family.name
       AND died IS NULL
     ORDER BY born;
```

