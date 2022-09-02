import mysql.connector
createTable='C:/Users/Lenovo/Dropbox/JP/Internship/DataMigration/pythonSQL/sampleDatabase/create objects.sql'
loadData='C:/Users/Lenovo/Dropbox/JP/Internship/DataMigration/pythonSQL/sampleDatabase/load data.sql'
refinedTable='C:/Users/Lenovo/Dropbox/JP/Internship/DataMigration/pythonSQL/sampleDatabase/refinedTable.sql'


cnx = mysql.connector.connect(user='root',
                             password='8380',
                             host='localhost')
cursor =cnx.cursor()


def executeScriptsFromFile(filename):
    with open(filename, 'r') as fd:
        sqlFile = fd.read()
    sqlCommands = sqlFile.split(';')

    for command in sqlCommands:
        try:
            if command.strip() != '':
                cursor.execute(command)
        except Exception as msg:
            print ("Command skipped: ", msg)

executeScriptsFromFile(createTable)
executeScriptsFromFile(loadData)
executeScriptsFromFile(refinedTable)
cnx.commit()