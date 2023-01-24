import re
import pandas as pd
import numpy as np
import dataframe_image as dfi


# Tekstinio failo nuskaitymas
def read_text():
    with open('settings/text.txt', encoding='utf-8') as f:
        text = f.read()

    return text


# Rikiavimo nustatymas. Jei norima rikiuoti pagal simbolių dažnumą, reikšmė lygi 1, jei pagal leksikografinę tvarką - 0.
# Funckija grąžina true arba false reikšmę.
def read_sorting_setting():
    with open('settings/sorting-settings.txt', encoding='utf-8') as f:
        setting = f.read()
    sort_by = bool(int(setting.split(': ')[1]))
    return sort_by


# Tekstas paverčiamas simbolių sąrašu.
def clean_text(text):
    text_1 = re.sub(r' |\n', '', text)
    characters_list = re.split('', text_1)
    characters_list = characters_list[1:len(characters_list) - 1]
    return characters_list

# Suskaičiuojami simboliai
def count_sort_chars(char_list):
    characters_dict = {}
    for i in char_list:
        if i in characters_dict.keys():
            characters_dict[i] += 1
        else:
            characters_dict[i] = 1
    return characters_dict

# Simbolių rikiavimas ir saugojimas
def sort_save_results(char_dict, sorting_setting):
    # Gauti rezultatai įrašomi į dataframe ir rikiuojami pagal nustatymus
    df = pd.DataFrame.from_dict(char_dict, orient='index').reset_index()
    df.columns = ['Character', 'Freq']
    if sorting_setting:
        sorted_df = df.sort_values('Freq', ascending=False).reset_index(drop=True)
        sorting_name = 'pagal dažnumą'
    else:
        sorted_df = df.sort_values('Character').reset_index(drop=True)
        sorting_name = 'pagal leksikografinę tvarką'

    # Rezultatai išsaugomi png formatu faile 'result.png'
    dfi.export(sorted_df, 'settings/result.png')
    print(f"Tekstinio failo simboliai sėkmingai suskaičiuoti, surikiuoti ir išsaugoti 'result.png' faile.\n"
          f"Rikiavimo tipas: {sorting_name}")


text = read_text()
chars = clean_text(text)
sort_by = read_sorting_setting()
chars_dict = count_sort_chars(chars)
sort_save_results(chars_dict, sort_by)