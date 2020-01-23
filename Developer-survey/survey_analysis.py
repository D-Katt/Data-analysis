# Пример анализа базы данных: итоги ежегодного опроса разработчиков за 2019 год
# Источник: https://insights.stackoverflow.com/survey

import numpy as np
import pandas as pd
import itertools

# Считываем данные из двух csv-файлов:
survey = pd.read_csv('survey_results_public.csv')  # Итоги опроса (основная база данных)
questions = pd.read_csv('survey_results_schema.csv')  # Расшифровка столбцов (список вопросов)

# Общее количество респондентов и количество вопросов

respondents_n, question_n = survey.shape

print("Анализ 'Stack Overflow Developer Survey 2019':\n"
      "\tреспондентов: {}\n\tвопросов: {}".format(respondents_n, question_n))

# Распределение респондентов по странам

# Создаем новую базу с двумя столбцами: порядковый номер и страна.
countries = pd.DataFrame(zip(itertools.count(1), survey['Country']), columns=['N', 'Country'])

countries_n = countries.groupby('Country').count()  # Кол-во респондентов по странам
countries_total = survey.Country.count()  # Всего респондентов, указавших страну
countries_n['Share'] = round(countries_n['N'] / countries_total, 2)  # Добавляем столбец с долей
countries_n.sort_values('N', ascending=False, inplace=True)  # Сортируем по убыванию

print('\nТоп-20 стран по количеству разработчиков:')
print(countries_n.head(20))  # Выводим первые 10 строк

# Корреляция уровня дохода с другими параметрами

av_income = int(np.mean(survey['ConvertedComp']))
print('\nСредний уровень дохода, долл. США в год:', av_income)

# Выбираем из базы параметры для сопоставления:
income_country = survey[['ConvertedComp', 'Country', 'EdLevel', 'YearsCodePro', 'Employment']]

# Убираем строки, в которых не указан доход
income_country = income_country[income_country.ConvertedComp > 0]

# Создаем копии:
income_education = income_country.copy()
income_experience = income_country.copy()
income_employment = income_country.copy()

# Убираем строки, в которых не указана страна:
income_country = income_country[income_country.Country != 'NaN']

# Убираем строки, в которых не указано образование:
income_education = income_education[income_education.EdLevel != 'NaN']

# Убираем строки, в которых опыт работы указан не числом:
income_experience = income_experience[income_experience.YearsCodePro != 'NaN']

# income_experience = income_experience[lambda x: 0.5 if x.YearsCodePro == 'Less than 1 year']

# Убираем строки, в которых не указана занятость:
income_employment = income_employment[income_employment.Employment != 'NaN']

# Группируем массив по странам и вычисляем средний уровень дохода:
income_country = income_country[['ConvertedComp', 'Country']].groupby('Country').mean()
# Сортируем по убыванию значений:
income_country.sort_values('ConvertedComp', ascending=False, inplace=True)
print('\nСредний уровень дохода по странам:\n', income_country)

# Группируем массив по уровню образования и вычисляем средний уровень дохода:
income_education = income_education[['ConvertedComp', 'EdLevel']].groupby('EdLevel').mean()
# Сортируем по убыванию значений:
income_education.sort_values('ConvertedComp', ascending=False, inplace=True)
print('\nСредний уровень дохода в зависимоси от образования:\n', income_education)

# Группируем массив по опыту работу и вычисляем средний уровень дохода:
income_experience = income_experience[['ConvertedComp', 'YearsCodePro']].groupby('YearsCodePro').mean()
# Сортируем по убыванию значений:
income_experience.sort_values('ConvertedComp', ascending=False, inplace=True)
print('\nСредний уровень дохода в зависимоси от опыта работы:\n', income_experience)

# Группируем массив по видам занятости и вычисляем средний уровень дохода:
income_employment = income_employment[['ConvertedComp', 'Employment']].groupby('Employment').mean()
# Сортируем по убыванию значений:
income_experience.sort_values('ConvertedComp', ascending=False, inplace=True)
print('\nСредний уровень дохода в зависимоси от вида занятости:\n', income_employment)
