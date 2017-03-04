import bs4
import requests
import ast
import re
def get_interest_expense(ticker):
    ticker = ticker.lower()
    url = 'http://www.marketwatch.com/investing/stock/{}/financials'.format(ticker)
    r = requests.get(url)
    html = r.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    year_lst = []
    tr = soup.find_all('tr')
    th = tr[0].find_all('th')
    for year in th[1:-1]:
        text = year.get_text()
        year_lst.append(text)

    td = tr[23].find_all('td')
    #a = td[0].find_all('a')[0]
    #hmm = a.get('data-ref')
    #print(hmm)

    div = td[6].find_all('div')[0]
    string = div.get('data-chart')
    string = re.search('\[[\w,]+\]', string).group()
    string = string.replace('null', '"null"')
    expense_years = ast.literal_eval(string)
    return year_lst, expense_years
