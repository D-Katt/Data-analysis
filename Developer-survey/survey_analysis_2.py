# Пример анализа базы данных: итоги ежегодного опроса разработчиков за 2019 год
# (с использованием библиотек pandas и numpy)
# Источник: https://insights.stackoverflow.com/survey

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Считываем из csv-файла данные, необходимые для анализа:
survey = pd.read_csv('survey_results_public.csv', usecols=['Respondent', 'Country',
                     'ConvertedComp', 'EdLevel', 'Employment', 'YearsCodePro', 'OrgSize'])

# Общее количество респондентов и количество вопросов
respondent_n, question_n = survey.shape
print("Анализ 'Stack Overflow Developer Survey 2019':\n"
      "\tреспондентов: {}\n\tвопросов: {}".format(respondent_n, question_n))

# Распределение респондентов по странам
countries = survey.Country.value_counts(normalize=True)
print('\nТоп-20 стран по количеству разработчиков (%):')
print(countries.nlargest(20))

y = countries.nlargest(10).index
x = countries.nlargest(10).tolist()

plt.style.use('fivethirtyeight')
plt.barh(y, x)
plt.title("Developers by Country (%)")
plt.tight_layout()
plt.show()

# Уровень дохода
print('\nСредний уровень дохода, долл. США в год:', int(np.mean(survey['ConvertedComp'])))

# Средний доход по странам:
income_country = survey[['ConvertedComp', 'Country']].groupby('Country').mean().round(0).\
    sort_values('ConvertedComp', ascending=False)
print('\nСредний уровень дохода по странам:')
print(income_country.head(20))

y = income_country.head(10).index
x = income_country.head(10).ConvertedComp.tolist()

plt.barh(y, x)
plt.title("Average income by Country (USD)")
plt.tight_layout()
plt.show()

# Средний доход в зависимости от уровня образования:
income_education = survey[['ConvertedComp', 'EdLevel']].groupby('EdLevel').mean().round(0).\
    sort_values('ConvertedComp', ascending=False)
print('\nСредний доход в зависимости от уровня образования:')
print(income_education)

# Средний доход в зависимости от типа занятости:
income_employment = survey[['ConvertedComp', 'Employment']].groupby('Employment').mean().round(0).\
    sort_values('ConvertedComp', ascending=False)
print('\nСредний доход в зависимости от типа занятости:')
print(income_employment)

# Средний доход в зависимости от опыта работы

# Заменяем исходные описательные выражения в столбце числовыми:
survey['YearsCodePro'] = survey['YearsCodePro'].replace({'Less than 1 year': '0.5', 'More than 50 years': '51'})

# Преобразуем данные столбца в числовой формат:
survey.YearsCodePro = survey.YearsCodePro.apply(pd.to_numeric, errors='coerce')

# Преобразуем числовые данные столбца в укрупненные категории и сохраняем в новый столбец:
survey['Years_group'] = survey['YearsCodePro']
survey.Years_group = pd.cut(survey.YearsCodePro, bins=[0, 1, 3, 6, 11, 21, 50],
                           labels=['Less than 1 year', '1 to 2 years', '3 to 5 years',
                                   '6 to 10 years', '11 to 20 years', 'Over 20 years'])

# Рассчитываем средние значения по категориям:
income_experience = survey[['Years_group', 'ConvertedComp']].groupby('Years_group').mean().round(0)
print('\nСредний доход в зависимости от опыта работы:')
print(income_experience)

print('\nКоэффициент корреляции (доход / опыт работы) по всей выборке:',
      round(survey['ConvertedComp'].corr(survey.YearsCodePro), 3))

# Средний доход в зависимости от размера компании:

income_company = survey[['ConvertedComp', 'OrgSize']].groupby('OrgSize').mean().round(0).\
    sort_values('ConvertedComp', ascending=False)
print('\nСредний уровень дохода в зависимости от размера компании:')
print(income_company)

# Анализ российского сегмента

income_Russia = survey[survey.Country == 'Russian Federation']
print('\nСредний уровень дохода в России, долл. США в год:', int(income_Russia.ConvertedComp.mean()))

education_Russia = income_Russia[['ConvertedComp', 'EdLevel']].groupby('EdLevel').mean().round(0).\
    sort_values('ConvertedComp', ascending=False)
print('\nСредний доход в России в зависимости от уровня образования:')
print(education_Russia)

experience_Russia = income_Russia[['Years_group', 'ConvertedComp']].groupby('Years_group').mean().round(0)
print('\nСредний доход в России в зависимости от опыта работы:')
print(experience_Russia)

print('\nКоэффициент корреляции (доход / опыт работы) по России:',
      round(income_Russia['ConvertedComp'].corr(income_Russia.YearsCodePro), 3))

print('\tв том числе для занятых full-time:',
      round(income_Russia[income_Russia.Employment == 'Employed full-time']
            ['ConvertedComp'].corr(income_Russia.YearsCodePro), 3))

print('\t\tв том числе с опытом работы более 5 лет:',
      round(income_Russia[(income_Russia.Employment == 'Employed full-time')
            & (income_Russia.YearsCodePro >= 5)]
            ['ConvertedComp'].corr(income_Russia.YearsCodePro), 3))

print('\nСредний доход в России в зависимости от уровня образования и опыта работы:')
with pd.option_context('display.precision', 0, 'display.max_columns', 7):
    print(pd.DataFrame(income_Russia.pivot_table(index='EdLevel', columns='Years_group',
                              values='ConvertedComp', aggfunc='mean', margins=True)))

company_Russia = income_Russia[['ConvertedComp', 'OrgSize']].groupby('OrgSize').mean().round(0).\
    sort_values('ConvertedComp', ascending=False)
print('\nСредний доход в России в зависимости от размера компании:')
print(company_Russia)
