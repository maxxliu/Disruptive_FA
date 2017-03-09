import pandas as pd


def get_current_ebit(fin_dict):
    revenue = fin_dict['Income Statement']['Total Revenue'][-1]
    cost = fin_dict['Income Statement']['Cost of Revenue'][-1]
    sga = fin_dict['Income Statement']['Sales, General and Admin.'][-1]
    depreciation = fin_dict['Cash Flow']['Depreciation'][-1]
    return revenue - cost - sga - depreciation


def get_rd(fin_dict):
    credit_rating_values = [0.04, 0.045, 0.05, 0.055, 0.085, 0.1, 0.12]
    market_cap = fin_dict['Summary Data']['market cap']
    ebit = get_current_ebit(fin_dict)
    interest_expense = fin_dict['Income Statement']['Interest Expense'][-1]
    icr = ebit / interest_expense
    value = -1
    if market_cap > 5000000000:
        if icr >= 3:
            if icr < 6.5:
                value = 2
            elif icr < 8.5:
                value = 1
            else:
                value = 0
        else:
            if icr >= 2.5:
                value = 3
            elif icr >= 2:
                value = 4
            elif icr >= 1.25
                value = 5
            else:
                value = 6
    else:
        if icr >= 4.5:
            if icr < 9.5:
                value = 2
            elif icr < 12.5:
                value = 1
            else:
                value = 0
        else:
            if icr >= 4:
                value = 3
            elif icr >= 3:
                value = 4
            elif icr >= 1.5:
                value = 5
            else:
                value = 6
    return credit_rating_values[value]





def data_dictionary(dates, stock_list):
    '''
    Takes in a dates object and a list of objects where each object represents 
    given financial values for a certain amount of years for a given company.  It inputs
    the dates and values into a financials dictionary
    '''
    financials_dict = {}
    financials_dict['Dates'] = (dates.year_1, dates.year_2, dates.year_3, dates.year_4)
    for obj in stock_list:
        financials_dict[obj.line_item] = (obj.year_1_val, obj.year_2_val, obj.year_3_val, obj.year_4_val)
    return financials_dict

def linear_regression(year_value_lst):
    '''
    Takes in a list of financial values for a set number of years and
    returns the slope and y intercept of its respective linear regression line
    '''
    x_bar = sum(range(len(year_value_lst)))/len(year_value_lst)
    y_bar = sum(year_value_lst)/len(year_value_lst)
    sum_xy = 0
    sum_x_squared = 0
    count = 0 #counts for 0s
    potential_error = False
    for i in range(len(year_value_lst)):
        x_difference = i - x_bar
        if year_value_lst[i] == 0:
            count += 1
        xy = i * year_value_lst[i]
        sum_xy += xy
        x_squared = i ** 2
        sum_x_squared += x_squared
    mean_xy = sum_xy / len(year_value_lst)
    mean_x_squared = sum_x_squared / len(year_value_lst)
    if count > 0 and count < len(year_value_lst):
        potential_error = True
    slope = (x_bar * y_bar - mean_xy) / ((x_bar ** 2) - mean_x_squared)
    y_int = y_bar - slope * x_bar
    return slope, y_int, potential_error




def get_values(slope, y_int, year):
    '''
    Takes in a slope, y-intercept, and a year represented as an index 
    and returns its expected year value
    '''
    return slope * year + y_int



def WACC(fin_dict, expected_return):
    '''
    Calculates the weighted average cost of capital
    '''
    risk_free_rate = 0.0246
    tax_rate = 0.35
    current_debt = fin_dict['Balance Sheet']['Long-Term Debt'][-1] + fin_dict['Balance Sheet']['Short-Term Debt / Current Portion of Long-Term Debt'][-1]
    current_equity = fin_dict['Balance Sheet']['Total Equity'][-1]
    total_d_e = current_debt + current_equity
    beta = fin_dict['Summary Data']['beta']
    rd = get_rd(fin_dict)
    cost_equity = risk_free_rate + beta * (expected_return - risk_free_rate)
    WACC_val = (current_equity/total_d_e) * cost_equity + (current_debt/ total_d_e) * rd* (1 - tax_rate) #rd not pulled yet
    return WACC_val

def NWC(fin_dict):
    '''
    Accesses a financial dictionary for totat assets and total Liabilities for a given year.  
    It takes the x_difference, which the net working capital and appends nwc to a nwc list
    The function returns the nwc
    '''
    nwc_list = []
    for i in range(len(fin_dict['Balance Sheet']['Total Current Assets'])):
        nwc_value = fin_dict['Balance Sheet']['Total Current Assets'][i] - fin_dict['Balance Sheet']['Total Current Liabilities'][i]
        nwc_list.append(nwc_value)
    return nwc_list

def dcf_feasibility(fin_dict):
    value_lst = fin_dict['Income Statement']['Total Revenue']
    assert len(value_lst) >= 3, 'Not enough years to create a meaningful DCF'
    test = list(set(value_lst))
    assert len(test) > 1 and test[0] != 0, 'Not enough information to create a meaningful DCF'





