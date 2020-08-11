import yfinance as yf
import csv
import pandas as pd
from bs4 import BeautifulSoup as bs4
import requests

def get_html(url):
	request = requests.get(url)
	return request.text

#write news links and titles to csv
def write_news_csv(data):
	with open(company_name + '_news' + '.csv', 'a+') as file:
		writer = csv.writer(file)
		writer.writerow((data['title'], data['link']))

#get historical dara and write to csv
def get_data(company):
	data = yf.download(company.upper(), period='max')
	data['3_days_before_change'] = data['Close'] / data['Adj Close'].shift(3)
	filename = company + '.csv'
	data = data.sort_values(by="Date", ascending=False) 
	data.to_csv(filename)

#scrape data from news
def get_news(html):
	data = {}
	soup = bs4(html, 'lxml')
	for news in soup.find_all('li', class_="js-stream-content Pos(r)"):
		title = news.find('h3').text
		link = 'https://finance.yahoo.com/quote/' + company_name + news.find('a').get('href')
		data = {'title': title, 'link': link}
		write_news_csv(data)


if __name__ == '__main__':
	company_name = str(input('Enter company short name: '))
	url = 'https://finance.yahoo.com/quote/' + company_name + '/news?p=' + company_name.upper()
	get_data(company_name)
	get_news(get_html(url))
