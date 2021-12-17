#!/usr/bin/python

#   Postgress maintains utility file 
#   for backup/restore database
#


from subprocess import PIPE,Popen
import shlex
from datetime import datetime
import os
import time
import json


class DeviceConfiguration:

    configParams = {}
    configFileName = "config.json"

    def set(self, str, value):
           self.configParams.update({str : value})     

    def param(self, str):
        return self.configParams[str] if str in self.configParams else None

    def __load_config(self):
        with open(self.configFileName, 'r') as filehandle:
            return json.load(filehandle)

    def read_config(self):
        self.configParams = self.__load_config()

    def save_config(self):
        with open(self.configFileName, 'w') as filehandle:
            json.dump(self.configParams, filehandle)

    def __init__(self, filename, args=None, **kwargs):
        self.configFileName = filename





__configFileName = "config.json"
config = DeviceConfiguration(__configFileName);

def __dump_table():
    global config
    now = datetime.now()

    userPassword = config.param("user_password") 
    usePasswordPromt = ""
    env = {}
    if userPassword is None :
        usePasswordPromt = "-w"
    else:
        env={ 'PGPASSWORD': userPassword }

    time =""    
    if config.param("backup_file_postfix") is not None:
        time = now.strftime(config.param("backup_file_postfix"))

    backupFile = '{0}/{1}{2}.dmp'.format(config.param("backup_dir"),  config.param("database_name"), time)
    # --clean --create 
    command = 'pg_dump -h {0} -d {1} -U {2} -p {3} {4} --blobs --format=c --file={5}'\
    .format( 
        config.param("host_name"),
        config.param("database_name"),
        config.param("user_name"), 
        config.param("port"), 
        usePasswordPromt,
        backupFile
        )

    dump_success = True
    print ('Backing up "%s" database to file "%s"' % (config.param("database_name"), backupFile))
    try:
        p = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE,env=env)
        p.wait()
        if (p.returncode != 0 ):
            print(p.stderr.read())
            dump_success = False
            if os.path.exists(backupFile):
                os.remove(backupFile)

        output = p.communicate()[0]
    except Exception as e:
        dump_success = False
        print('Exception happened during dump %s' %(e))

    return dump_success

def file_chooser() :
    global config
    os.system('clear')
   
    c_dir = config.param("backup_dir")

    fileList = []
    for (dirpath, dirnames, filenames) in os.walk(c_dir):
        fileList.extend(filenames)

    list_of_files = sorted( fileList,
                        key = lambda x: os.path.getmtime(os.path.join(c_dir, x))
                        )
    list_of_files.reverse()
    print( "Select file")

    for id, entry in enumerate(list_of_files): 
        print ("%s - %s" %( id, entry))
    
    selection=raw_input("Select:") 
    return list_of_files[int(selection)]

def __restore_table():
    global config
    backupFileName = '{0}/{1}'.format( config.param("backup_dir"),  file_chooser() )
    print ("Trying restore from backup {}".format(backupFileName))
    userPassword = config.param("user_password") 
    usePasswordPromt = ""
    env = {}
    if userPassword is None :
        usePasswordPromt = "-w"
    else:
        env={ 'PGPASSWORD': userPassword }

    dump_success = True
    command = 'dropdb  -h {} -U {} -p {} {} --if-exist {}'\
              .format( 
                    config.param("host_name"),
                    config.param("user_name"), 
                    config.param("port"), 
                    usePasswordPromt,
                    config.param("database_name")
                    )
    command = shlex.split(command)
    try:
        p = Popen(command, shell=False, stdin=PIPE,stdout=PIPE, stderr=PIPE, env=env)
        p.wait()
    except Exception as e:
        print('Exception happened during drop database  %s' %(e))    



    command = 'createdb -h {} -U {} -p {} {} {}'\
              .format( 
                    config.param("host_name"),
                    config.param("user_name"), 
                    config.param("port"), 
                    usePasswordPromt,
                    config.param("database_name")
                    )
    command = shlex.split(command)
    try:
        p = Popen(command, shell=False, stdin=PIPE,stdout=PIPE, stderr=PIPE, env=env)
        p.wait()
    except Exception as e:
        print('Exception happened during create database %s' %(e))    



    command = 'pg_restore --format=c -h {} -d {} -U {} -p {} {} {}'\
              .format( 
                    config.param("host_name"),
                    config.param("database_name"),
                    config.param("user_name"), 
                    config.param("port"), 
                    usePasswordPromt,
                    backupFileName
                    )
    command = shlex.split(command)
    
    try:
        p = Popen(command, shell=False, stdin=PIPE,stdout=PIPE, stderr=PIPE, env=env)
        p.wait()
        if (p.returncode != 0 ):
            print(p.stderr.read())
            dump_success = False

    except Exception as e:
        dump_success = False
        print('Exception happened during dump %s' %(e))

    return dump_success


def main():
    global config
    config.read_config();

    menu = {}
    menu['1']="Backup" 
    menu['2']="Restore"
    menu['3']="Exit"
    options=menu.keys()
    options.sort()
    for entry in options: 
        print ("%s - %s" %( entry, menu[entry]))

    selection=raw_input("Select:") 
    os.system('clear')
    if selection =='1': 
        if __dump_table():
            print('db dump successfull')
    elif selection == '2': 
        if __restore_table():
            print('db restore successfull')
    elif selection == '3':
        print ("exitig..." )
        return
    

if __name__ == "__main__":
    main()
    time.sleep(3)
    exit(0)