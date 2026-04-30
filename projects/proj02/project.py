# project.py


import pandas as pd
import numpy as np
np.set_printoptions(threshold=20, suppress=True, legacy='1.21')

from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pd.options.plotting.backend = 'plotly'

from IPython.display import display

# DSC 80 preferred styles
pio.templates["dsc80"] = go.layout.Template(
    layout=dict(
        margin=dict(l=30, r=30, t=30, b=30),
        autosize=True,
        width=600,
        height=400,
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        title=dict(x=0.5, xanchor="center"),
    )
)
pio.templates.default = "simple_white+dsc80"
import warnings
warnings.filterwarnings("ignore")


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def clean_loans(loans):
    loans = loans.copy()
    loans['emp_title'] = loans['emp_title'].str.strip().str.lower().replace('rn', 'registered nurse')
    loans['issue_d'] = pd.to_datetime(loans['issue_d'])
    loans['term'] = loans['term'].apply(lambda x: int(x.strip().split(' ')[0]))
    loans['term_end'] = loans.apply(lambda row: row['issue_d'] + pd.DateOffset(months=row['term']), axis=1)
    return loans


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def correlations(loans, pairs):
    results = []
    
    for pair in pairs:
        col1, col2 = pair
        corr = loans[[col1, col2]].corr().iloc[0, 1]
        results.append(('r_' + col1 + '_' + col2, corr))

    return pd.Series(dict(results))


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def create_boxplot(loans):
    loans = loans.copy()
    loans['fico_bin'] = pd.cut(loans['fico_range_low'], bins=[580, 670, 740, 800, 850], right=False)
    fico_order = loans['fico_bin'].cat.categories.astype(str).tolist()
    loans['fico_bin'] = loans['fico_bin'].astype(str)
    
    return px.box(loans, x='fico_bin', y='int_rate', color='term', color_discrete_map={36: 'red', 60: 'blue'},
                  category_orders={'fico_bin': fico_order, 'term': sorted(loans['term'].unique())},
                  labels={'fico_bin': 'Credit Score Range', 
                          'int_rate': 'Interest Rate (%)', 
                          'term': 'Loan Length (Months)'},
                  title='Interest Rate vs. Credit Score')


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def ps_test(loans, N):
    loans = loans.copy()
    loans['has_ps'] = loans['desc'].notna()
    
    observed_diff = (
        loans.groupby('has_ps')['int_rate'].mean()[True] 
        - loans.groupby('has_ps')['int_rate'].mean()[False]
    )
    
    diffs = []
    for _ in range(N):
        shuffled = loans['has_ps'].sample(frac=1).reset_index(drop=True)
        loans_copy = loans.copy()
        loans_copy['has_ps'] = shuffled
        diff = (
            loans_copy.groupby('has_ps')['int_rate'].mean()[True]
            - loans_copy.groupby('has_ps')['int_rate'].mean()[False]
        )
        diffs.append(diff)
    
    diffs = np.array(diffs)
    return (diffs >= observed_diff).mean()
 
    
def missingness_mechanism():
    return 2
    
def other_missingness():
    return 1



# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def tax_owed(income, brackets):
    ...


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def clean_state_taxes(state_taxes_raw): 
    ...


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def state_brackets(state_taxes):
    ...
    
def combine_loans_and_state_taxes(loans, state_taxes):
    # Start by loading in the JSON file.
    # state_mapping is a dictionary; use it!
    import json
    state_mapping_path = Path('data') / 'state_mapping.json'
    with open(state_mapping_path, 'r') as f:
        state_mapping = json.load(f)
        
    # Now it's your turn:
    ...


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def find_disposable_income(loans_with_state_taxes):
    FEDERAL_BRACKETS = [
     (0.1, 0), 
     (0.12, 11000), 
     (0.22, 44725), 
     (0.24, 95375), 
     (0.32, 182100),
     (0.35, 231251),
     (0.37, 578125)
    ]
    ...


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def aggregate_and_combine(loans, keywords, quantitative_column, categorical_column):
    ...


# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------


def exists_paradox(loans, keywords, quantitative_column, categorical_column):
    ...
    
def paradox_example(loans):
    return {
        'loans': loans,
        'keywords': [..., ...],
        'quantitative_column': ...,
        'categorical_column': ...
    }
