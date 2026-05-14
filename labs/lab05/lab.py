# lab.py


from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def after_purchase():
    return ['NMAR', 'MD', 'MAR', 'MAR', 'MAR']


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def multiple_choice():
    return ['MAR', 'NMAR', 'MD', 'NMAR', 'MCAR']


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------



def first_round():
    fp = Path('data') / 'payment.csv'
    df = pd.read_csv(fp)
 
    df['dob'] = pd.to_datetime(df['date_of_birth'], format='%d-%b-%Y', errors='coerce')
    df['age'] = 2024 - df['dob'].dt.year
 
    ages_missing = df[df['credit_card_number'].isnull()]['age'].dropna().values
    ages_present = df[df['credit_card_number'].notnull()]['age'].dropna().values
 
    observed_stat = abs(ages_missing.mean() - ages_present.mean())
 
    combined = np.concatenate([ages_missing, ages_present])
    n_missing = len(ages_missing)
 
    np.random.seed(42)
    perm_stats = []
    for _ in range(1000):
        perm = np.random.permutation(combined)
        perm_stats.append(abs(perm[:n_missing].mean() - perm[n_missing:].mean()))
 
    p_value = float(np.mean(np.array(perm_stats) >= observed_stat))
    result = 'R' if p_value < 0.05 else 'NR'
 
    return [p_value, result]



def second_round():
    fp = Path('data') / 'payment.csv'
    df = pd.read_csv(fp)
 
    df['dob'] = pd.to_datetime(df['date_of_birth'], format='%d-%b-%Y', errors='coerce')
    df['age'] = 2024 - df['dob'].dt.year
 
    ages_missing = df[df['credit_card_number'].isnull()]['age'].dropna().values
    ages_present = df[df['credit_card_number'].notnull()]['age'].dropna().values
 
    ks_result = stats.ks_2samp(ages_missing, ages_present)
    p_value = float(ks_result.pvalue)
 
    result = 'R' if p_value < 0.05 else 'NR'
    conclusion = 'D' if result == 'R' else 'ND'
 
    return [p_value, result, conclusion]



# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def verify_child(heights):
    child_cols = [c for c in heights.columns if c.startswith('child_')]
 
    pvals = {}
    for col in child_cols:
        father_missing = heights[heights[col].isnull()]['father']
        father_present = heights[heights[col].notnull()]['father']
        ks = stats.ks_2samp(father_missing, father_present)
        pvals[col] = ks.pvalue
 
    return pd.Series(pvals)



# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def cond_single_imputation(new_heights):
    new_heights = new_heights.copy()
    new_heights['father_bin'] = pd.qcut(new_heights['father'], q=4)
    group_means = new_heights.groupby('father_bin')['child'].transform('mean')
    return new_heights['child'].fillna(group_means)


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def quantitative_distribution(child, N):

    observed = child.dropna().values
    counts, bin_edges = np.histogram(observed, bins=10)
    areas = counts / counts.sum()
 
    imputed = []
    for _ in range(N):
        bin_idx = np.random.choice(len(counts), p=areas)
        value = np.random.uniform(bin_edges[bin_idx], bin_edges[bin_idx + 1])
        imputed.append(value)
 
    return np.array(imputed)




def impute_height_quant(child):
    child = child.copy()
    n_missing = child.isnull().sum()
    if n_missing == 0:
        return child
    imputed_values = quantitative_distribution(child, n_missing)
    child[child.isnull()] = imputed_values
    return child



# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def answers():
    mc_answers = [1, 2, 2, 1]
    websites = [
        'https://toscrape.com',
        'https://www.facebook.com',
    ]
    return mc_answers, websites

