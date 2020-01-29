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

plt.style.use('fivethirtyeight')

fig1, ax1 = plt.subplots()

ax1.plot(income_experience_p.index, income_experience_p.ConvertedComp, label='Python Developers')
ax1.plot(income_experience.index, income_experience.ConvertedComp, label='All Developers')
ax1.set_title('Average Income by Coding Experience')
ax1.legend()
ax1.set_xlabel('Years')
ax1.set_ylabel('Annual Income (USD)')

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

fig2, ax2 = plt.subplots()
rows = ax2.barh(lang_response.head(10).index, lang_response.head(10).Percentage)
ax2.set_title("Usage of Programming Languages (%)")


def bar_labels(ax, rows):
    """Attach a text label to each row in 'rows', displaying its value."""
    for row in rows:
        width = row.get_width()
        ax.annotate('{}%'.format(width),
                    xy=(width, row.get_y()),
                    xytext=(0, 10),
                    textcoords="offset points",
                    ha='right', va='center')


bar_labels(ax2, rows)

fig1.tight_layout()
fig2.tight_layout()
plt.show()
