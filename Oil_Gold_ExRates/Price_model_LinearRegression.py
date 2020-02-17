# Модель прогнозирует курс доллара на основе динамики стоимости золота.
# Линейная зависимость двух переменных.

import pandas as pd
from pandas.plotting import register_matplotlib_converters
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn import metrics

import matplotlib.pyplot as plt

# Считываем исходные данные:
dollar = pd.read_excel('USD_Rub.xlsx', usecols=['data', 'curs'])
dollar = dollar.rename(columns={'data':'Date'})

gold = pd.read_csv('Gold_Rub.csv')
gold['Date'] = pd.to_datetime(gold['Date'], format='%Y%m%d')

# Объединяем данные, соотнося их по дате:
data = pd.merge(dollar, gold, on='Date')

print('Корреляция между курсом доллара и стоимостью золота:', data['curs'].corr(data['Price']))

# Делим данные на учебные и тестовые, включая в тестовые данные
# динамику цен за последний месяц в выборке:
train = data[data['Date'] < pd.to_datetime('2020-01-01')]
test = data.drop(train.index)

# Определяем значения X и y для учебных и тестовых данных:
X_train = np.array(train['Price']).reshape(-1, 1)
y_train = np.array(train['curs'])

X_test = np.array(test['Price']).reshape(-1, 1)
y_test = np.array(test['curs'])

# Создаем модель, обучаем и делаем прогноз:
lr = LinearRegression().fit(X_train, y_train)
y_pred = lr.predict(X_test)

register_matplotlib_converters()

# Выводим график прогнозируемых и фактических значений:
plt.plot(test['Date'].tolist(), y_test.tolist(), label='Фактический')
plt.plot(test['Date'].tolist(), y_pred.tolist(), label='Прогнозируемый')
plt.legend()
plt.title('Курс доллара, руб.')
plt.show()

# Видим, что прогнозируемые значения с высокой степенью корреляции
# соотносятся с фактическими данными, но отличаются от них примерно на 10 рублей.

av_err = metrics.mean_absolute_error(y_test, y_pred)
print(f'\nСредняя абсолютная ошибка (MAE): {av_err}')

# Выводим парами фактические данные и прогноз
# с поправкой на стабильно наблюдаемое отклонение:
print('\nСкорректированный прогноз с поправкой на MAE:')
for i in range(len(y_pred)):
    print(f'Прогноз: {y_pred[i] - av_err} Факт: {y_test[i]} Разница: {(y_pred[i] - av_err) / y_test[i] - 1}')
