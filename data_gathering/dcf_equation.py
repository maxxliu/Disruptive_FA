def dcf_calculator(data_dict, risk_factor, expected_return, growth_rate):
    '''
    Takes a nested dictionary and risk factor and returns price per share
    '''
    tax_rate = 0.35
    risk_free_rate = 0.0238 #10 year U.S. Treasury Bond
    summary = data_dict['summary quote']
    
    fcf_value_list = []
    pvfcf = 0
    for year in range(4):

        beta = summary['beta'][year]

        income_dict = data_dict['Income Statement']
        balance_sheet = data_dict['Balance Sheet']

        gross_profit = income_dict['Total Revenue'][year] - income_dict['COGS'][year]
        EBITDA = gross_profit - income_dict['Selling gneral and Admin Expenses'][year]
        EBIT = EBITDA - income_dict['Research and Development'][year] - income_dict['Non-Recurring Items'][3] - income_dict['Other Operating Items'][3]
        debt = balance_sheet['total liabilities'][year]
        equity = balance_sheet['Total Stockholders Equity'][year]
        total_d_e = debt + equity
        cost_equity = risk_free_rate + beta * (expected_return - risk_free_rate)
        WACC = (equity/total_d_e) * cost_equity + (debt/ total_d_e) * rd* (1 - tax_rate)

        FCF = EBIT(1 - tax_rate) + depreciation - NWC - Capex #NWC, depreciation, Capex not pulled yet
        
        year_value = FCF * (1 + growth_rate) / (WACC - growth_rate)
        present_value_year_value = year_value / ((1 + WACC) ** year)

        fcf_value_list.append(present_value_year_value)
    for fcf in fcf_value_list[:-1]:
        pvfcf += fcf


    enterprise_value = pvfcf + fcf_value_list[-1]
    equity_value = enterprise_value - debt - preferred_stock - minor_interest + cash
    price_per_share = equity_value / shares_outstanding

    return price_per_share

        

