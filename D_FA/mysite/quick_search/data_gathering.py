# Financial Statement Data Scraping
# Max Liu


import bs4
import requests
from collections import OrderedDict
import csv
import ast
import re


'''
example data structure for holding financial data

data = {"Period Ending": []
        "Income Statement": {"Total Revenue": []
                                "Cost of Revenue": []
        }
        "Balance Sheet": {}
        "Cash Flow": {}
        }
'''


def create_urls(ticker):
    '''
    create link to web page that holds data

    Inputs:
        ticker (string): stock ticker

    Returns:
        list of tuples with the statement type and url link
    '''
    url_p1 = "https://www.nasdaq.com/symbol/"
    url_p2 = "/financials?query="
    rough_url = url_p1 + ticker + url_p2

    i_s = rough_url + "income-statement"
    b_s = rough_url + "balance-sheet"
    c_f = rough_url + "cash-flow"

    return [("Income Statement", i_s), ("Balance Sheet", b_s), \
            ("Cash Flow", c_f)]


def clean_text(tr_tag):
    '''
    return clean list of data

    Inputs:
        tr_tag: a beautiful soup tag with data

    Returns:
        a list of the data gathered from the tag
    '''
    row_data = tr_tag.get_text()
    row_data = row_data.split('\n')

    clean_row = []
    for item in row_data:
        if len(item) > 0:
            clean_row.append(item)

    if len(clean_row) != 5:
        return 0, 0

    num_lst = []
    for item in clean_row[1:]:
        item = item.replace(',', '')
        if "(" in item:
            item = item.strip('()')
            item = int(item[1:]) * -1000
        else:
            item = int(item[1:]) * 1000
        num_lst.append(item)

    num_lst.reverse()

    return clean_row[0], num_lst


def get_dates(tr_tag):
    '''
    format and return period ending dates

    Inputs:
        tr_tag: a beautiful soup tag with data 

    Returns:
        a list of the dates that the financial data is from
    '''
    raw_str = tr_tag.get_text()
    raw_str = raw_str.split('\n')

    clean_dates = []
    for item in raw_str:
        item.replace('/', '')
        if item != 'Trend' and len(item) > 0:
            item.replace('/', '')
            clean_dates.append(item)

    dates = clean_dates[1:]
    dates.reverse()

    return clean_dates[0].strip(':'), dates 


def get_interest_expense(ticker):
    '''
    pulls interest expense data 

    Inputs:
        ticker (string): stock ticker

    Returns:
        a list of interest expense data from last 4 years
    '''
    ticker = ticker.lower()
    url = 'http://www.marketwatch.com/investing/stock/{}/financials'.format(ticker)
    r = requests.get(url)
    html = r.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    year_lst = []
    tr = soup.find_all('tr')
    try:
        th = tr[0].find_all('th')
    except:
        return [0, 0, 0, 0], [0, 0, 0, 0]
    for year in th[1:-1]:
        text = year.get_text()
        year_lst.append(text)

    expense_years = []
    for tag in tr:
        text = tag.get_text()
        if "Interest Expense" in text:
            td = tag.find_all('td')
            div = td[6].find_all('div')[0]
            string = div.get('data-chart')
            try:
                string = re.search('\[[\w,]+\]', string).group()
            except:
                return [0, 0, 0, 0], [0, 0, 0, 0]
            string = string.replace('null', '"null"')
            expense_years = ast.literal_eval(string)
            break

    for i, num in enumerate(expense_years):
        if num == "null":
            expense_years[i] = 0

    return year_lst, expense_years[1:]


def collect_fin_data(ticker):
    '''
    takes a ticker and collect financial data relating to the ticker

    Inputs:
        ticker (string): stock ticker

    Returns:
        a dictionary with financial data and a dictionary with dates
    '''
    ticker = ticker.lower()
    data_dict = OrderedDict()
    date_dict = OrderedDict()
    urls = create_urls(ticker)

    for pair in urls:
        fin_type = pair[0]
        url = pair[1]

        r = requests.get(url)
        if r.status_code == 404 or r.status_code == 403:
            return {}, {}
        html = r.text 
        soup = bs4.BeautifulSoup(html, "lxml")

        data_dict[fin_type] = OrderedDict()
        current_dict = data_dict[fin_type]
        current_dict['Ticker'] = ticker.upper()

        data_loc = soup.find_all('table')[5]
        raw_data = data_loc.find_all('tr')
        if len(raw_data) <= 1:
            return None, None

        clean_tags = []
        for tag in raw_data:
            if tag.next_sibling == '\n':
                clean_tags.append(tag)

        if len(date_dict) == 0:
            date_key, dates = get_dates(clean_tags[0])
            date_dict[ticker.upper()] = dates

        for tag in clean_tags[1:]:
            key_name, data_vals = clean_text(tag)
            if key_name != 0:
                current_dict[key_name] = data_vals

    if 'Interest Expense' in data_dict['Income Statement']:
        if data_dict['Income Statement']['Interest Expense'][-1] == 0:
            ie = get_interest_expense(ticker)[1]
            data_dict['Income Statement']['Interest Expense'] = ie


    return data_dict, date_dict


def summary_info(ticker):
    '''
    Takes a ticker and creates a dictionary of summary information

    Inputs:
        ticker (string): stock ticker

    Returns:
        a dictionary with summary data
    '''
    summary_d = {}

    ticker = ticker.lower()
    url = 'http://www.nasdaq.com/symbol/' + ticker
    r = requests.get(url)
    if r.status_code == 404 or r.status_code == 403:
        return None
    html = r.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    try:
        data_tables = soup.find_all('table')[8].find_all('td')
    except:
        return None

    keys = []
    values = []
    for i, tag in enumerate(data_tables):
        text = tag.get_text()
        if i % 2 == 0:
            text = text.strip('\n\r\t ')
            text = text.split('\r')
            keys.append(text[0])
        else:
            text = text.strip('$\n\r\xa0% ')
            text = text.replace('\xa0', '')
            text = text.replace(',', '')
            text = text.split('/')
            if len(text) > 1:
                text[1] = text[1].strip('$')
                values.append(text)
            else:
                values.append(text[0])

    try:
        for i in range(len(keys)):
            summary_d[keys[i]] = values[i]
    except:
        return None
            
    return summary_d


def create_csv(data_dict):
    '''
    convert dictionary into csv file

    Inputs:
        data_dict (dictionary): a dictionary of financial data 

    Returns:
        a csv file of data from financials dictionary
    '''
    data_lst = []
    for key, d in data_dict.items():
        for line_item in d.keys():
            if line_item != 'Ticker':
                temp_lst = [d['Ticker']]
                temp_lst.append(key)
                temp_lst.append(line_item)
                temp_lst.extend(d[line_item])
                data_lst.append(temp_lst)

    with open('stock_financials.csv', 'wt') as fin_csv:
        fin_writer = csv.writer(fin_csv)
        fin_writer.writerow(['Ticker', 'Statement Type', 'Line Item', 'Year 1', 'Year 2', 'Year 3', 'Year 4'])
        for row in data_lst:
            fin_writer.writerow(row)

    return fin_csv


