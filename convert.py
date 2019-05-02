# -*- coding: utf-8 -*-
import csv,os,sys,io
from StringIO import StringIO
from dbfpy import dbf
#import pandas as pd

#to be able to deal a huge CSV
csv.field_size_limit(1000000000)

def convert_file(file_to_convert):
	file_name = file_to_convert.filename
	if file_name.endswith('.dbf'):
		return convert_dbf_to_csv(file_to_convert)
	elif file_name.endswith('.csv'):
		return convert_csv_to_dbf(file_to_convert)
	elif file_name.endswith('.xls') or file_to_convert.endswith('.xlsx'):
		data = pd.read_excel(file_to_convert, 'Sheet1', index_col=None)
		data.to_csv(file_to_convert[:-4]+ ".csv", encoding='utf-8')
		return convert_csv_to_dbf(data)
	else:
		print("Filename does not end with .dbf or .csv")


def convert_dbf_to_csv(dbffile):
	file_name = dbffile.filename
	in_db = dbf.Dbf(dbffile)
	f = StringIO()
	writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL, lineterminator="\n")
	names = []
	for field in in_db.header.fields:
		names.append(field.name)
	writer.writerow(names)
	for rec in in_db:
		writer.writerow(rec.fieldData)
	print(writer)
	return f.getvalue()

def convert_csv_to_dbf(csvfile):
	filename = csvfile.filename
	reader = csv.reader(csvfile)
	f = io.BytesIO()
	out_db = dbf.Dbf(f, new=True)
	#make database-fields by CSV header
	header = next(reader)
	for col in header:
		out_db.addField((col,'C',20))
	for row in reader:
		rec = out_db.newRecord()
		for i in range(len(header)):
			rec[header[i]] = row[i]
		rec.store()
	out_db.flush()
	return f.getvalue()