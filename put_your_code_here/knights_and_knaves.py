import re
from collections import defaultdict

file_input = input('Which text file do you want to use for the puzzle? ')
dict_name_quote = defaultdict(list)
Sir_or_sirs = set()
list_solution = []
truth_table = []
dict_data = {}
l_s = []

with open(file_input) as file:
    contents = file.read()

no_space = ''
i = 0
while i < len(contents):
    if contents[i] == '\n':
        no_space += ' '
    else:
        no_space += contents[i]
    i += 1

def Sir_sirs(names):
    Sir_or_sirs.update(names)
Sentences = re.findall('\"*[A-Za-z,\": ]*[.?!]\"{0,1}', no_space)
index = 0
while index < len(Sentences):
    sentence = Sentences[index]
    if 'Sir ' in sentence:
        name = re.findall('Sir\\s([A-Z][a-z]+)', sentence)
        Sir_sirs(name)
    if 'Sirs ' in sentence:
        names = re.split('Sirs ', sentence)[1]
        list_of_names = re.findall('[A-Z][a-z]+', names)
        Sir_sirs(list_of_names)
    index += 1

for name in ['Knight', 'Knights', 'Knaves', 'Knave']:
    Sir_or_sirs.discard(name)
Sir_or_sirs = sorted(set(Sir_or_sirs))
if len(Sir_or_sirs) == 1:
    print('The Sir is:',Sir_or_sirs )
else:
    print('The Sirs are:', ' '.join(Sir_or_sirs))

for sentence in Sentences:
    if '"' in sentence:
        quote = re.findall('"([^"]*)"', sentence)
        new_sentence = sentence.replace(quote[0], '')
        name = re.findall('Sir\\s([A-Z][a-z]+)', new_sentence)
        dict_name_quote[name[0]] += quote
def add_list(list_name, val, binary):
    return_list = [list_name]
    return_list.extend([val, binary])
    return return_list

list_names = list(sorted(Sir_or_sirs))
for n in list_names:
    l_s.append(list_names.index(n))

Knave = 0
Knight = 1
for name, statements in dict_name_quote.items():
    list_val = []
    for quote in statements:
        list_person = []
        if 'I ' in quote:
            n_statement = quote.replace('I ', 'Sir ' + name + ' ')
            names = re.findall('Sir\\s([A-Z][a-z]+)', n_statement)
            for n in names:
                list_person.append(list_names.index(n))
            if ' least ' in n_statement:
                for character_type, character in [('Knight', Knight), ('Knave', Knave)]:
                    if character_type in n_statement:
                        target_list = l_s if ' us ' in n_statement else list_person
                        list_val.append(add_list(target_list, 'least', character))

            elif ' most ' in n_statement:
                for character_type in ['Knight', 'Knave']:
                    if character_type in n_statement:
                        target_list = l_s if ' us ' in n_statement else list_person
                        list_val.append(add_list(target_list, 'most', character_type))

            elif 'Exactly ' in n_statement or 'exactly' in n_statement:
                key_word = 'exactly'
                character_mappings = [('Knight', Knight), ('Knave', Knave)]
                for character_type, character in character_mappings:
                    if character_type in n_statement:
                        target_list = l_s if ' us ' in n_statement else list_person
                        list_val.append(add_list(target_list, key_word, character))

            elif ' or ' in n_statement:
                if 'Knight' in n_statement:
                    list_val.append(add_list(list_person, 'least', Knight))
                if 'Knave' in n_statement:
                    list_val.append(add_list(list_person, 'least', Knave))

            elif ' or ' in n_statement:
                if 'Knight' in n_statement:
                    list_val += [add_list(list_person, 'least', Knight)]
                if 'Knave' in n_statement:
                    list_val += [add_list(list_person, 'least', Knave)]

            elif ' is ' in n_statement or ' am ' in n_statement or ' are ' in n_statement:
                if 'Knight' in n_statement:
                    list_val.append(add_list(list_person, 'am', Knight))
                if 'Knave' in n_statement:
                    list_val.append(add_list(list_person, 'am', Knave))
        else:
            names = re.findall('Sir\\s([A-Z][a-z]+)', quote)
            for n in names:
                list_person.append(list_names.index(n))

            if ' least ' in quote:
                for character_type, character in [('Knight', Knight), ('Knave', Knave)]:
                    if character_type in quote:
                        target_list = l_s if ' us ' in quote else list_person
                        list_val.append(add_list(target_list, 'least', character))

            elif ' most ' in quote:
                for character_type, character in [('Knight', Knight), ('Knave', Knave)]:
                    if character_type in quote:
                        target_list = l_s if ' us ' in quote else list_person
                        list_val.append(add_list(target_list, 'most', character))
            elif 'Exactly' in quote or 'exactly ' in quote:
                for role in [Knight, Knave]:
                    target_list = l_s if ' us ' in quote else list_person
                    list_val.append(add_list(target_list, 'exactly', role) if role in quote else None)
                list_val = [item for item in list_val if item is not None]

            elif 'All ' in quote or 'all ' in quote:
                if 'Knight' in quote:
                    list_val.append(add_list(l_s, 'am', Knight))
                if 'Knave' in quote:
                    list_val.append(add_list(l_s, 'am', Knave))

            elif ' or ' in quote:
                if 'Knight' in quote:
                    list_val.append(add_list(list_person, 'least', Knight))
                if 'Knave' in quote:
                    list_val.append(add_list(list_person, 'least', Knave))

            elif ' is ' in quote or ' am ' in quote or ' are ' in quote:
                if 'Knight' in quote:
                    list_val.append(add_list(list_person, 'am', Knight))
                if 'Knave' in quote:
                    list_val.append(add_list(list_person, 'am', Knave))

    dict_data[list_names.index(name)] = list_val

