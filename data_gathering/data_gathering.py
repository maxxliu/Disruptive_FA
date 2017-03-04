# Financial Statement Data Scraping
# Max Liu


import bs4
import requests
from collections import OrderedDict
import csv


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
    '''
    ticker = ticker.lower()
    url_p1 = "https://www.nasdaq.com/symbol/"
    url_p2 = "/financials?query="
    rough_url = url_p1 + ticker + url_p2

    i_s = rough_url + "income-statement"
    b_s = rough_url + "balance-sheet"
    c_f = rough_url + "cash-flow"

    return [("Income Statement", i_s), ("Balance Sheet", b_s), ("Cash Flow", c_f)]


def clean_text(tr_tag):
    '''
    return clean list of data
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


def collect_fin_data(ticker):
    '''
    takes a ticker and collect financial data relating to the ticker
    '''
    data_dict = OrderedDict()
    date_dict = OrderedDict()
    urls = create_urls(ticker)

    for pair in urls:
        fin_type = pair[0]
        url = pair[1]

        data_dict[fin_type] = OrderedDict()
        current_dict = data_dict[fin_type]
        current_dict['Ticker'] = ticker.upper()

        r = requests.get(url)
        html = r.text 
        soup = bs4.BeautifulSoup(html, "lxml")

        data_loc = soup.find_all('table')[5]
        raw_data = data_loc.find_all('tr')

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


    return data_dict, date_dict


def summary_info(ticker):
    '''
    Takes a ticker and creates a dictionary of summary information
    '''
    summary_d = {}

    ticker = ticker.lower()
    url = 'http://www.nasdaq.com/symbol/' + ticker
    r = requests.get(url)
    html = r.text
    soup = bs4.BeautifulSoup(html, 'lxml')
    data_tables = soup.find_all('table')[8].find_all('td')

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

    for i in range(len(keys)):
        summary_d[keys[i]] = values[i]
            
    return summary_d


def create_csv(data_dict):
    '''
    convert dictionary into csv file
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


