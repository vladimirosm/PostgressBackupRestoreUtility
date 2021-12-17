# Python script backup or restore postgress database

config.json  - configuration file
pg_maintance.py - main file utility


## Configuration file 'config.json'

format: json

fields:

    "host_name"      - string. server host name.     example: "localhost",
    "database_name"  - string. postgress database name . example : "test",
    "user_name"      - string. example: "postgres", 
    "user_password"  - string. example: "123", 
    "port"           - string. example: "5432",
    "backup_dir"     - string. Folder to collect backups. example: "/var/db_backup"
    "backup_file_postfix" - string. Postfix for backup file.   Пример: "_%Y-%m-%d_%H:%M:%S" 

## Main file utility

used libraries : subprocess, shlex, datetime, os, time, json
working with: dropdb, createdb, pg_restore, pg_dump

After run :

    1 - Backup   (create dump)
    2 - Restore  (restore from dump)
    3 - Exit     


Backup process create file "<database_name>_<backup_file_postfix>" in configuration parameter "backup_dir"

Restore process show all files in "backup_dir" and wait for input number of file 


    Select file
    0 - test_2021-12-14_17:11:14.dmp
    1 - test_2021-12-14_17:10:56.dmp
    2 - test_2021-12-14_17:09:43.dmp
    3 - test_2021-12-14_17:08:32.dmp
    4 - test_2021-12-14_17:05:32.dmp
    5 - test_2021-12-14_16:54:45.dmp

