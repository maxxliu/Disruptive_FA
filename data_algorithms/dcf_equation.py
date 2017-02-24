def dcf_calculator(data_dict, risk_factor, expected_return, growth_rate):
    '''
    Takes a nested dictionary and risk factor and returns price per share
    '''
    tax_rate = 0.35
    risk_free_rate = 0.0238 #10 year U.S. Treasury Bond
    summary = data_dict['summary quote']
    income_dict = data_dict['Income Statement']
    balance_sheet_dict = data_dict['Balance Sheet']
    cash_flow_dict = data_dict['Cash Flow']
    
    fcf_value_list = []
    pvfcf = 0

#this section calculates WACC
    average_debt = (sum(balance_sheet_dict['long term debt'])/4 + sum(balance_sheet_dict['short term debt'])/4)
    current_debt = balance_sheet_dict['long term debt'][3] + balance_sheet_dict['short term debt'][3]
    current_equity = balance_sheet_dict['Total equity'][3]
    total_d_e = current_debt + current_equity
    rd = income_dict['interest expense'] / average_debt #interest expense not listed on Nasdaq
    cost_equity = risk_free_rate + beta * (expected_return - risk_free_rate)
    WACC = (current_equity/total_d_e) * cost_equity + (debt/ total_d_e) * rd* (1 - tax_rate) #rd not pulled yet

    for year in range(4):
        beta = summary['beta'][year]
        gross_profit = income_dict['Total Revenue'][year] - income_dict['Cost of revenue'][year]
        EBITDA = gross_profit - income_dict['Selling general and Admin Expenses'][year]
        EBIT = EBITDA - cash_flow_dict['depreciation'][year] 

        capex = cash_flow_dict['capital expenditure'][year]
        total_liabilities = balance_sheet_dict['total_liabilities'][year]
        total_assets = balance_sheet_dict['total_assets'][year]
        nwc = total_liabilities - total_assets
        depreciation = cash_flow_dict['depreciation'][year]
        FCF = EBIT(1 - tax_rate) + depreciation - nwc - capex #NWC, depreciation, Capex not pulled yet
        
        year_value = FCF * (1 + growth_rate) / (WACC - growth_rate)
        present_value_year_value = year_value / ((1 + WACC) ** year)

        fcf_value_list.append(present_value_year_value)
    for fcf in fcf_value_list[:-1]:
        pvfcf += fcf


    enterprise_value = pvfcf + fcf_value_list[-1]
    cash = balance_sheet_dict['cash and cash equivalents'][3]
    minor_interest = balance_sheet_dict['minority interest'][3]
    equity_value = enterprise_value - average_debt - preferred_stock - minor_interest + cash 
    price_per_share = equity_value / summary['shares_outstanding'] #shares_outstanding not pulled yet

    return price_per_share

        

