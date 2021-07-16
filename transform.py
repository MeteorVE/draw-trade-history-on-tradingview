import pandas as pd
import sys, getopt

def main(argv):

	columns_name = {
		'date': 'Date(UTC)',
		'price': 'Price',
		'total': 'Total',
		'amount': 'Amount',
		'market': 'Market',
		'type': 'Type'
	}
	market = ''

	opts,args = getopt.getopt(sys.argv[1:],'-h-m:',['help','market'])
	print(opts)
	for opt_name,opt_value in opts:
		if opt_name in ('-m','--market'):
			market = opt_value


	df = pd.read_excel("example.xlsx",engine='openpyxl')
	print(df.columns)

	# Date(UTC)	Market	Type	Price	Amount	Total

	f = open("output_pine_script.txt", "w", encoding="utf-8")
	f.write("""// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
	// © MeteorV

	//@version=4
	study("Draw my trade", overlay=true)
	""")

	sell_cnt = 0
	buy_cnt = 0
	df = df[df[columns_name['market']].isin([market])]
	style = ["style_label_left", "style_label_right"]
	label_size = "normal"

	for index, row in df.iterrows():
		print(row[columns_name['date']], row[columns_name['market']], row[columns_name['type']], row[columns_name['price']], row[columns_name['amount']])
		if(row[columns_name['type']] == 'SELL'):
			f.write("label.new(timestamp('"+row[columns_name['date']]+"'), "+ str(int(row[columns_name['price']]+0.5))+ ", text='Sell "+str(int(row[columns_name['total']]+0.5))+ r"\nat "+ str(int(row[columns_name['price']])) + "', xloc=xloc.bar_time, yloc=yloc.abovebar ,size=size."+ label_size +", style=label."+ style[sell_cnt%2] +", color=color.new(color.red, 90), textcolor=color.white)"+'\n')
			sell_cnt+=1
		else:
			f.write("label.new(timestamp('"+row[columns_name['date']]+"'), "+ str(int(row[columns_name['price']]+0.5))+ ", text='Buy "+str(int(row[columns_name['total']]+0.5))+ r"\nat "+ str(int(row[columns_name['price']]))  + "', xloc=xloc.bar_time, yloc=yloc.belowbar ,size=size."+ label_size +", style=label."+ style[buy_cnt%2] +", color=color.new(color.green, 90), textcolor=color.white)"+'\n')
			buy_cnt+=1
	f.close()

if __name__ == "__main__":
   main(sys.argv[1:])