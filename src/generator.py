import csv
from copy import copy

candidates = ['Dariusz Maciej GRABOWSKI', 'Piotr IKONOWICZ', 'Jarosław KALINOWSKI',
              'Janusz KORWIN-MIKKE', 'Marian KRZAKLEWSKI', 'Aleksander KWAŚNIEWSKI',
              'Andrzej LEPPER', 'Jan ŁOPUSZAŃSKI', 'Andrzej Marian OLECHOWSKI',
              'Bogdan PAWŁOWSKI', 'Lech WAŁĘSA', 'Tadeusz Adam WILECKI']

stat_list = ['Obwody', 'Uprawnieni', 'Karty wydane', 'Głosy oddane', 'Głosy nieważne', 'Głosy ważne']


children = {'Polska': []}

basic_statsheet = {}

for stat in stat_list:
    basic_statsheet[stat] = 0

for cand in candidates:
    basic_statsheet[cand] = 0

stats = {'Polska': copy(basic_statsheet)}

with open('../results_csv/pkw2000.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    previous = {'Województwo': '', 'Nr okręgu': '', 'Kod gminy': ''}
    for row in reader:
        new_statsheet = copy(basic_statsheet)
        for k in new_statsheet.keys():
            new_statsheet[k] = int(row[k])
        new_statsheet['Gmina'] = row['Gmina']
        stats[row['Kod gminy']] = new_statsheet

        if (row['Województwo'] != previous['Województwo']):
            stats[row['Województwo']] = copy(basic_statsheet)
            children[row['Województwo']] = []
            children['Polska'].append(row['Województwo'])

        if (row['Nr okręgu'] != previous['Nr okręgu']):
            stats[row['Nr okręgu']] = copy(basic_statsheet)
            children[row['Nr okręgu']] = []
            children[row['Województwo']].append(row['Nr okręgu'])

        children[row['Nr okręgu']].append(row['Kod gminy'])

        previous = copy(row)

def calc_stats(area):
    if(stats[area]['Obwody'] == 0):
        for child in children[area]:
            child_stats = calc_stats(child)
            for k in stats[area].keys():
                stats[area][k] += child_stats[k]
    return stats[area]

calc_stats('Polska')

print(children['Polska'])
print(stats['Polska'])