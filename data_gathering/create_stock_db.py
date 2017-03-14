#Creates database for a sample range of stocks
#Sample will include the sp 500 (or all of NYSE/NASDAQ)
#Max Liu
#NOTHING IN THIS FILE WAS USED FOR THE FINAL PRODUCT


import data_gathering
from collections import OrderedDict
import sqlite3
import csv


def fin_data_dict(list_of_tickers):
    '''
    creates dictionary for multiple tickers
    '''
    stock_fin = OrderedDict()
    stock_dates = OrderedDict()
    for stock in list_of_tickers:
        temp_fin, temp_dates = data_gathering.collect_fin_data(stock)
        if len(temp_fin['Income Statement']) > 2:
            stock_fin[stock.upper()] = temp_fin
            stock_dates[stock.upper()] = temp_dates

    return stock_fin, stock_dates


def sum_info_dict(list_of_tickers):
    '''
    creates dictionary of summary data for multiple stocks
    '''
    summary = {}
    for stock in list_of_tickers:
        summary[stock.upper()] = data_gathering.summary_info(stock)

    return summary


def stock_list_csv(list_of_tickers):
    '''
    takes a list of tickers and creates a csv file with all of them
    '''
    final_dict = OrderedDict()
    for stock in list_of_tickers:
        temp_dict = data_gathering.collect_fin_data(stock)
        if len(temp_dict['Income Statement']) > 2:
            final_dict[stock.upper()] = temp_dict

    data_lst = []
    for stock_d in final_dict.values():
        for key, d in stock_d.items():
            for line_item in d.keys():
                if line_item != 'Ticker':
                    temp_lst = [d['Ticker']]
                    temp_lst.append(key)
                    temp_lst.append(line_item)
                    temp_lst.extend(d[line_item])
                    data_lst.append(temp_lst)

    with open('stock_financials.csv', 'wt') as fin_csv:
        fin_writer = csv.writer(fin_csv)
        for row in data_lst:
            fin_writer.writerow(row)

    return fin_csv


def init_sql_db(stock_fin_csv):
    '''
    create a sql database of financial data
    '''
    conn = sqlite3.connect("stock_data.db")
    c = conn.cursor()
    c.execute("CREATE TABLE stock_financials \
                (ticker VARCHAR, \
                    statement_type VARCHAR, \
                    line_item VARCHAR, \
                    year_1 BIGINT, \
                    year_2 BIGINT, \
                    year_3 BIGINT, \
                    year_4 BIGINT);")

    conn.commit()
    conn.close()