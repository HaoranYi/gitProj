CREATE TABLE `tbTeacher` (
	`id`	  INTEGER PRIMARY KEY     NOT NULL,
	`name`    VARCHAR[50]             NOT NULL,
	`rate`    DOUBLE                  NOT NULL,
	`address` VARCHAR[50],	
	`phone`   CHAR[20]                  
);

CREATE TABLE `tbStudent` (
	`id`	  INTEGER PRIMARY KEY     NOT NULL,
	`name`    VARCHAR[50]             NOT NULL,
	`age`     INT                     NOT NULL,
	`grade`   INT                     NOT NULL,
	`address` VARCHAR[50],	
	`phone`   CHAR[20]                  
);

DROP TABLE `tbClass`;

CREATE TABLE `tbClass` (
	`id`	  INTEGER PRIMARY KEY     NOT NULL,
	`student_id`    INTEGER,
	`teacher_id`    INTEGER,
	`starttime`     DATETIME,
	`endtime`       DATETIME,	
	FOREIGN KEY (`student_id`) REFERENCES `tbStudent`(id) ON DELETE SET NULL ON UPDATE CASCADE,
	FOREIGN KEY (`teacher_id`) REFERENCES` tbTeacher`(id) ON DELETE SET NULL ON UPDATE CASCADE
);

PRAGMA foreign_keys 
PRAGMA foreign_keys = ON; -- OFF

-- actions on foreign key constraint
-- SET NULL, SET DEFAULT, RESTRICT, CASCADE, and NO ACTION.

-- Insert some data ...

INSERT INTO tbTeacher(name, rate)
VALUES
('Mike', 100.0),
('Tom', 100.0); 

INSERT INTO tbStudent(name, age, grade)
VALUES
('Caroline', 7, 2),
('Charles', 4, 1); 


INSERT INTO tbClass(student_id, teacher_id, starttime, endtime)
VALUES
(1, 1, datetime('now', 'localtime'),  datetime('now', 'localtime', '+60 minutes')),
(2, 2, datetime('now', 'localtime'),  datetime('now', 'localtime', '+60 minutes'));

-- list all the classes
SELECT T.name as TName, T.rate as Rate, S.name as SName, S.age as Age, S.grade as Grade,
    C.starttime as StartTime, C.endtime as EndTime
FROM tbClass C
JOIN tbTeacher T ON C.teacher_id = T.id
JOIN tbStudent S ON C.student_id = S.id

-- example to add primary key
CREATE TABLE test_table(
    id INTEGER,
    salt TEXT NOT NULL UNIQUE,
    step INT,
    insert_date TIMESTAMP
);

ALTER TABLE test_table RENAME TO test_table_temp;

CREATE TABLE test_table(
    id INTEGER PRIMARY KEY,
    salt TEXT,
    step INT,
    insert_date TIMESTAMP
);

INSERT INTO test_table SELECT * FROM test_table_temp;

DROP TABLE test_table_temp;
