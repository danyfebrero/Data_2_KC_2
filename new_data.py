#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 17:44:16 2022

@author: Daniel Jimenez
"""

import pandas as pd
import json


DATA_FILE = r'new_data.xlsx'

def load_file(filename):
    """ 
        Does: Loads the tables in the file to dataframes\n
        Arguments: filename with the extension\n
        Return: Retainer and Beauties dataframes\n
    """
    retainers_df = pd.read_excel(filename, sheet_name = "Retainers", engine='openpyxl')    
    beauties_df = pd.read_excel(filename, sheet_name = "Beauties", engine='openpyxl')
    
    return(retainers_df, beauties_df)

def create_bond_table (retainer_df):
    """ 
        Does: splits the bonds of each retainer and creates a bond table
        Arguments explanation: retainer_df is the table with all the retainers data
        Return: a new table with the bonds
    """
    bond_df = pd.DataFrame(columns = ['Retainer', 'Bond'])
    
    for index, row in retainer_df.iterrows():
        bonds = row['Bonds'].split(", ")
        for beauty in bonds:
            bond_df.loc[len(bond_df.index)] = [row['Retainer Name'], beauty]
    return(bond_df)

def cleaning_data(retainers_df, beauties_df):
    """ 
        Does: Rename all the column names taht needed a fix\n
        Arguments: retainer dataframe and beauties dataframe\n
        Return: uodated datafrmas for retainers and beauties\n
    """
    retainers_df.drop('Bonds', axis=1, inplace = True)
    retainers_df.rename(columns={
        'Retainer Name': 'retainer_name',
        'Skill 1': 'Skill_1', 'Skill 2': 'Skill_2',
        'Skill 3': 'Skill_3', 'Skill 4': 'Skill_4',
        'Skill 5': 'Skill_5', 'Skill 6': 'Skill_6',
        'Skill 7': 'Skill_7', 'Skill 8': 'Skill_8',
        'Skill 9': 'Skill_9', 'Skill 10': 'Skill_10',
        'Skill 11': 'Skill_11', 'Skill 12': 'Skill_12',
        'Talent 1': 'Talent_1', 'Talent 2': 'Talent_2',
        'Talent 3': 'Talent_3', 'Talent 4': 'Talent_4',
        'Aura 1': 'Aura_1', 'Aura 2': 'Aura_2',
        'Aura 3': 'Aura_3'
        }, inplace=True)
    beauties_df.rename(columns={
        'Banner Effect ': 'Banner_Effect',
        'Min Banner': 'Min_Banner',
        'Max Banner': 'Max_Banner'
        }, inplace=True)

    for index, row in retainers_df.iterrows():   
        if len(row['Grade'].split(", ")) > 1:
            new_row = row
            grades = new_row['Grade'].split(", ")
            retainers_df.loc[index,['Grade']] = grades[0]
            grades.pop(0)
            for grade in grades:
                new_row['Grade'] = grade
                retainers_df.loc[len(retainers_df.index)] = new_row

    return(retainers_df, beauties_df)
        
def save_json(retainers_df, beauties_df, bond_df):
    data = {}
    data['retainers'] = retainers_df.to_dict(orient='index')
    data['beauties'] = beauties_df.to_dict(orient='index')
    data['bonds'] = bond_df.to_dict(orient='index')
    filename = 'trading_legend.json'
    with open (filename,'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        
def save_xlsx(retainers_df, beauties_df, bond_df):     
    filename = 'trading_legend.xlsx'

    with pd.ExcelWriter(filename,
        engine="openpyxl"
    ) as writer:
        retainers_df.to_excel(writer, sheet_name="Retainers")
        beauties_df.to_excel(writer, sheet_name="Beauties")
        bond_df.to_excel(writer, sheet_name="Bonds") 

def process_xlms():
    """ 
        Does: loads the dataframes
        Arguments explanation:
        Return:
    """
    print('Loading data...')
    retainers_df, beauties_df = load_file(DATA_FILE)
    print('Creating tables...')
    bond_df = create_bond_table(retainers_df)
    print('Cleaning data...')
    retainers_df, beauties_df = cleaning_data(retainers_df, beauties_df)
    print('Exporting data...')
    save_json(retainers_df, beauties_df, bond_df)
    save_xlsx(retainers_df, beauties_df, bond_df)
    print('Done.')
    
def main():

    process_xlms()

if __name__ == '__main__':
    main()