import getpass
from mysql.connector import connect
import sys
import os
import numpy as np
import pandas as pd

HOST = ''
USER = ''
DB = ''
PASS = ''
PORT = 


def connect_to_db():
    global CONNECTION
    print(
        """[+]You have to connect to the database for you to use the database[+] \n[+]please enter below the password of user '{0}'[+]""".format(
            USER))

    try:
        CONNECTION = connect(host=HOST, user=USER, passwd=PASS, db=DB, port=PORT)
    except Exception as e:
        print(str(e))
        retry = input('Do yo want to retry connection (y/n):')
        retry = str(retry)
        if retry.lower() == 'y':
            connect_to_db()
        else:
            print('You have decided to exit,Bye')
            CONNECTION.close()
            sys.exit()

def Get_Column_Names_Of_Table(table_name):
    cu = CONNECTION.cursor()
    cu.execute(
        "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{0}' AND TABLE_NAME = '{1}'".format(
            DB, table_name))
    columns = []
    for cl in cu:
        cl = str(cl).strip('(,)')
        cl = cl.strip("''")
        columns.append(cl)
    return columns

def get_client_data(data):
	client_data = data['clinic_number']
	return client_data
	
def check_data_length(client_data):
	wrong_client_number = []
	
	#Check if there is data
	if len(client_data) > 0:
		#clean_data
		for i in range(len(client_data)):
			if len(client_data[i]) != 10:
				#Data is wrong
				#get those client
				#client_id = client_data[i]
				pass
	return client_data		
	
def clean_data(client_data):
	chars = ['/', '\\','-','*']
	if len(client_data) > 0:
		for i in range(len(client_data)):
			if not client_data[i].isdigit():
				change = client_data[i]
				##Get the record that is has alpha and replace then
				for c in change:
					if c.isalpha():
						change = change.replace(c,str(0))
						client_data[i] = change
						if c in chars:
							change = change.replace(c,str(0))
							client_data[i] = change
									
								
	return client_data	

def restore_data(dataframe,series):
		clean = clean_data(series)
		dataframe['clinic_number'] = clean
		return dataframe
					

def Query_Table(table_name,mfl):
	try:
		table_columns = Get_Column_Names_Of_Table(table_name)
	except Exception as e:
		print(e)
	try:	
		query = "select * from {0} where mfl_code={1}".format(table_name,mfl)
		data_frame = pd.read_sql(query, CONNECTION, parse_dates=True)
		data_frame.columns = table_columns
	except Exception as e:
		print(e)
	return data_frame	
	
connect_to_db()
data = Query_Table('tbl_client',10100)
print(data[:4])
data.to_csv('original.csv', index=False)
cd = get_client_data(data)
clean = clean_data(cd)
cleaned = restore_data(data,clean)
print(cleaned[:4])
cleaned.to_csv('cleaned.csv', index=False)