truth_table = [tuple(int(x) for x in f'{i:0{len(Sir_or_sirs)}b}') for i in range(2 ** len(Sir_or_sirs))]
list_solution = [{name: val for name, val in zip(sorted(Sir_or_sirs), row)} for row in truth_table]

person_in_quote = 0
type_quote = 1
type_person = 2
def Cases(n_dict):
    global truth_table
    for person, _ in n_dict.items():
        for stats in _:
            person_type = stats[type_person]
            type_of_quote = stats[type_quote]
            person_quote = stats[person_in_quote]
            other_persons = sorted([p for p in person_quote if p != person]) if person in person_quote else person_quote

            if all([person in person_quote, type_of_quote == 'am', person_type == Knave, len(person_quote) == 1]):
                return None

            elif all([person in person_quote, type_of_quote == 'am', person_type == Knight, len(person_quote) == 1]):
                pass

            elif all([len(person_quote) >= 2, type_of_quote == 'am', person_type == Knight, person in person_quote]):
                truth_table = [tt for tt in truth_table if tt[person] == 1 and all(tt[op] != 0 for op in other_persons)]

            elif all([len(person_quote) >= 2, type_of_quote == 'am', person_type == Knight]):
                removing_elements = {tt for tt in truth_table if
                                     (tt[person] == 1 and any(tt[op] == 0 for op in other_persons)) or
                                     (tt[person] == 0 and sum(tt[op] for op in other_persons) == len(person_quote))}
                truth_table = [tt for tt in truth_table if tt not in removing_elements]

            elif all([len(person_quote) == 1, type_of_quote == 'am', person_type == Knight, person not in person_quote]):
                truth_table = [tt for tt in truth_table if all(tt[person] == tt[op] for op in other_persons)]

            elif all([person in person_quote, type_of_quote == 'least', person_type == Knight]):
                truth_table = [tt for tt in truth_table if tt[person] != 0 or all(tt[op] == 0 for op in other_persons)]

            elif all([person not in person_quote, type_of_quote == 'least', person_type == Knight]):
                truth_table = [tt for tt in truth_table if
                               not (tt[person] == 1 and all(tt[op] == 0 for op in other_persons)) and not (
                                           tt[person] == 0 and any(tt[op] != 0 for op in other_persons))]

            elif person in person_quote and type_of_quote == 'exactly' and person_type == Knight:
                truth_table = [tt for tt in truth_table if not ((tt[person] == 0 and (
                            sum(tt[op] == 0 for op in other_persons) != len(other_persons) and sum(
                        tt[op] == 1 for op in other_persons) <= 1)) or (tt[person] == 1 and all(
                    tt[op] == 0 for op in other_persons)))]

            elif all([person not in person_quote, type_of_quote == 'exactly', person_type == Knight]):
                truth_table = [
                    tt for tt in truth_table if not ((tt[person] == 0 and not (
                                        sum(tt[op] == 0 for op in other_persons) in {0, len(other_persons)})) or
                            (tt[person] == 1 and sum(tt[op] == 1 for op in other_persons) != 1))]

            elif all([person in person_quote, type_of_quote == 'most', person_type == Knight]):
                truth_table = [tt for tt in truth_table if not (
                            (tt[person] == 0 and sum(tt[op] == 1 for op in other_persons) <= 1) or
                            (tt[person] == 1 and any(tt[op] == 1 for op in other_persons)))]

            elif all([person not in person_quote, type_of_quote == 'most', person_type == Knight]):
                truth_table = [tt for tt in truth_table if not (
                            (tt[person] == 0 and sum(tt[op] == 1 for op in other_persons) <= 1) or
                            (tt[person] == 1 and not (sum(tt[op] == 1 for op in other_persons) == 1 or all(
                                tt[op] == 0 for op in other_persons))))]

            elif all([person in person_quote, type_of_quote == 'am', person_type == Knave]):
                truth_table = [ tt for tt in truth_table
                    if not (tt[person] == 1 or (tt[person] == 0 and all(tt[op] == 0 for op in other_persons)))]

            elif all([person not in person_quote, type_of_quote == 'am', person_type == Knave]):
                truth_table = [tt for tt in truth_table
                    if not ((tt[person] == 0 and all(tt[op] == 0 for op in other_persons)) or
                            (tt[person] == 1 and any(tt[op] != 0 for op in other_persons)))]

            elif all([person in person_quote, type_of_quote == 'least', person_type == Knave]):
                truth_table = [tt for tt in truth_table if
                               not (tt[person] == 0 or (tt[person] == 1 and all(tt[op] == 1 for op in other_persons)))]

            elif all([person not in person_quote, type_of_quote == 'least', person_type == Knave]):
                truth_table = [tt for tt in truth_table
                    if not ((tt[person] == 0 and any(tt[op] == 0 for op in other_persons)) or
                            (tt[person] == 1 and all(tt[op] == 1 for op in other_persons)))]

            elif all([person in person_quote, type_of_quote == 'exactly', person_type == Knave]):
                truth_table = [tt for tt in truth_table
                    if not ((tt[person] == 0 and not any(tt[op] == 0 for op in other_persons)) or
                            (tt[person] == 1 and sum(tt[op] == 0 for op in other_persons) != 1))]

            elif all([person not in person_quote, type_of_quote == 'exactly', person_type == Knave]):
                truth_table = [tt for tt in truth_table
                    if not ((tt[person] == 0 and sum(tt[op] == 0 for op in other_persons) == 1) or
                            (tt[person] == 1 and sum(tt[op] == 0 for op in other_persons) != 1))]

            elif all([person in person_quote, type_of_quote == 'most', person_type == Knave]):
                truth_table = [tt for tt in truth_table
                    if ((tt[person] == 0 and any(tt[op] == 0 for op in other_persons)) or
                            (tt[person] == 1 and (sum(tt[op] == 0 for op in other_persons) == 1 or all(
                                tt[op] == 1 for op in other_persons))))]

            elif all([person not in person_quote, type_of_quote == 'most', person_type == Knave]):
                truth_table = [tt for tt in truth_table
                    if ((tt[person] == 0 and sum(tt[op] == 0 for op in other_persons) >= 2) or
                            (tt[person] == 1 and (sum(tt[op] == 0 for op in other_persons) == 1 or all(
                                tt[op] == 1 for op in other_persons))))]
    return truth_table

solutions = Cases(dict_data)
knight_knave = {1: 'Knight', 0: 'Knave'}
if solutions is None:
    print('There is no solution.')
elif len(solutions) == 1:
    print('There is a unique solution:')
    for name, type_of_person in zip(list_names, solutions[0]):
        print(f'Sir {name} is a {knight_knave[type_of_person]}.')
elif len(solutions) >= 2:
    print(f'There are {len(solutions)} solutions.')
