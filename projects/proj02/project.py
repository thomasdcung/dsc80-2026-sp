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
    total_tax = 0.0
    for i, (rate, lower) in enumerate(brackets):
        # Determine upper bound of this bracket
        if i + 1 < len(brackets):
            upper = brackets[i + 1][1]
        else:
            upper = float('inf')
        
        if income <= lower:
            break
        
        taxable_in_bracket = min(income, upper) - lower
        total_tax += rate * taxable_in_bracket
    
    return total_tax


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def clean_state_taxes(state_taxes_raw): 
    df = state_taxes_raw.copy()
    
    # Drop rows where all values are NaN (separator rows)
    df = df.dropna(how='all')
    
    # Replace non-state-name values in State column with NaN
    # State names don't start with '(' 
    df['State'] = df['State'].where(
        df['State'].str.match(r'^(?!\().*', na=False),
        other=np.nan
    )
    
    # Forward-fill state names
    df['State'] = df['State'].ffill()
    
    # Clean the Rate column: convert percentages to floats
    def parse_rate(r):
        if pd.isna(r):
            return 0.0
        r = str(r).strip().rstrip('%')
        if r.lower() == 'none':
            return 0.0
        return round(float(r) / 100, 4)
    
    df['Rate'] = df['Rate'].apply(parse_rate)
    
    # Clean the Lower Limit column: convert currency strings to integers
    def parse_lower_limit(v):
        if pd.isna(v):
            return 0
        v = str(v).strip().replace('$', '').replace(',', '').strip()
        try:
            return int(float(v))
        except:
            return 0
    
    df['Lower Limit'] = df['Lower Limit'].apply(parse_lower_limit)
    
    df = df.reset_index(drop=True)
    return df



# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def state_brackets(state_taxes):
    return (
        state_taxes
        .groupby('State')
        .apply(lambda df: list(zip(df['Rate'], df['Lower Limit'])))
        .rename('bracket_list')
        .to_frame()
    )
    
def combine_loans_and_state_taxes(loans, state_taxes):
    # Start by loading in the JSON file.
    # state_mapping is a dictionary; use it!
    import json
    state_mapping_path = Path('data') / 'state_mapping.json'
    with open(state_mapping_path, 'r') as f:
        state_mapping = json.load(f)
    
    # Build state_brackets DataFrame
    sb = state_brackets(state_taxes)
    
    # Add two-letter state abbreviation to sb
    # state_mapping maps abbreviated state names (like 'Ala.') to two-letter codes ('AL')
    sb = sb.reset_index()
    sb['State'] = sb['State'].map(state_mapping)
    sb = sb.set_index('State')
    
    # Rename addr_state to State in loans
    loans = loans.copy()
    loans = loans.rename(columns={'addr_state': 'State'})
    
    # Merge loans with state brackets on State
    result = loans.merge(sb, on='State', how='left')
    
    return result



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
    
    df = loans_with_state_taxes.copy()
    
    df['federal_tax_owed'] = df['annual_inc'].apply(lambda inc: tax_owed(inc, FEDERAL_BRACKETS))
    df['state_tax_owed'] = df.apply(lambda row: tax_owed(row['annual_inc'], row['bracket_list']), axis=1)
    df['disposable_income'] = df['annual_inc'] - df['federal_tax_owed'] - df['state_tax_owed']
    
    return df



# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def aggregate_and_combine(loans, keywords, quantitative_column, categorical_column):
    result_cols = {}
    
    for keyword in keywords:
        mask = loans['emp_title'].str.contains(keyword, na=False)
        subset = loans[mask]
        
        # Per-category means
        per_cat = subset.groupby(categorical_column)[quantitative_column].mean()
        
        # Overall mean
        overall = pd.Series({categorical_column: 'Overall', quantitative_column: subset[quantitative_column].mean()})
        
        col_name = f'{keyword}_mean_{quantitative_column}'
        result_cols[keyword] = (per_cat, subset[quantitative_column].mean(), col_name)
    
    # Build combined DataFrame
    keyword1, keyword2 = keywords
    per_cat1, overall1, col1 = result_cols[keyword1]
    per_cat2, overall2, col2 = result_cols[keyword2]
    
    combined = pd.DataFrame({col1: per_cat1, col2: per_cat2})
    combined.index.name = categorical_column
    
    overall_row = pd.DataFrame({col1: [overall1], col2: [overall2]}, index=pd.Index(['Overall'], name=categorical_column))
    
    return pd.concat([combined, overall_row])


# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------


def exists_paradox(loans, keywords, quantitative_column, categorical_column):
    df = aggregate_and_combine(loans, keywords, quantitative_column, categorical_column)
    col1, col2 = df.columns[:2]
    
    non_overall = df.iloc[:-1].dropna()
    
    return bool((non_overall[col1] > non_overall[col2]).all() != (df.iloc[-1][col1] > df.iloc[-1][col2]))
    
def paradox_example(loans):
    return {
        'loans': loans,
        'keywords': ['teacher', 'engineer'],
        'quantitative_column': 'int_rate',
        'categorical_column': 'grade'
    }

 
