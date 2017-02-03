# Financial Statement Data Scraping
# Max Liu


import bs4
import requests


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
        if item != 'Trend' and len(item) > 0:
            clean_dates.append(item)

    dates = clean_dates[1:]
    dates.reverse()

    return clean_dates[0].strip(':'), dates 


def collect_fin_data(ticker):
    '''
    takes a ticker and collect financial data relating to the ticker
    '''
    data_dict = {}
    urls = create_urls(ticker)

    for pair in urls:
        fin_type = pair[0]
        url = pair[1]

        data_dict[fin_type] = {}
        current_dict = data_dict[fin_type]

        r = requests.get(url)
        html = r.text 
        soup = bs4.BeautifulSoup(html, "lxml")

        data_loc = soup.find_all('table')[5]
        raw_data = data_loc.find_all('tr')

        clean_tags = []
        for tag in raw_data:
            if tag.next_sibling == '\n':
                clean_tags.append(tag)

        date_key, dates = get_dates(clean_tags[0])

        current_dict[date_key] = dates

        for tag in clean_tags[1:]:
            key_name, data_vals = clean_text(tag)
            if key_name != 0:
                current_dict[key_name] = data_vals


    return data_dict