import requests
import re
from flask import Flask, render_template



def check_vin(vin):
	url = 'http://0.0.0.0:9000/check/'
	post_data = {
	    'vin':vin
	}
	# 提交并获取返回数据
	post_html = requests.post(url,data=post_data)

def download():
	url = 'http://0.0.0.0:9000/download/'
	# 提交并获取返回数据
	post_data = {
	}
	post_html = requests.get(url,data=post_data)

#check_vin("1M8TRMPAXZP060950,1M8TRMPAXZP060950,M8TRMPAXZP060950")
#download()
