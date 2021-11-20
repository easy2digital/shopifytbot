from flask import Flask, render_template, request, flash
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

app = Flask(__name__)
app.secret_key = "lousieasy2digital_8888001"

@app.route("/hello")

def index():
	flash("Please enter the Shopify store domain")
	return render_template("index.html")


@app.route("/StoreUrl", methods=["POST", "GET"])
def StoreUrl():
	flash("Great! " + str(request.form['name_input']) + " - This is its store data, check it out!")
	shopifyweb = []
	e1 = str(request.form['name_input'])

	for x in range (1,3):

		URL = e1 + 'products.json?limit=250&page='
		productweb = requests.get(URL+str(x))
		ProductData = productweb.json()

		for item in ProductData['products']:
			try:
				title = (item['title'])
			except Exception as e:
				title = None

			try:
				created = (item['created_at'])
			except Exception as e:
				created = None

			try:
				vendor = (item['vendor'])
			except Exception as e:
				vendor = None

			try:
				handle = (item['handle'])
			except Exception as e:
				handle = None

			try:
				producttype = (item['product_type'])
			except Exception as e:
				producttype = None

			for variant in item['variants']:
				try:
					variants_title = (variant['title'])
				except Exception as e:
					variants_title = None

				try:
					SKU = (variant['sku'])
				except Exception as e:
					SKU = None

				try:
					price = (variant['price'])
				except Exception as e:
					price = None

				try:
					ComparePrice = (variant['compare_at_price'])
				except Exception as e:
					ComparePrice = None

				element_info = {
				'Title': title,
				'Created at': created,
				'Vendor': vendor,
				'URL': handle,
				'Product Type': producttype,
				'variants_title': variants_title,
				'SKU': SKU,
				'Price': price,
				'ComparePrice': ComparePrice
				}

			shopifyweb.append(element_info)

	df = pd.DataFrame(shopifyweb)
	df.to_csv('shopifydata.csv')
	return send_file('shopifydata.csv', mimetype='text/csv', attachment_filename='shopifydata.csv',as_attachment=True)
