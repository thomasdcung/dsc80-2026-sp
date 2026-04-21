# lab.py


import os
import io
from pathlib import Path
import pandas as pd
import numpy as np


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def trick_me():

    tricky_1 = pd.DataFrame(
        [['Andrew', 'Arta', 20],
         ['Thomas', 'Jonah', 21],
         ['Russell', 'Kevin', 22],
         ['Ethan', 'Darren', 23],
         ['Ryan', 'Amine', 24]],
        columns=['Name', 'Name', 'Age']
    )

    tricky_1.to_csv('tricky_1.csv', index=False)
    tricky_2 = pd.read_csv('tricky_1.csv')

    return 3 


def trick_bool():

    bools = pd.DataFrame(
    [[1, 2, 3, 4],
     [5, 6, 7, 8],
     [9, 10, 11, 12],
     [13, 14, 15, 16]],
    columns=[True, True, False, False]
    )

    return [4, 10, 13 ]




# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def population_stats(df):
    num_nonnull = df.notnull().sum()
    num_distinct = df.nunique()
    
    pop_stats = pd.DataFrame({
        'num_nonnull': num_nonnull,
        'prop_nonnull': num_nonnull / df.shape[0],
        'num_distinct': num_distinct,
        'prop_distinct': num_distinct / num_nonnull,
    })

    return pop_stats

# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def most_common(df, N=10):
    result = pd.DataFrame(index=range(N))
    
    for column in df.columns:
        counts = df[column].value_counts()

        values = list(counts.iloc[:N].index) + [np.nan] * (N - len(counts))
        freq = list(counts.iloc[:N].values) + [np.nan] * (N - len(counts))
        
        result[column + '_values'] = values[:N]
        result[column + '_counts'] = freq[:N]
    
    return result



# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def super_hero_powers(powers):
    greatest_powers = powers.loc[(powers == True).sum(axis=1).idxmax(), 'hero_names']

    can_fly = powers[powers['Flight']]
    most_common = can_fly.drop(columns=['hero_names', 'Flight']).sum().idxmax()

    power_counts = (powers == True).sum(axis=1)
    one_power = powers[power_counts == 1]
    most_common_single = one_power.drop(columns=['hero_names']).sum().idxmax()

    return [greatest_powers, most_common, most_common_single]



# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def clean_heroes(heroes):
    return heroes.replace(['-', -99.0], np.nan)


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def super_hero_stats():

    return ['Onslaught', 'George Lucas', 'bad', 'Marvel Comics', 'NBC - Heroes', 'Groot']




# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def clean_universities(df):
    df = df.copy()
    
    df['institution'] = df['institution'].str.replace('\n', ', ')
    
    df['broad_impact'] = df['broad_impact'].astype(int)

    df['nation'] = df['national_rank'].str.split(', ').str[0]
    df['national_rank_cleaned'] = df['national_rank'].str.split(', ').str[1].astype('Int64')
    
    df['nation'] = df['nation'].replace('Czechia', 'Czech Republic')
    df['nation'] = df['nation'].replace('UK', 'United Kingdom')
    
    df = df.drop(columns=['national_rank'])
    
    is_r1 = df['control'].notnull() & df['city'].notnull() & df['state'].notnull()
    df['is_r1_public'] = is_r1 & (df['control'] == 'Public')
    
    df['nation'] = df['nation'].replace('Czechia', 'Czech Republic')
    df['nation'] = df['nation'].replace('UK', 'United Kingdom')
    df['nation'] = df['nation'].replace('USA', 'United States')
    
    return df

def university_info(cleaned):

    state_counts = cleaned.groupby('state')['institution'].count()
    valid_states = state_counts[state_counts >= 3].index
    q_0 = cleaned[cleaned['state'].isin(valid_states)].groupby('state')['score'].mean().idxmin()

    top_100 = cleaned[cleaned['world_rank'] <= 100]
    q_1 = float((top_100['quality_of_faculty'] <= 100).sum() / len(top_100))

    state_total = cleaned.groupby('state')['is_r1_public'].count()
    state_private = (cleaned[cleaned['is_r1_public'] == False]).groupby('state')['is_r1_public'].count()
    state_prop = state_private / state_total
    q_2 = (state_prop >= 0.5).sum()

    q_3 = cleaned[cleaned['national_rank_cleaned'] == 1].sort_values(
        'world_rank', ascending=False
    ).iloc[0]['institution']

    return [q_0, q_1, q_2, q_3]

