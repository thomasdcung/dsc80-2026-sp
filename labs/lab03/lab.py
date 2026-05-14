# lab.py


import os
import io
from pathlib import Path
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def read_linkedin_survey(dirname):

    dirname = Path(dirname)
    target_columns = ['first name', 'last name', 'current company', 'job title', 'email', 'university']

    dfs = []
    for file in dirname.iterdir():

        if file.name.startswith('survey') and file.suffix == '.csv':
            
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip().str.lower().str.replace('_', ' ')
            df = df[target_columns]
            dfs.append(df)

    combined = pd.concat(dfs, ignore_index=True)
    return combined

def com_stats(df):
    
    ohio = df[df['university'].str.contains('Ohio', na=False)]
    prop_programmer = ohio['job title'].str.contains('Programmer', na=False).mean()

    ends_engineer = df['job title'].str.endswith('Engineer', na=False)
    num_engineer_titles = df[ends_engineer]['job title'].nunique()

    longest_title = df['job title'].str.len().idxmax()
    longest_job_title = df.loc[longest_title, 'job title']

    num_managers = df['job title'].str.contains('manager', case=False, na=False).sum()

    return [prop_programmer, num_engineer_titles, longest_job_title, num_managers]



# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def read_student_surveys(dirname):
    dirname = Path(dirname)
    
    dfs = []
    for file in sorted(dirname.iterdir()):
        if file.name.startswith('favorite') and file.suffix == '.csv':
            df = pd.read_csv(file, index_col='id')
            dfs.append(df)
    
    combined = pd.concat(dfs, axis=1)
    combined.index.name = 'id'
    return combined


def check_credit(df):
    
    survey_cols = [col for col in df.columns if col != 'name']
    
    answers = df[survey_cols].copy()
    if 'genre' in answers.columns:
        answers['genre'] = answers['genre'].replace('(no genres listed)', pd.NA)
    
    num_questions = len(survey_cols)
    answered = answers.notna().sum(axis=1)
    student_ec = (answered / num_questions >= 0.5).astype(int) * 5

    response_rates = answers.notna().mean()
    num_qualifying = (response_rates >= 0.90).sum()
    class_ec = min(num_qualifying, 2)

    result = pd.DataFrame({
        'name': df['name'],
        'ec': student_ec + class_ec
    })
    result.index.name = 'id'
    return result


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def most_popular_procedure(pets, procedure_history):

    registered = procedure_history[procedure_history['PetID'].isin(pets['PetID'])]
    return registered['ProcedureType'].value_counts().idxmax()


def pet_name_by_owner(owners, pets):
    merged = owners.merge(pets, on='OwnerID', how='left')

    def collect_names(names):
        valid = names.dropna().tolist()
        if len(valid) == 1:
            return valid[0]
        return valid

    result = merged.groupby('OwnerID')['Name_y'].apply(collect_names)

    result.index = result.index.map(owners.set_index('OwnerID')['Name'])
    result.index.name = 'Name'
    return result


def total_cost_per_city(owners, pets, procedure_history, procedure_detail):

    history_with_price = procedure_history.merge(
        procedure_detail, on=['ProcedureType', 'ProcedureSubCode'], how='left'
    )

    pets_with_city = pets.merge(owners[['OwnerID', 'City']], on='OwnerID', how='left')
    
    full = history_with_price.merge(pets_with_city[['PetID', 'City']], on='PetID', how='left')
    
    city_spend = full.groupby('City')['Price'].sum()
    all_cities = owners['City'].unique()
    return city_spend.reindex(all_cities, fill_value=0)


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def average_seller(sales):
    return sales.pivot_table(
        values='Total',
        index='Name',
        aggfunc='mean'
    ).rename(columns={'Total': 'Average Sales'})


def product_name(sales):
    return sales.pivot_table(
        values='Total',
        index='Name',
        columns='Product',
        aggfunc='sum'
    )


def count_product(sales):
    return sales.pivot_table(
        values='Total',
        index=['Product', 'Name'],
        columns='Date',
        aggfunc='count',
        fill_value=0
    )


def total_by_month(sales):
    # Derive a Month column from the Date string
    temp = sales.copy()
    temp['Month'] = pd.to_datetime(temp['Date'], format='%m.%d.%Y').dt.month_name()

    return temp.pivot_table(
        values='Total',
        index=['Name', 'Product'],
        columns='Month',
        aggfunc='sum',
        fill_value=0
    )