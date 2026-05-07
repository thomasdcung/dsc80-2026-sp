# lab.py


import pandas as pd
import numpy as np
import io
from pathlib import Path
import os


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def prime_time_logins(login):

    login = login.copy()
    login['Time'] = pd.to_datetime(login['Time'])
    hour = login['Time'].dt.hour
    prime = login[(hour >= 16) & (hour < 20)]
    result = prime.groupby('Login Id')['Time'].count().to_frame(name='Time')
    # Include all users, even those with 0 prime-time logins
    all_users = login.groupby('Login Id')['Time'].count().to_frame(name='Time')
    result = result.reindex(all_users.index, fill_value=0)
    return result


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def count_frequency(login):

    login = login.copy()
    login['Time'] = pd.to_datetime(login['Time'])
    today = pd.Timestamp('2024-01-31 23:59:00')
 
    def freq(times):
        count = len(times)
        first = times.min()
        days = (today - first).days
        if days == 0:
            days = 1
        return count / days
 
    return login.groupby('Login Id')['Time'].agg(freq)



# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def cookies_null_hypothesis():

    return [1, 2]
 
 
def cookies_p_value(N):

    observed = 15  # burnt cookies
    n = 250
    p_null = 0.04  # probability of being burnt under null
 
    simulations = np.random.binomial(n, p_null, N)
    p_value = (simulations >= observed).mean()
    return p_value



# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


 
def car_null_hypothesis():

    return [1, 4]
 
 
def car_alt_hypothesis():

    return [2, 6]
 
 
def car_test_statistic():

    return [1, 4]
 
 
def car_p_value():

    return 4
 


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def superheroes_test_statistic():

    return [1, 2]
 
 
def bhbe_col(heroes):

    blond = heroes['Hair color'].str.lower().str.contains('blond', na=False)
    blue = heroes['Eye color'].str.lower().str.contains('blue', na=False)
    return blond & blue
 
 
def superheroes_observed_statistic(heroes):

    bhbe = bhbe_col(heroes)
    bhbe_heroes = heroes[bhbe]
    return (bhbe_heroes['Alignment'] == 'good').mean()
 
 
def simulate_bhbe_null(heroes, N):

    bhbe = bhbe_col(heroes)
    n_bhbe = bhbe.sum()
    overall_good_prop = (heroes['Alignment'] == 'good').mean()
 
    simulations = np.random.binomial(n_bhbe, overall_good_prop, N) / n_bhbe
    return simulations
 
 
def superheroes_p_value(heroes):

    obs = superheroes_observed_statistic(heroes)
    simulations = simulate_bhbe_null(heroes, 100000)
    p_value = (simulations >= obs).mean()
    decision = 'Reject' if p_value < 0.01 else 'Fail to reject'
    return [p_value, decision]



# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def diff_of_means(data, col='orange'):

    groups = data.groupby('Factory')[col].mean()
    return abs(groups.iloc[0] - groups.iloc[1])
 
 
def simulate_null(data, col='orange'):

    shuffled = data.copy()
    shuffled['Factory'] = np.random.permutation(data['Factory'].values)
    return diff_of_means(shuffled, col)
 
 
def color_p_value(data, col='orange'):

    obs = diff_of_means(data, col)
    sims = np.array([simulate_null(data, col) for _ in range(1000)])
    return (sims >= obs).mean()



# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------

def ordered_colors():

    return [
        ('yellow', 0.0),
        ('orange', 0.043),
        ('red', 0.235),
        ('green', 0.491),
        ('purple', 0.97),
    ]


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


    
def same_color_distribution():

    return (0.008, 'Reject')



# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def perm_vs_hyp():

    return ['P', 'P', 'H', 'H', 'P']

