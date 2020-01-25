# Пример анализа базы данных: итоги ежегодного опроса разработчиков за 2019 год
# (с использованием библиотек pandas и numpy)
# Источник: https://insights.stackoverflow.com/survey

import numpy as np
import pandas as pd

# Считываем из csv-файла данные, необходимые для анализа:
survey = pd.read_csv('survey_results_public.csv', usecols=['Respondent', 'Country',
                     'ConvertedComp', 'EdLevel', 'Employment', 'YearsCodePro'])

# Общее количество респондентов и количество вопросов

respondents_n, question_n = survey.shape

print("Анализ 'Stack Overflow Developer Survey 2019':\n"
      "\tреспондентов: {}\n\tвопросов: {}".format(respondents_n, question_n))

# Распределение респондентов по странам

# Подсчитываем кол-во по странам и из 20-ки крупнейших создаем новую таблицу:
countries = pd.DataFrame(survey.Country.value_counts().nlargest(20))
countries.columns = ['N_of_Developers']  # Переименовываем столбец
total = survey.Country.count()  # Всего респондентов, указавших страну
# Добавляем столбец с долей от общего числа разработчиков:
countries['Percentage'] = round(countries['N_of_Developers'] / total * 100, 2)
print('\nТоп-20 стран по количеству разработчиков:')
print(countries)

# Уровень дохода

av_income = int(np.mean(survey['ConvertedComp']))  # Среднее значение по столбцу
print('\nСредний уровень дохода, долл. США в год:', av_income)

# Средний доход по странам

# Среднее значение с группировкой по странам:
income_country = survey[['ConvertedComp', 'Country']].groupby('Country').mean().round(0)
income_country.sort_values('ConvertedComp', ascending=False, inplace=True)  # Сортировка по убыванию
print('\nСредний уровень дохода по странам:')
print(income_country.head(20))

# Средний доход в зависимости от уровня образования

income_education = survey[['ConvertedComp', 'EdLevel']].groupby('EdLevel').mean().round(0)
income_education.sort_values('ConvertedComp', ascending=False, inplace=True)
print('\nСредний доход в зависимости от уровня образования:')
print(income_education)

# Средний доход в зависимости от типа занятости

income_employment = survey[['ConvertedComp', 'Employment']].groupby('Employment').mean().round(0)
income_employment.sort_values('ConvertedComp', ascending=False, inplace=True)
print('\nСредний доход в зависимости от типа занятости:')
print(income_employment)

# Средний доход в зависимости от опыта работы

# Заменяем исходные текстовые значения в столбце числовыми:
for i in range(len(survey)):
    if survey.loc[i, 'YearsCodePro'] == 'Less than 1 year':
        survey.loc[i, 'YearsCodePro'] = '0.5'
    elif survey.loc[i, 'YearsCodePro'] == 'More than 50 years':
        survey.loc[i, 'YearsCodePro'] = 51

# Преобразуем данные столбца в числовой формат:
survey.YearsCodePro = survey.YearsCodePro.apply(pd.to_numeric, errors='coerce')

# Преобразуем числовые данные столбца в укрупненные категории:
survey.YearsCodePro = pd.cut(survey.YearsCodePro, bins=[0, 1, 3, 6, 11, 21, 50],
                           labels=['Less than 1 year', '1 to 2 years', '3 to 5 years',
                                   '6 to 10 years', '11 to 20 years', 'Over 20 years'])

# Рассчитываем средние значения по категориям:
income_experience = survey[['YearsCodePro', 'ConvertedComp']].groupby('YearsCodePro').mean().round(0)
print('\nСредний доход в зависимости от опыта работы:')
print(income_experience)
