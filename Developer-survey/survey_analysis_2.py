# Пример анализа базы данных: итоги ежегодного опроса разработчиков за 2019 год
# (с использованием библиотек pandas и numpy)
# Источник: https://insights.stackoverflow.com/survey

import numpy as np
import pandas as pd

# Считываем данные из csv-файла:
survey = pd.read_csv('survey_results_public.csv')

# Общее количество респондентов и количество вопросов

respondents_n, question_n = survey.shape

print("Анализ 'Stack Overflow Developer Survey 2019':\n"
      "\tреспондентов: {}\n\tвопросов: {}".format(respondents_n, question_n))

# Распределение респондентов по странам

countries = survey[['Respondent', 'Country']]  # Выбираем столбцы: порядковый номер и страна
countries_n = countries.groupby('Country').count()  # Кол-во респондентов по странам
countries_total = survey.Country.count()  # Всего респондентов, указавших страну
countries_n['Share'] = round(countries_n['Respondent'] / countries_total * 100, 2)  # Добавляем столбец с долей
countries_n.sort_values('Respondent', ascending=False, inplace=True)  # Сортируем по убыванию

print('\nТоп-20 стран по количеству разработчиков:')
print(countries_n.head(20))  # Выводим первые 20 строк

# Уровень дохода

av_income = int(np.mean(survey['ConvertedComp']))
print('\nСредний уровень дохода, долл. США в год:', av_income)

# Средний доход по странам

income_country = survey[['ConvertedComp', 'Country']].groupby('Country').mean().round(0)  # Среднее значение
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

income_experience = survey[['ConvertedComp', 'YearsCodePro']].groupby('YearsCodePro').mean().round(0)
income_experience.sort_values('ConvertedComp', ascending=False, inplace=True)
print('\nСредний доход в зависимости от опыта работы:')
print(income_experience.head(20))
