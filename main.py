import sys
from flask import Flask, render_template, make_response, request
from convert import convert_file

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/convert', methods=["post"])
def convert():
	file = request.files['datafile']
	mimetype = ""
	if file.filename.endswith(".dbf"):
		mimetype = ".csv"
	elif file.filename.endswith(".csv"):
		mimetype = ".dbf"
	else:
		return
	result = convert_file(file)
	response = make_response()
	response.data = result
	downloadFileName = file.filename[:-4] + mimetype
	response.headers["Content-Disposition"] = "attachment; filename=" + downloadFileName
	return response

if __name__ == '__main__':
	app.run()