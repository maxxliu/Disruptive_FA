# Questions and get question function for risk survey app

import numpy as np 

QUESTIONS = {
	0: ("If you pay $100 to enter a lottery, you have a 20 percent chance of winning $500 and a 80 percent chance of making $0. Would you enter the lottery?", 1),
	1: ("You are trying to ask your significant other to prom. Would you sing to him/her in a crowded area if it gave you a 75 percent chance of success versus a 50 percent chance of success if asking regularly?", 1),
	2: ("If you were given $5000, would you invest it in a stock that has a 50 percent chance of doubling your money or a 50 percent chance of losing all your money?", 1),
	3: ("If you were given $5000, would you invest it in a stock that has a 75 percent of doubling your money but a 25 percent of losing all your money?", 1),
	4: ("Would you cheating on an exam to get an A? You have a 90 percent chance of not getting caught and a 10 percent chance of not getting caught and receiving a 0. You will get a C if you do not cheat.", 1),
	5: ("If your favorite biologically related person (e.g. parent, grandparent, aunty, uncle, brother, sister, cousin) gave you all their money to invest, would you invest in a stock that had a 60 percent chance of doubling money and a 40 percent chance of losing half the money?", 1),
	6: ("Would you be happy with a 5 percent annual portfolio growth rate?", 1),
	7: ("You associate the word “risk” with opportunity or thrill.", 1),
	8: ("Your friends would describe you as a gambler.", 1),
	9: ("Fifty-fifty is good enough odds for a bet.", 1),
	10: ("You think start ups are a good choice for investments.", 1),
	11: ("You consider IPOs a good opporunity to invest.", 1),
	12: ("You don’t understand the business environment of a small foreign country, but you think that it is a good idea to invest since it is an emerging market.", 1),
	13: ("You think assessing risk is the most important part of any investment decision.", -1),
	14: ("You do not find extreme sports appealing to you.", -1),
	15: ("You consider yourself a traditional investor.", -1),
	16: ("You prefer an investment portfolio that has a larger proportion of treasury bonds.", -1),
	17: ("You are relatively reluctant to invest in the stock market.", -1),
	18: ("When budgeting, you prioritize your savings.", -1),
	19: ("If the traffic light is yellow, you stop regardless if you are late.", -1),
	20: ("Do you think an art major is a financially stable career?", 1),
	21: ("Having a stable job is better than investing all your money on a risky but promising startup.", 1),
	22: ("Would you take a vacation knowing you have 20 percent chance of being fired?", 1),
	23: ("Would you accept $1,000,000 for a 1 percent chance a family relative of yours dies?", 1),
	24: ("Do you not speak up in class or discussion because you fear being wrong?", -1),
	25: ("Would you take a penalty kick in the world cup backwards with a 1 percent chance of scoring over taking a regular penalty kick with a 0 percent chance of scoring?", 1),
	26: ("Would you take a class that will teach you everything you need to know at the cost of having a 1.0 GPA?", 1),
	27: ("Riskier but higher returns are better than safe low returns.", 1),
	28: ("Would you risk all your money if you had a 90 percent chance of doubling it?", 1),
	29: ("You would choose life saving surgery with a low chance of survival to cure a terminal disease leaving you with a year to live.", 1)}

def get_questions():
	'''
	Gets a list of 5 questions randomly chosen from the QUESTIONS list

	Inputs:
		none, just the global QUESTIONS list

	Returns:
		fin: list of 5 tuples of question and positive or negative risk score
	'''
	question_list = []
	for item in np.random.choice(range(30), 5, replace=False):
		question_list.append(QUESTIONS[item])

	fin = []
	for i, val in enumerate(question_list):
		fin.append(('Question ' + str(i), val[0], val[1]))

	return fin
