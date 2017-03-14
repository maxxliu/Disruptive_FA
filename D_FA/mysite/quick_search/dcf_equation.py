import pandas as pd


def partial(func, *args, **keywords): #this is a curry function that will be used to get y value from the linear regression line
    '''
    This partial, currying function takes in another function, and default arguments and returns a new function that 
    has these default arguments.

    Example:
    a line function usually would take in slope, y intercept, and x value to get its corresponding y value 
    curry = partial(get_values, slope=5, y_int = 1)
    curry(year = 1) -> 6

    '''
    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*(args + fargs), **newkeywords)
    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc


def get_current_ebit(fin_dict):
    '''
    This helper function finds a company's current Earnings before interest and tax.
   EBIT =  total revenue - cost of revenue - sga (sales, general, and admin) - depreciation
   This function accesses the financial dictionary for all these values.
    '''
    revenue = fin_dict['Income Statement']['Total Revenue'][-1]
    cost = fin_dict['Income Statement']['Cost of Revenue'][-1]
    sga = fin_dict['Income Statement']['Sales, General and Admin.'][-1]
    depreciation = fin_dict['Cash Flow']['Depreciation'][-1]
    return revenue - cost - sga - depreciation


def get_rd(fin_dict):
    '''
    This function finds a company's cost of debt.  It takes a financial dictionary as its input.
    It accesses this dictionary to get the company's interest expense.  It uses the helper function get_current_ebit
    to find a company's ebit.  It then calculates the interest coverage ratio(icr) = ebit / interest_expense.
    Based on Aswath Damodaran's icr to credit rating estimation table, it matches a company's icr to its credit rating 
    cost of debt score.  These values are in credit_rating_values where the first index value is AAA, the next AA,
    the next A etc.  There are two tables, one for companies above 5B market cap and ones below 5B.  We find a company's
    market cap in the financial dictionary. 
    '''
    credit_rating_values = [0.04, 0.045, 0.05, 0.055, 0.085, 0.1, 0.12]
    market_cap = fin_dict['Summary Data']['market cap']
    ebit = get_current_ebit(fin_dict)
    interest_expense = fin_dict['Income Statement']['Interest Expense'][-1]
    if interest_expense == 0: #accounts for dividing by 0
        return credit_rating_values[0]
    icr = ebit / interest_expense
    value = -1
    if market_cap > 5000000000: #for market cap greater than 5 B 
        if icr >= 3: #makes searching for what icr range the icr value falls under.
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
            elif icr >= 1.25:
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


def linear_regression(year_value_lst):
    '''
    Takes in a list of financial values for a set number of years and
    returns the slope and y intercept of its respective linear regression line.
    This linear_regression function also accounts for missing values.  If it sees more than 
    one zero but total zeros are less than total number of values, it sets potential_error as True.
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
    Calculates the weighted average cost of capital.  This function takes in financial dictionary and 
    expected return, which is an investor's risk averse score.  
    WACC = (equity/total equity and debt) * cost_equity + (current_debt / total equity and debt) * rd * (1-tax_rate).
    The function returns a company's WACC value, which will be used to discount future cash.
    '''
    risk_free_rate = 0.02587 #10 year U.S. Treasury Bond
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
    '''
    This helper function tests to see if there are less than 3 years worth of data, no data, and if revenue = 0. 
    If either are True, the function returns True, meaning that there is not sufficient data to create a DCF. 
    '''
    value_lst = fin_dict['Income Statement']['Total Revenue']
    if len(value_lst) <= 3:
        return True
    test = list(set(value_lst))
    if len(test) < 1 or test[0] == 0:
        return True


