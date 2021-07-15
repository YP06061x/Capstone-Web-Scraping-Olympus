from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")
print(table.prettify()[1:500])

#find your right key here
table = soup.find('table', attrs={'class':'table table-striped table-hover table-hover-solid-row table-simple history-data'})
tr = table.find_all('tr',attrs={'class':""})
tr[:5]

row_length = len(tr)

temp = [] #initiating a list 

for i in range(1, row_length):
#insert the scrapping process here
    
    row = table.find_all('tr',attrs={'class':""})[i]

	date = row.find_all('td')[0].text
    date = date.strip()

	day = row.find_all('td')[1].text
    day = day.strip()

	idr = row.find_all('td')[2].text
    idr = idr.strip()

	remarks = row.find_all('td')[3].text
    remarks = remarks.strip()

	temp.append((date,day,idr,remarks))
temp

temp = temp[::-1]
temp[:10]

#change into dataframe
exchange = pd.DataFrame(temp, columns = ('date','day','idr','remarks'))

#insert data wrangling here
exchange = exchange[['date','idr']]
exchange['idr'] = exchange['idr'].replace('IDR',"",regex=True).replace(',',"",regex=True)
exchange['idr'] = exchange['idr'].astype('float64')
exchange['date'] = exchange['date'].astype('datetime64')
exchangerate= exchange.set_index('date')
exchangerate

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'USD {round(exchangerate["idr"].mean(),2)}' #be careful with the " and ' 

	# generate plot
	ax = exchangerate.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)