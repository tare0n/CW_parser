import json
from classes import HH, Superjob


def vac_list_by_keyword(keyword):
    with open('hh.json', 'r') as hh:
        json_hh = json.load(hh)
    if json_hh['keyword'] != keyword: 
        HH(keyword).dump_vacancies()
        with open('hh.json', 'r') as hh:
            json_hh = json.load(hh)

    with open('superjob.json', 'r') as sj:
        json_sj = json.load(sj)
    if json_sj['keyword'] != keyword: 
        Superjob(keyword).dump_vacancies()
        with open('superjob.json', 'r') as sj:
            json_sj = json.load(sj)

    return json_hh['vacancies'] + json_sj['vacancies']


def sort_vac_list(mode: str, vac_list):
    if mode == "sf":
        vac_list.sort(key=lambda x: x['salary'][0] if x['salary'][0] else 0)
    elif mode == "st":
        vac_list.sort(key=lambda x: x['salary'][1] if x['salary'][1] else 0)
    else:
        raise ValueError("Incorrect mode for sorting, use 'sf' or 'st'")


def dump_to_file(filename, vacs):
    with open(filename, 'w+') as f:
        for vacancy in vacs:
            f.write("title: " + str(vacancy['title']) + '\n'
                    + "description: " + str(vacancy['description']).replace('<highlighttext>', '').replace('</highlighttext>', '') + '\n'
                    + "link: " + str(vacancy['link']) + '\n'
                    + "salary: " + str(vacancy['salary']) + '\n')


if __name__ == '__main__':
    keyword = input('Print keyword for search\n')
    vac_list = vac_list_by_keyword(keyword)
    print(f"There are {len(vac_list)} vacancies found")
    sort_vac_list(input('Print criteria for sorting: '
                        'bottom range of salary (use "sf" marker)'
                        'or upper range of salary (use "st" marker)\n'), vac_list)
    counter = input("How many vacancies you wanna see in file?\n")
    vac_list.reverse()
    dump_to_file(input("print name of file:\n"), vac_list[:int(counter)])


