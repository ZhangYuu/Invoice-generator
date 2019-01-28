import requests
import re
from flask import Flask, render_template, request, send_from_directory
from reportlab.pdfgen import canvas
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph,Frame
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import Image as platImage
from PIL import Image
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.graphics.shapes import Drawing, String
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
bootstrap = Bootstrap(app)

def split_tc(tc):
	newtable=[["Item","Service Length","Quantity","Price","Late Fee"]]
	for line in tc:
		if line !="" and len(line.split(','))==5:
			newtable.append(line.split(','))
	return newtable

def generate_pdf(pdfname,InvoiceNo,create_date,carrier,address,totalfee,tc,payment):
	#设置页面大小
	c = canvas.Canvas(pdfname+'.pdf',pagesize=A4)
	xlength,ylength = A4
	print('width:%d high:%d'%(xlength,ylength))
	#c.line(1,1,ylength/2,ylength)

	#设置文字类型及字号
	c.setFont('Helvetica',12)

	#简单的图片载入
	imageValue = 'test.jpg'
	#c.drawImage(imageValue,97,97,300,300)
	c.drawImage('test.jpg',50,750,200,50)

	#text gengerating
	def set_text(x,y,text1):
		indexVlaue = 0
		set_text = c.beginText(x,y)
		while(indexVlaue < ylength):
		    textStr = text1
		    #print('nextline,nextline%d'%indexVlaue)
		    set_text.textLine(textStr)
		    indexVlaue = indexVlaue + 1
		    break
		c.drawText(set_text)

	#tc = [['ELD Subscription & Data Plan','12/01/2018-12/01/2019 (12 month)','3','$1197','0']]
	atable = tc

	set_text(50,ylength-110,"Invoice#: "+InvoiceNo)
	set_text(400,ylength-110,"Created: "+create_date)
	set_text(50,ylength-150,"Supplier: United Bus Technology Inc.")
	set_text(50,ylength-165,"Address: 7926 Jones Branch Dr. Suite 630, McLean, VA 22102")
	set_text(50,ylength-190,"Motor Carrier:"+carrier)
	set_text(50,ylength-205,"Address:"+address)

	set_text(400,280,"Total Fee: $"+totalfee)
	set_text(50,250,"Thanks for purchase!")
	set_text(50,235,"For any further questions do not hesitate to contact us!")
	set_text(50,200,"Website: https://www.ubtshield.com/")
	set_text(50,185,"Address: 7926 Jones Branch Dr., Suite 630, VA 22102")
	set_text(50,170,"Phone: +1 202 800 6565")
	set_text(50,155,"Email: shiled@ubt.io")
	if payment == "Paid":
		c.drawImage('paid.jpg',400,200,120,120)
	elif payment == "Not Paid":
		c.drawImage('notpaid.jpg',400,200,120,120)

	t = Table(atable,colWidths=[150,170,40,60,60])
	t.setStyle(TableStyle([('ALIGN',(0,0),(4,len(atable)-1),'CENTER'),
	                       ('INNERGRID',(0,0),(-1,-1),0.25,colors.black),
	                       ('BOX',(0,0),(-1,-1),0.25,colors.black),
	                       ]))
	t.split(0,0)
	t.drawOn(c,50,ylength-400,1)
	c.showPage()
	#换页的方式不同的showPage  c.drawString(0,0,'helloword')
	c.save()

#generate_pdf('test','2012386231231',"08/08/2019",'What the fuck Technology','12000',split_tc(['','',"ELD Subscription & Data Plan,12/01/2018-12/01/2019 (12 month),3,$1197,0"]))

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/check/',methods=['POST'])
def check():
	if request.method == 'POST':
		pdfname = request.form['pdfname']
		InvoiceNo = request.form['InvoiceNo']
		create_date = request.form['create_date']
		carrier = request.form['carrier']
		address = request.form['address']
		totalfee = request.form['totalfee']
		tc = [request.form['tc1'],request.form['tc2'],request.form['tc3'],request.form['tc4'],request.form['tc5']]
		payment = request.form["payment"]
		generate_pdf(pdfname,InvoiceNo,create_date,carrier,address,totalfee,split_tc(tc),payment)
		return render_template("index.html",error="works well")
#		else:
#			return render_template("index.html",error="bad input")
	else:
		return render_template("index.html")

@app.route("/download/")
def download_file():
	directory=os.getcwd()
	return send_from_directory(directory, 'test.pdf', as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=9000,debug=app.debug)

#split_vin("1M8TRMPAXZP060950,1M8TRMPAXZP060950")
#check_vin("1M8TRMPAXZP060950")