def find_slope_intercept(fin_dict):
    '''
    This function finds all the slope and y intercepts for a financial value's respective
    linear regression line.  This function returns a list of tuples where each tuple is a slope
    and its corresponding y intercept.  It also returns the current nwc
    '''
    slope_int_lst = []
    dcf_feasibility(fin_dict)
    slope_int_lst.append(linear_regression(fin_dict['Income Statement']['Total Revenue']))
    slope_int_lst.append(linear_regression(fin_dict['Income Statement']['Cost of Revenue']))
    slope_int_lst.append(linear_regression(fin_dict['Income Statement']['Sales, General and Admin.']))
    slope_int_lst.append(linear_regression(fin_dict['Cash Flow']['Depreciation']))
    nwc_list = NWC(fin_dict)
    slope_int_lst.append(linear_regression(nwc_list))
    slope_int_lst.append(linear_regression(fin_dict['Cash Flow']['Capital Expenditures']))
    return slope_int_lst, nwc_list[-1] 

def get_financial_values(future_year, slope_int_lst, tax_rate, past_nwc):
    '''
    This function takes in the future year, the list of slopes and y intercepts, the tax rate, and the past 
    nwc (will be used to calculate delta nwc).  It saves total revenue, cost of revenue, gross profit, sga,
    ebitda, depreciation, ebit, nwc, delta_nwc, capital expenditures, and fcf for a given future year to financal value list.
    This function finally returns this financial value list and the future year's nwc. 
    '''
    financial_val_lst = []
    total_revenue = get_values(slope_int_lst[0][0], slope_int_lst[0][1], future_year)
    cost_of_revenue = get_values(slope_int_lst[1][0], slope_int_lst[1][1], future_year)
    gross_profit = total_revenue - cost_of_revenue
    sga = get_values(slope_int_lst[2][0], slope_int_lst[2][1], future_year)
    ebitda = gross_profit - sga
    depreciation = get_values(slope_int_lst[3][0], slope_int_lst[3][1], future_year)
    ebit = ebitda - depreciation
    nwc = get_values(slope_int_lst[4][0], slope_int_lst[4][1], future_year)
    delta_nwc = nwc - past_nwc
    capex = get_values(slope_int_lst[5][0], slope_int_lst[5][1], future_year)
    fcf = ebit * (1 - tax_rate) + depreciation - delta_nwc + capex

    financial_val_lst += [total_revenue] + [cost_of_revenue] + [gross_profit] + [sga] + [ebitda] + [depreciation] + [ebit] + [delta_nwc] + [capex] + [fcf] 
    return financial_val_lst, nwc

financial_term_lst = ['Total Revenue', 'Cost of Revenue', 'Gross Profit', 'SGA', 'EBITDA', 'Depreciation',
'EBIT', 'Change in NWC', 'Capital Expenditures', 'FCF']

def numbers_dataframe(financial_table, year_lst, financial_term_lst):
    df = pd.DataFrame(financial_table)
    df = df.transpose()
    df.columns = year_lst
    df.index = financial_term_lst
    return df


def dcf_calculator(fin_dict, expected_return, growth_rate=0.0124):
    '''
    Takes a nested dictionary and risk factor and returns price per share
    '''
    tax_rate = 0.35
    risk_free_rate = 0.0238 #10 year U.S. Treasury Bond
    pvfcf = 0
    WACC_val = WACC(fin_dict, expected_return)
    last_date = fin_dict['Dates'][-1][-4:]
    last_date = int(last_date)
    year_lst = []

    current_year_index = len(fin_dict['Dates']) - 1
    current_debt = fin_dict['Balance Sheet']['Long-Term Debt'][-1] + fin_dict['Balance Sheet']['Short-Term Debt / Current Portion of Long-Term Debt'][-1]
    financial_table = []
    slope_int_lst, past_nwc = find_slope_intercept(fin_dict)
    preferred_stock = 0
    pvfcf = 0

    
    for year in range(1,6):
        future_year = current_year_index + year
        year_lst.append(last_date + year)
        financial_val_lst, past_nwc = get_financial_values(future_year, slope_int_lst, tax_rate, past_nwc)
        fcf = financial_val_lst[-1]
        nwc = financial_val_lst[7]
        present_future_value = fcf / ((1 + WACC_val) ** year)
        pvfcf += present_future_value
        financial_table.append(financial_val_lst)

    terminal_value = (fcf * (1 + growth_rate)) / (WACC_val - growth_rate)
    pvtv = terminal_value / ((1 + WACC_val) ** year)    
    enterprise_value = pvfcf + pvtv

    cash = fin_dict['Balance Sheet']['Cash and Cash Equivalents'][-1]
    minor_interest = fin_dict['Balance Sheet']['Minority Interest'][-1]
    equity_value = enterprise_value - current_debt - preferred_stock - minor_interest + cash 
    number_of_shares = fin_dict['Summary Data']['market cap'] / fin_dict['Summary Data']['previous close']
    price_per_share = equity_value / number_of_shares 

    return price_per_share, financial_table, year_lst

