import django
import os
import sys
import pandas as pd
import data_gathering

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()

from quick_search.models import Stock, Fin_Statement, Data_Date, Summary_Data

NYSE = pd.read_csv('NYSE.csv')
NASDAQ = pd.read_csv('NASDAQ.csv')

def fix_summary(summ_d):
    '''
    takes the summary dictionary and makes sure that all the keys are
    present and have a value

    Inputs:
        summ_d (dictionary): dictionary of summary data

    Returns:
        edited summary data dictionary
    '''
    for key, value in summ_d.items():
        if value == '':
            summ_d[key] = 0

    for key in ['1 Year Target', '52 Week High/Low', 'Beta', 'Market cap', \
                                                    'Previous Close']:
        if key in summ_d:
            if key != '52 Week High/Low':
                if type(summ_d[key]) == list:
                    summ_d[key] = 0
            else:
                try:
                    summ_d[key][0] = float(summ_d[key][0])
                except:
                    summ_d[key] = [0, 0]
        else:
            if key == '52 Week High/Low':
                summ_d[key] = [0, 0]
            else:
                summ_d[key] = 0


def populate_db():
    '''
    takes every single stock in a csv and gathers the data for the
    stock and inputs the data into the django database

    Inputs:
        None

    Returns:
        None. edits the django database and adds in all of the financial data
    '''
    for index, row in NASDAQ.iterrows():
        print(index)
        ticker1 = row['Symbol']
        name1 = row['Name']
        sector1 = row['Sector']
        industry1 = row['Industry']
        print(ticker1)

        try:
            summ_d = data_gathering.summary_info(ticker1)

            if summ_d != None:
                #add to stock table
                s = Stock(ticker=ticker1, name=name1, sector=sector1, \
                                                            industry=industry1)
                s.save()
                print('stock done')

                fix_summary(summ_d)
                #add to summary data table
                s_d = Summary_Data(ticker=s, \
                    target=float(summ_d['1 Year Target']), \
                    year_high=float(summ_d['52 Week High/Low'][0]), \
                    year_low=float(summ_d['52 Week High/Low'][1]), \
                    beta=float(summ_d['Beta']), \
                    market_cap=summ_d['Market cap'], \
                    previous_close=float(summ_d['Previous Close']))
                s_d.save()
                print('summary done')

        except:
            print('COULD NOT GET SUMMARY DATA')

        try:
            data, dates = data_gathering.collect_fin_data(ticker1)

            if data != None:
                #add to fin statement and data dates tables
                if len(data['Income Statement']) > 1:
                    data_lst = []
                    for key, d in data.items():
                        for line_item in d.keys():
                            if line_item != 'Ticker':
                                temp_lst = [d['Ticker']]
                                temp_lst.append(key)
                                temp_lst.append(line_item)
                                temp_lst.extend(d[line_item])
                                data_lst.append(temp_lst)

                    for lst in data_lst:
                        f = Fin_Statement(ticker=s, statement_type=lst[1], \
                            line_item=lst[2], year_1_val=lst[3], \
                            year_2_val=lst[4], year_3_val=lst[5], \
                            year_4_val=lst[6])
                        f.save()
                    print('financials done')

                    #add to data dates
                    lst = dates[ticker1]
                    dd = Data_Date(ticker=s, year_1=lst[0], year_2=lst[1], \
                                                year_3=lst[2], year_4=lst[3])
                    dd.save()
                    print('dates done')
        except:
            print('COULD NOT GET FINANCIAL DATA')

        print('complete')


def try_one(ticker1, name1, sector1, industry1):
    '''
    tests to see if a single stock can be added into database

    Inputs:
        ticker1 (string): stock ticker1
        name1 (string): name of the stock
        sector1 (string): sector of stock
        industry1 (string): industry of stock

    Returns:
        adds data into the django database
    '''
    summ_d = data_gathering.summary_info(ticker1)

    if summ_d != None:
        #add to stock table
        s = Stock(ticker=ticker1, name=name1, sector=sector1, \
                                                industry=industry1)
        s.save()
        print('stock done')

        for key, value in summ_d.items():
            if value == '':
                summ_d[key] = 0

        for key in ['1 Year Target', '52 Week High/Low', 'Beta', 'Market cap', \
                                                        'Previous Close']:
            if key in summ_d:
                if key != '52 Week High/Low':
                    if type(summ_d[key]) == list:
                        summ_d[key] = 0
                else:
                    try:
                        summ_d[key][0] = float(summ_d[key][0])
                    except:
                        summ_d[key] = [0, 0]
            else:
                if key == '52 Week High/Low':
                    summ_d[key] = [0, 0]
                else:
                    summ_d[key] = 0

        #add to summary data table
        s_d = Summary_Data(ticker=s, target=float(summ_d['1 Year Target']), \
            year_high=float(summ_d['52 Week High/Low'][0]), \
            year_low=float(summ_d['52 Week High/Low'][1]), \
            beta=float(summ_d['Beta']), \
            market_cap=summ_d['Market cap'], \
            previous_close=float(summ_d['Previous Close']))
        s_d.save()
        print('summary done')

        data, dates = data_gathering.collect_fin_data(ticker1)

        if data != None:
            #add to fin statement and data dates tables
            if len(data['Income Statement']) > 1:
                data_lst = []
                for key, d in data.items():
                    for line_item in d.keys():
                        if line_item != 'Ticker':
                            temp_lst = [d['Ticker']]
                            temp_lst.append(key)
                            temp_lst.append(line_item)
                            temp_lst.extend(d[line_item])
                            data_lst.append(temp_lst)

                for lst in data_lst:
                    f = Fin_Statement(ticker=s, statement_type=lst[1], \
                        line_item=lst[2], year_1_val=lst[3], \
                        year_2_val=lst[4], year_3_val=lst[5], year_4_val=lst[6])
                    f.save()
                print('financials done')

                #add to data dates
                lst = dates[ticker1]
                dd = Data_Date(ticker=s, year_1=lst[0], year_2=lst[1], \
                                            year_3=lst[2], year_4=lst[3])
                dd.save()
                print('dates done')

        print('complete')
