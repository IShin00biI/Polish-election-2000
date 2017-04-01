
import csv
from copy import copy

candidates = ['Dariusz Maciej GRABOWSKI', 'Piotr IKONOWICZ', 'Jarosław KALINOWSKI', 'Janusz KORWIN-MIKKE', 'Marian KRZAKLEWSKI', 'Aleksander KWAŚNIEWSKI', 'Andrzej LEPPER', 'Jan ŁOPUSZAŃSKI', 'Andrzej Marian OLECHOWSKI', 'Bogdan PAWŁOWSKI', 'Lech WAŁĘSA', 'Tadeusz Adam WILECKI']

stat_list = ['Obwody', 'Uprawnieni', 'Karty wydane', 'Głosy oddane', 'Głosy nieważne', 'Głosy ważne']

color = {'Dariusz Maciej GRABOWSKI': 'crimson', 'Piotr IKONOWICZ': 'blue', 'Jarosław KALINOWSKI': 'yellow', 'Janusz KORWIN-MIKKE': 'green', 'Marian KRZAKLEWSKI': 'purple', 'Aleksander KWAŚNIEWSKI': 'pink', 'Andrzej LEPPER': 'brown', 'Jan ŁOPUSZAŃSKI': 'darkcyan', 'Andrzej Marian OLECHOWSKI': 'blueviolet', 'Bogdan PAWŁOWSKI': 'greenyellow', 'Lech WAŁĘSA': 'fuchsia', 'Tadeusz Adam WILECKI': 'coral'}

children = {'Polska': []}

basic_statsheet = {}

for stat in stat_list:
    basic_statsheet[stat] = 0

for cand in candidates:
    basic_statsheet[cand] = 0

stats = {'Polska': copy(basic_statsheet)}

type = {'Polska': 'country'}

with open('./results_csv/pkw2000.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    previous = {'Województwo': '', 'Nr okręgu': '', 'Kod gminy': ''}
    for row in reader:
        if(not (row['Kod gminy'] in stats)):
            new_statsheet = copy(basic_statsheet)
            for k in new_statsheet.keys():
                new_statsheet[k] = int(row[k])
            new_statsheet['Gmina'] = row['Gmina']
            stats[row['Kod gminy']] = new_statsheet
            type[row['Kod gminy']] = 'commune'
            children[row['Kod gminy']] = []

            if (row['Województwo'] != previous['Województwo']):
                stats[row['Województwo']] = copy(basic_statsheet)
                children[row['Województwo']] = []
                children['Polska'].append(row['Województwo'])
                type[row['Województwo']] = 'voivodeship'

            if (row['Nr okręgu'] != previous['Nr okręgu']):
                stats[row['Nr okręgu']] = copy(basic_statsheet)
                children[row['Nr okręgu']] = []
                children[row['Województwo']].append(row['Nr okręgu'])
                type[row['Nr okręgu']] = 'district'

            children[row['Nr okręgu']].append(row['Kod gminy'])
        else:
            for k in stats[row['Kod gminy']].keys():
                if(k != 'Gmina'):
                    stats[row['Kod gminy']][k] += int(row[k])

        previous = copy(row)

def calc_stats(area):
    if(stats[area]['Obwody'] == 0):
        for child in children[area]:
            child_stats = calc_stats(child)
            for k in stats[area].keys():
                stats[area][k] += child_stats[k]
    return stats[area]

calc_stats('Polska')

from jinja2 import Environment, PackageLoader
from jinja2 import select_autoescape

env = Environment(
        loader=PackageLoader('src', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )

template = env.get_template('country.html')

with open('./website/index.html', 'w', encoding='UTF-8') as out:
    out.write(template.render(
        stat_list=stat_list,
        candidates=candidates,
        stats=stats,
        color=color,
        area='Polska',
        children=children['Polska']
    ))

for cur_type in ['voivodeship', 'district', 'commune']:
    template = env.get_template(cur_type + '.html')
    for area in stats.keys():
        if(type[area] == cur_type):
            with open('./website/' + cur_type + 's/' + area + '.html', 'w', encoding='UTF-8') as out:
                out.write(template.render(
                    stat_list=stat_list,
                    candidates=candidates,
                    stats=stats,
                    color=color,
                    area=area,
                    children=children[area]
                ))
