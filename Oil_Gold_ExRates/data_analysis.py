import pandas as pd
from matplotlib import pyplot as plt

# Считываем исходные данные из 4 файлов:
dollar = pd.read_excel('USD_Rub.xlsx')
euro = pd.read_excel('Euro_Rub.xlsx')
brent = pd.read_csv('Brent_USD.csv')
gold = pd.read_csv('Gold_Rub.csv')

# Преобразуем дату в формат datetime, где это необходимо:
gold['Date'] = pd.to_datetime(gold['Date'], format='%Y%m%d')
brent['Date'] = pd.to_datetime(brent['Date'], format='%Y%m%d')

# Переименовываем столбцы для последующего объединения данных в одну таблицу:
dollar = dollar.rename({'nominal': 'Dollar_nominal', 'data': 'Date',
                        'curs': 'Dollar_rate', 'cdx': 'Dollar_cdx'}, axis='columns')
euro = euro.rename({'nominal': 'Euror_nominal', 'data': 'Date',
                    'curs': 'Euro_rate', 'cdx': 'Euro_cdx'}, axis='columns')
gold = gold.rename({'Price': 'Gold_price'}, axis='columns')
brent = brent.rename({'Ticker': 'Brent_Ticker', 'PER': 'Brent_per', 'Time': 'Brent_time',
                      'Open': 'Brent_open', 'High': 'Brent_high', 'Low': 'Brent_low',
                      'Close': 'Brent_close', 'Vol': 'Brent_vol'}, axis='columns')

# Объединяем исходные данные в две базы, соотнося их по дате:
data_cur = pd.merge(dollar, euro, on='Date')
data_cur = pd.merge(data_cur, brent, on='Date')  # База 1 - курсы валют и цены на нефть.

data_gold = pd.merge(data_cur, gold, on='Date')  # База 2 - с включением цен на золото
# (динамика цен на золото доступна с 2008 г., поэтому все предшествующие периоды в ней отсутствуют).

# Сортируем данные по значениям в столбце 'Date':
data_cur.sort_values(by='Date')
data_gold.sort_values(by='Date')

# Вычисляем коэффициенты корреляции:

print('Коэффициент корреляции (курс доллара / цена на нефть):\n\tза весь период:',
      round(data_cur['Brent_close'].corr(data_cur.Dollar_rate), 3))

data_08_14 = data_cur[data_cur.Date.dt.year < 2008]
print('\tдо 2007 г.:',
      round(data_08_14['Brent_close'].corr(data_08_14.Dollar_rate), 3))

data_08_14 = data_cur[(data_cur.Date.dt.year > 2007) & (data_cur.Date.dt.year < 2018)]
print('\tв 2008-2017 гг.:',
      round(data_08_14['Brent_close'].corr(data_08_14.Dollar_rate), 3))

data_15 = data_cur[data_cur.Date.dt.year > 2017]
print('\tс 2018 г.:',
      round(data_15['Brent_close'].corr(data_15.Dollar_rate), 3))

print('\nКоэффициент корреляции (курс доллара / цена на золото):',
      round(data_gold['Gold_price'].corr(data_gold.Dollar_rate), 3))

print('\nКоэффициент корреляции (курс евро / цена на золото):',
      round(data_gold['Gold_price'].corr(data_gold.Euro_rate), 3))

# Визуализация динамики курсов валют и цен на нефть (два графика в одном окне):

fig1, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)

ax1.plot(data_cur.Date.tolist(), data_cur.Brent_close.tolist(), label='Brent Price (USD)')
ax1.plot(data_cur.Date.tolist(), data_cur.Dollar_rate.tolist(), label='Dollar Rate (Rub)')

ax2.plot(data_cur.Date.tolist(), data_cur.Brent_close.tolist(), label='Brent Price (USD)')
ax2.plot(data_cur.Date.tolist(), data_cur.Euro_rate.tolist(), label='Euro Rate (Rub)')

ax1.legend()
ax2.legend()
ax1.set_title('Brent Price and Exchange Rates')
fig1.tight_layout()

# Визуализация динамики курсов валют и цен на золото (график с двумя осями y):

fig2, ax3 = plt.subplots()
ax_double_x = ax3.twinx()

ax3.plot(data_gold.Date.tolist(), data_gold.Dollar_rate.tolist(), color='g', label='Dollar Rate')
ax3.plot(data_gold.Date.tolist(), data_gold.Euro_rate.tolist(), color='b', label='Euro Rate')
ax3.set_ylabel('Exchange Rate (RUR)')

ax_double_x.plot(data_gold.Date.tolist(), data_gold.Gold_price.tolist(), color='r', label='Gold Price')
ax_double_x.set_ylabel('Gold Price (RUR)')

ax3.legend(loc='upper left')
ax_double_x.legend(loc='lower right')
ax3.set_title('Exchange Rates and Gold Price')

fig2.tight_layout()

plt.show()

# Сохраняем полученные графики в файлы .png:
fig1.savefig('Brent_Ex_Rates.png')
fig2.savefig('Gold_Ex_Rates.png')
