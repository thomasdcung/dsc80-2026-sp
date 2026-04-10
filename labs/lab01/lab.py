# lab.py


import os
from pathlib import Path
import io

import pandas as pd
import numpy as np
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

np.set_printoptions(legacy='1.21')


# ---------------------------------------------------------------------
# QUESTION 0
# ---------------------------------------------------------------------


def consecutive_ints(ints):
    if len(ints) == 0:
        return False

    for k in range(len(ints) - 1):
        diff = abs(ints[k] - ints[k+1])
        if diff == 1:
            return True

    return False


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def median_vs_mean(nums):
    
    mean = sum(nums) / len(nums)

    sorted_nums = sorted(nums)
    n = len(nums)
    if n % 2 == 1:
        median = sorted_nums[n // 2]
    else:
        median = (sorted_nums[n // 2 -1] + sorted_nums[n// 2])/2

    return median <= mean


# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def n_prefixes(s, n):
    prefixes = ""
    for i in range(n, 0, -1):
        prefixes += (s[:i])
    return prefixes


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def exploded_numbers(ints, n):
    fill = len(str(max(ints)+n))
    newInts = []
    for num1 in ints:
        temp = ""
        for num2 in range(num1 - n, num1 + n + 1):
            temp += str(num2).zfill(fill) + " "
        newInts.append(temp.strip())
    return newInts


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def last_chars(fh):
    result = ""
    for line in fh:
        line = line.strip()
        if len(line) > 0:
            result += line[-1]
    return result


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def add_root(A):
    return A + np.sqrt(np.arange(len(A)))

def where_square(A):
    return (np.sqrt(A) % 1 == 0)


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def filter_cutoff_loop(matrix, cutoff):
    result= []
    numCols = len(matrix[0])
    numRows = len(matrix)

    for m in range(numRows):
        colSum = 0
        
        for n in range(numCols):
            colSum += matrix[m][n]
        colMean = colSum / numRows

        if colMean > cutoff:
            col = [matrix[m][n] for i in range(numRows)]
            result.append(col)

    return result


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def filter_cutoff_np(matrix, cutoff):
    colMeans = np.mean(matrix, axis=0)
    return matrix[:, colMeans > cutoff]


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def growth_rates(A):
    return np.round((A[1:] - A[:-1]) / A[:1], 2)

def with_leftover(A):
    leftover = np.cumsum(20 % A)
    days = np.where(leftover >= A)[0]
    return int(days[0]) if len(days) > 0 else -1


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def salary_stats(salary):
    num_players = salary.shape[0]
    num_teams = salary['Team'].nunique()
    total_salary = salary['Salary'].sum()
    highest_salary = salary.loc[salary['Salary'].idxmax(), 'Player']
    avg_los = round(salary[salary['Team'] == 'Los Angeles Lakers']['Salary'].mean(), 2)
    fifth_lowest = salary.nsmallest(5, 'Salary').iloc[-1][['Player', 'Team']].str.cat(sep=', ')
    duplicates = salary['Player'].str.split().str[1].duplicated().any()
    total_highest = salary[salary['Team'] == (salary.loc[salary['Salary'].idxmax(), 'Team'])]['Salary'].sum()
    return pd.Series(
    [num_players, num_teams, total_salary, highest_salary, avg_los, fifth_lowest, duplicates, total_highest],
    index=['num_players', 'num_teams', 'total_salary', 'highest_salary', 'avg_los', 'fifth_lowest', 'duplicates', 'total_highest']
    )


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def parse_malformed(fp):
    rows = []

    with open(fp, 'r') as f:
        lines = f.readlines()

    header = [col.strip().strip('"') for col in lines[0].strip().split(',')]

    for line in lines[1:]:
        line = line.strip().strip(',')
        if not line:
            continue


        cleaned = line.replace('"', '').replace(',,', ',')

        parts = cleaned.split(',')

        first  = parts[0].strip()
        last   = parts[1].strip()
        weight = float(parts[2].strip())
        height = float(parts[3].strip())
        geo    = parts[4].strip() + ',' + parts[5].strip()

        rows.append({
            'first':  first,
            'last':   last,
            'weight': weight,
            'height': height,
            'geo':    geo
        })

    return pd.DataFrame(rows, columns=header)
