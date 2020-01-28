# Пример анализа базы данных: итоги ежегодного опроса разработчиков за 2019 год
# (с использованием модуля csv и словарей)
# Источник: https://insights.stackoverflow.com/survey

import csv
from collections import Counter

# Считываем данные из csv-файла:
with open('survey_results_public.csv', 'r', encoding='utf-8') as f:
    survey = csv.DictReader(f)

    # Общее число респондентов:
    total = 0

    # Словари для подсчета количества респондентов:
    countries = Counter()
    employment = Counter()
    job = Counter()
    languages = Counter()

    for line in survey:

        # Подсчитываем респондентов по странам:
        countries[line['Country']] += 1
        total += 1

        # Подсчитываем респондентов по типу занятости:
        employment[line['Employment']] += 1

        # Подсчитываем выполняемые респондентами функции:
        job.update(line['DevType'].split(';'))

        # Подсчитываем используемые языки программирования:
        languages.update(line['LanguageWorkedWith'].split(';'))

print("Анализ 'Stack Overflow Developer Survey 2019':")
print('\tколичество респондентов: {}'.format(total))

# Обрабатываем данные, в которых не указана страна проживания:
if 'NA' in countries:
    total_in_countries = total - countries['NA']
    countries.pop('NA')
else:
    total_in_countries = total

# Распределение разработчиков по странам:

print('\nТоп-20 стран по количеству разработчиков:')
c = countries.most_common(20)
rank = 1
for line in c:
    print(f'\t{rank}. {line[0]}: {line[1]} ({round(line[1] / total_in_countries * 100, 2)}%)')
    rank += 1

# Обрабатываем данные, в которых не указан тип занятости:
if 'NA' in employment:
    total_by_empl = total - employment['NA']
    employment.pop('NA')
else:
    total_by_empl = total

# Распределение разработчиков по типам занятости:

print('\nСтруктура респондентов по типам занятости:')
for types in employment:
    print(f'\t{types}: {employment[types]} ({round(employment[types] / total_by_empl * 100, 2)}%)')

# Обрабатываем данные, в которых не указаны выполняемые функции:
if 'NA' in job:
    total_by_job = total - job['NA']
    job.pop('NA')
else:
    total_by_job = total

# Наиболее часто выполняемые функции:

print('\nНаиболее часто выполняемые функции\n(респонденты могли указать несколько вариантов):')
j = job.most_common(20)
rank = 1
for line in j:
    print(f'\t{rank}. {line[0]}: {line[1]} ({round(line[1] / total_by_job * 100, 2)}%)')
    rank += 1

# Обрабатываем данные, в которых не указан язык программирования:
if 'NA' in languages:
    total_by_lang = total - languages['NA']
    languages.pop('NA')
else:
    total_by_lang = total

# Наиболее часто используемые языки программирования:

print('\nНаиболее часто используемые языки программирования\n(респонденты могли указать несколько вариантов):')
l = languages.most_common(20)
rank = 1
for line in l:
    print(f'\t{rank}. {line[0]}: {line[1]} ({round(line[1] / total_by_lang * 100, 2)}%)')
    rank += 1
