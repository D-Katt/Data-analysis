# Пример анализа базы данных: итоги ежегодного опроса разработчиков за 2019 год
# (с использованием библиотек pandas и matplotlib и визуализацией данных)
# Источник: https://insights.stackoverflow.com/survey

import pandas as pd
from matplotlib import pyplot as plt
from collections import Counter

survey = pd.read_csv('survey_results_public.csv', usecols=['Respondent', 'Country', 'LanguageWorkedWith',
                     'ConvertedComp', 'EdLevel', 'Employment', 'YearsCodePro', 'OrgSize'])

# Средний доход в зависимости от опыта работы:
survey['YearsCodePro'] = survey['YearsCodePro'].replace({'Less than 1 year': '0.5', 'More than 50 years': '51'})
survey.YearsCodePro = survey.YearsCodePro.apply(pd.to_numeric, errors='coerce')
income_experience = survey[['YearsCodePro', 'ConvertedComp']].groupby('YearsCodePro').mean().round(0)

# Средний доход среди владеющих Python:
income_experience_p = survey[survey.LanguageWorkedWith.str.contains('Python', na=False)]
income_experience_p = income_experience_p[['YearsCodePro', 'ConvertedComp']].groupby('YearsCodePro').mean().round(0)

# Визуализация:
plt.style.use('seaborn-poster')
plt.plot(income_experience_p.index, income_experience_p.ConvertedComp, label='Python Developers')
plt.plot(income_experience.index, income_experience.ConvertedComp, label='All Developers')
plt.title('Average Developer Salaries by Age')
plt.legend()
plt.xlabel('Ages')
plt.ylabel('Annual Salary (USD)')
plt.tight_layout()
plt.show()

# Наиболее популярные языки программирования:
lang_response = survey['LanguageWorkedWith']
lang_response.dropna(inplace=True)

languages = Counter()
for response in lang_response:
    languages.update(response.split(';'))

lang_response = pd.DataFrame.from_dict(languages, orient='index')
lang_response.rename(columns={0: 'Developers_N'}, inplace=True)
lang_response.sort_values(by='Developers_N', ascending=False, inplace=True)
total = survey['LanguageWorkedWith'].count()
lang_response['Percentage'] = round(lang_response.Developers_N / total * 100, 2)

# Визуализация:
plt.barh(lang_response.index, lang_response.Percentage)
plt.title("Usage of Programming Languages (%)")
plt.tight_layout()
plt.show()