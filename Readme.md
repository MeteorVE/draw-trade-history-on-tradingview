# Draw your trade on Tradingview

## Introduction

This script can help you to convert your trading history data from Excel to pine script.



## Usage

1. Git clone this repo or download zip from github
2. Put your Excel in the same folder of ``.py`` file 
	- [Note A]
3. ``python convert.py --m BTCUSDT``
   - [Note B]
4. You will get a ``output_pine_script.txt``，copy the context in that.
5. Create a new script in Tradingview, paste the context and click ``add to chart``.
  ![](https://i.imgur.com/LeaDLQY.png)
6. Result like this. 
  - [Note C]
  ![](https://i.imgur.com/qBMle4S.png)

## Note

Note A : 

1. The column fileds are fixed. Below picture is an example.
	(It's default by Binance.)
	
	![](https://i.imgur.com/5kn5yGa.png)
	
	- ``Date(UTC)``	``Market``	``Type``	``Price``	``Amount``	``Total``
	
2. If your excel is exported from Binance, you need to open it, maybe random double click some filed and just **SAVE**。
    I don't know why openpyxl Lib can't read the excel downloaded from Binance System.
    
3. If you export your file from other system, you can modfiy this script to match column name.
    example: you want to replace ``Amount`` to ``Share``, open IDE and replace all ``Amount`` keyword to ``Share``.
    
    - **Notice** : My script doesn't use **Amount** this field. I use **Total** to indicate how many I bought.
      You can modify it in the code.
      (Replace ``row['Total']`` to ``row['Amount']`` or others filed name.)
      
    - I create a Dictionary mapping variable, you can modify this : 
      
      ```python
      # 'key': 'THE_WORD_IN_YOUR_EXCEL'
      columns_name = {
      	'date': 'Date(UTC)', 
      	'price': 'Price',
      	'total': 'Total', 
      	'amount': 'Amount', # You can change 'Amount' to 'Share'.
      	'market': 'Market',
      	'type': 'Type'
      }
      ```
      
      



Note B : 

1. You can indicate trading variety (investment) by argument ``-m VARIETY``
  e.g. : ``python convert.py --m BTCUSDT``, ``python convert.py --m AAPL``
  (it will filter "BTCUSD" transcations from Excel table)
2. If you want to filter your trading investment **in advance**, you can modify this line: 
   ``df = df[df[columns_name['market']].isin([market])]``



Note C :

1. The label's  **Y-AXIS location** is attach **BELOW** or **ABOVE** of the candlestick.
   **Not** at the **Price** of the transcation because of the overlaping problem.
   If you want to change it to the price location, replace ``yloc.abovebar``  and ``yloc.belowbar``  to ``yloc.price`` .

2. There are some style can be adjust with parameter such as ``size=size.large``, ``color=color.new(color.red)``, if you are interesting, you can read docs of pine script v4.
3. To avoid two transcations' trading time are too close, the label is displayed on the left and right by crossing (count of trades modulo 2, so it will be left, right, left, right ... )



## Some useful Information

- Some DataFrame usage

  ```python
  # Get the the (x,y) data : (0, 'price')
  get_row0_price = df.at[0, "Price"]
  
  # Filter the rows in "Market" Column if "BTCUSDT" in.
  # = SELECT * FROM df WHERE Market LIKE 'BTCUSDT';
  filter_market = df[df["Market"].isin(["BTCUSDT"])]
  
  # = SELECT * FROM df WHERE Price >= 35000;
  filter_price = df[df["Price"] > 35000]
  
  # print the columns name of df
  df.columns
  ```

- Pine Script ``label.new`` example

  ```
  // pine script example
  
  mytime = "2021-06-29 8:05:36"
  val = 2115
  label.new(timestamp(mytime), val, text="Sell "+tostring(val)+"\n-200" ,xloc=xloc.bar_time, yloc=yloc.price ,size=size.large, style=label.style_label_up, color=color.new(color.yellow, 90), textcolor=color.gray)
  ```

  - ``color=color.new(color.yellow, 90)`` : 90 is the transparency.
  - ``xloc`` : the label location, x-axis
  - ``yloc`` : the label location, y-axis, option: ``yloc.belowbar``, ``yloc.abovebar``, ``yloc.price``
  - ``size=size.large`` : the size of the label, ``large``, ``normal``, ``small``, ``tiny``, ``auto``, or others.

