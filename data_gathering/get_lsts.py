# CS122
# DFA
# Max Liu

import pandas as pd 

def find_lists():
	'''
	creates a list of the possible indsutries and sectors 

	inputs:
		None

	Returns:
		a list of all possible industries and sectors
	'''
	nyse = pd.read_csv('NYSE.csv')
	nasdaq = pd.read_csv('NASDAQ.csv')

	nyse_lst_sectors = []
	nyse_lst_industry = []
	for row, val in nyse.iterrows():
		nyse_lst_sectors.append(val.Sector)
		nyse_lst_industry.append(val.Industry)

	nasdaq_lst_sectors = []
	nasdaq_lst_industry = []
	for row, val in nasdaq.iterrows():
		nasdaq_lst_sectors.append(val.Sector)
		nasdaq_lst_industry.append(val.Industry)

	final_sectors = nyse_lst_sectors + nasdaq_lst_sectors
	final_industry = nyse_lst_industry + nasdaq_lst_industry

	final_sectors = list(set(final_sectors))
	final_industry = list(set(final_industry))

	final_sectors.sort()
	final_industry.sort()

	return final_sectors, final_industry


SECTORS =
['Basic Industries',
 'Capital Goods',
 'Consumer Durables',
 'Consumer Non-Durables',
 'Consumer Services',
 'Energy',
 'Finance',
 'Health Care',
 'Miscellaneous',
 'Public Utilities',
 'Technology',
 'Transportation',
 'n/a']

INDSUTRY = 
['Accident &Health Insurance',
 'Advertising',
 'Aerospace',
 'Agricultural Chemicals',
 'Air Freight/Delivery Services',
 'Aluminum',
 'Apparel',
 'Auto Manufacturing',
 'Auto Parts:O.E.M.',
 'Automotive Aftermarket',
 'Banks',
 'Beverages (Production/Distribution)',
 'Biotechnology: Biological Products (No Diagnostic Substances)',
 'Biotechnology: Commercial Physical & Biological Resarch',
 'Biotechnology: Electromedical & Electrotherapeutic Apparatus',
 'Biotechnology: In Vitro & In Vivo Diagnostic Substances',
 'Biotechnology: Laboratory Analytical Instruments',
 'Books',
 'Broadcasting',
 'Building Materials',
 'Building Products',
 'Building operators',
 'Business Services',
 'Catalog/Specialty Distribution',
 'Clothing/Shoe/Accessory Stores',
 'Coal Mining',
 'Commercial Banks',
 'Computer Communications Equipment',
 'Computer Manufacturing',
 'Computer Software: Prepackaged Software',
 'Computer Software: Programming, Data Processing',
 'Computer peripheral equipment',
 'Construction/Ag Equipment/Trucks',
 'Consumer Electronics/Appliances',
 'Consumer Electronics/Video Chains',
 'Consumer Specialties',
 'Consumer: Greeting Cards',
 'Containers/Packaging',
 'Department/Specialty Retail Stores',
 'Diversified Commercial Services',
 'Diversified Electronic Products',
 'Diversified Financial Services',
 'EDP Services',
 'Electric Utilities: Central',
 'Electrical Products',
 'Electronic Components',
 'Electronics Distribution',
 'Engineering & Construction',
 'Environmental Services',
 'Farming/Seeds/Milling',
 'Finance Companies',
 'Finance/Investors Services',
 'Finance: Consumer Services',
 'Fluid Controls',
 'Food Chains',
 'Food Distributors',
 'Forest Products',
 'General Bldg Contractors - Nonresidential Bldgs',
 'Home Furnishings',
 'Homebuilding',
 'Hospital/Nursing Management',
 'Hotels/Resorts',
 'Industrial Machinery/Components',
 'Industrial Specialties',
 'Integrated oil Companies',
 'Investment Bankers/Brokers/Service',
 'Investment Managers',
 'Life Insurance',
 'Major Banks',
 'Major Chemicals',
 'Major Pharmaceuticals',
 'Marine Transportation',
 'Meat/Poultry/Fish',
 'Medical Electronics',
 'Medical Specialities',
 'Medical/Dental Instruments',
 'Medical/Nursing Services',
 'Metal Fabrications',
 'Military/Government/Technical',
 'Mining & Quarrying of Nonmetallic Minerals (No Fuels)',
 'Miscellaneous',
 'Miscellaneous manufacturing industries',
 'Motor Vehicles',
 'Movies/Entertainment',
 'Multi-Sector Companies',
 'Natural Gas Distribution',
 'Newspapers/Magazines',
 'Office Equipment/Supplies/Services',
 'Oil & Gas Production',
 'Oil Refining/Marketing',
 'Oil/Gas Transmission',
 'Oilfield Services/Equipment',
 'Ophthalmic Goods',
 'Ordnance And Accessories',
 'Other Consumer Services',
 'Other Pharmaceuticals',
 'Other Specialty Stores',
 'Other Transportation',
 'Package Goods/Cosmetics',
 'Packaged Foods',
 'Paints/Coatings',
 'Paper',
 'Plastic Products',
 'Pollution Control Equipment',
 'Power Generation',
 'Precious Metals',
 'Precision Instruments',
 'Professional Services',
 'Property-Casualty Insurers',
 'Publishing',
 'RETAIL: Building Materials',
 'Radio And Television Broadcasting And Communications Equipment',
 'Railroads',
 'Real Estate',
 'Real Estate Investment Trusts',
 'Recreational Products/Toys',
 'Rental/Leasing Companies',
 'Restaurants',
 'Retail: Computer Software & Peripheral Equipment',
 'Savings Institutions',
 'Semiconductors',
 'Services-Misc. Amusement & Recreation',
 'Shoe Manufacturing',
 'Specialty Chemicals',
 'Specialty Foods',
 'Specialty Insurers',
 'Steel/Iron Ore',
 'Telecommunications Equipment',
 'Television Services',
 'Textiles',
 'Tobacco',
 'Tools/Hardware',
 'Transportation Services',
 'Trucking Freight/Courier Services',
 'Water Supply',
 'Wholesale Distributors',
 'n/a']