def find_slope_intercept(fin_dict):
    '''
    This function finds all the slope and y intercepts for a financial value's respective
    linear regression line.  This function returns a list of tuples where each tuple is the 
    corresponding curry partial function and potential error value.  It also returns the current nwc
    '''
    curry_error_lst = []

    s, y, p_error = linear_regression(fin_dict['Income Statement']['Total Revenue'])
    curry = partial(get_values, slope = s, y_int = y)
    curry_error_lst.append((curry, p_error))

    s, y, p_error = linear_regression(fin_dict['Income Statement']['Cost of Revenue'])
    curry = partial(get_values, slope = s, y_int = y)
    curry_error_lst.append((curry, p_error))

    s, y, p_error = linear_regression(fin_dict['Income Statement']['Sales, General and Admin.'])
    curry = partial(get_values, slope = s, y_int = y)
    curry_error_lst.append((curry, p_error))

    s, y, p_error = linear_regression(fin_dict['Cash Flow']['Depreciation'])
    curry = partial(get_values, slope = s, y_int = y)
    curry_error_lst.append((curry, p_error))

    nwc_list = NWC(fin_dict)
    s, y, p_error = linear_regression(nwc_list)
    curry = partial(get_values, slope = s, y_int = y)
    curry_error_lst.append((curry, p_error))

    s, y, p_error = linear_regression(fin_dict['Cash Flow']['Capital Expenditures'])
    curry = partial(get_values, slope = s, y_int = y)
    curry_error_lst.append((curry, p_error))
    return curry_error_lst, nwc_list[-1]


def get_financial_values(future_year, curry_error_lst, tax_rate, past_nwc):
    '''
    This function takes in the future year, the list of slopes and y intercepts, the tax rate, and the past 
    nwc (will be used to calculate delta nwc).  It saves total revenue, cost of revenue, gross profit, sga,
    ebitda, depreciation, ebit, nwc, delta_nwc, capital expenditures, and fcf for a given future year to financal value list.
    This function finally returns this financial value list and the future year's nwc. 
    '''
    financial_val_lst = []
    total_revenue = curry_error_lst[0][0](year=future_year)
    cost_of_revenue = curry_error_lst[1][0](year=future_year)
    gross_profit = total_revenue - cost_of_revenue
    sga = curry_error_lst[2][0](year=future_year)
    ebitda = gross_profit - sga
    depreciation = curry_error_lst[3][0](year=future_year)
    ebit = ebitda - depreciation
    nwc = curry_error_lst[4][0](year=future_year)
    delta_nwc = nwc - past_nwc
    capex = curry_error_lst[5][0](year=future_year)
    fcf = ebit * (1 - tax_rate) + depreciation - delta_nwc + capex

    financial_val_lst += [total_revenue] + [cost_of_revenue] + [gross_profit] + [sga] + [ebitda] + [depreciation] + [ebit] + [delta_nwc] + [capex] + [fcf] 
    return financial_val_lst, nwc

#These are index labels for the fcf breakdown dataframe
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
    Takes a nested dictionary, expected_return (based on an investor's risk averse score), 
    growth_rate (default is average between interest rate and GDP growth) and returns actual price per share of company
    the financial calcuations table for all future cash flows, list of years, inaccurate rating, and buy/ sell rating.
    The calculator assumes the tax rate to be 35 percent and that preferred stock is negligible
    '''
    tax_rate = 0.35
    pvfcf = 0
    WACC_val = WACC(fin_dict, expected_return)
    last_date = fin_dict['Dates'][-1][-4:]
    last_date = int(last_date)
    year_lst = []

    inaccurate = False
    inaccurate = dcf_feasibility(fin_dict)
    if inaccurate:
        return None, None, None, True, None
        
    current_year_index = len(fin_dict['Dates']) - 1
    current_debt = fin_dict['Balance Sheet']['Long-Term Debt'][-1] + fin_dict['Balance Sheet']['Short-Term Debt / Current Portion of Long-Term Debt'][-1]
    financial_table = []
    slope_int_lst, past_nwc = find_slope_intercept(fin_dict)
    pvfcf = 0
    
    for year in range(1,6): #each year represents one of the 5 future years
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
    equity_value = enterprise_value - current_debt - minor_interest + cash 
    number_of_shares = fin_dict['Summary Data']['market cap'] / fin_dict['Summary Data']['previous close']
    price_per_share = equity_value / number_of_shares 

    if price_per_share > fin_dict['Summary Data']['previous close']:
        rating = 'BUY'
    else:
        rating = 'SELL'

    return price_per_share, financial_table, year_lst, inaccurate, rating 

