# project.py


import pandas as pd
import numpy as np
from pathlib import Path

import plotly.express as px


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def get_assignment_names(grades):

    filtered_grades = grades.drop(columns=[col for col in grades.columns if len(col.split(' ')) > 1])

    key = ['lab', 'project', 'midterm', 'final', 'disc', 'checkpoint']
    result = {k: [] for k in key}
    
    for col in filtered_grades.columns:
        for k in key:
            if k == 'project' and 'checkpoint' in col.lower():
                continue 
            if k == 'checkpoint' and k in col.lower():
                result[k].append(col)
            elif col.lower().startswith(k):
                result[k].append(col)
    return result




# ---------------------------------------------------------------------
# QUESTION 2
# ---------------------------------------------------------------------


def projects_total(grades):

    projects = get_assignment_names(grades)['project']

    earned_cols = projects
    max_cols = [col for col in grades.columns 
                if any(p in col for p in projects) and 'Max Points' in col]
    
    earned = grades[earned_cols].sum(axis=1)
    total = grades[max_cols].sum(axis=1)
    
    return earned / total


# ---------------------------------------------------------------------
# QUESTION 3
# ---------------------------------------------------------------------


def lateness_penalty(col):

    def get_multiplier(time_str):
        h, m, s = time_str.split(":")
        total_late = int(h) + int(m)/60 + int(s)/3600
        
        if total_late <= 2:
            return 1.0
        elif total_late <= 168:
            return 0.9
        elif total_late <= 336:
            return 0.7
        else:
            return 0.4
    
    return col.apply(get_multiplier)


# ---------------------------------------------------------------------
# QUESTION 4
# ---------------------------------------------------------------------


def process_labs(grades):
    ...


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def lab_total(processed):
    ...


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def total_points(grades):
    ...


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def final_grades(total):
    ...

def letter_proportions(total):
    ...


# ---------------------------------------------------------------------
# QUESTION 8
# ---------------------------------------------------------------------


def raw_redemption(final_breakdown, question_numbers):
    ...
    
def combine_grades(grades, raw_redemption_scores):
    ...


# ---------------------------------------------------------------------
# QUESTION 9
# ---------------------------------------------------------------------


def z_score(ser):
    ...
    
def add_post_redemption(grades_combined):
    ...


# ---------------------------------------------------------------------
# QUESTION 10
# ---------------------------------------------------------------------


def total_points_post_redemption(grades_combined):
    ...
        
def proportion_improved(grades_combined):
    ...


# ---------------------------------------------------------------------
# QUESTION 11
# ---------------------------------------------------------------------


def section_most_improved(grades_analysis):
    ...
    
def top_sections(grades_analysis, t, n):
    ...


# ---------------------------------------------------------------------
# QUESTION 12
# ---------------------------------------------------------------------


def rank_by_section(grades_analysis):
    ...







# ---------------------------------------------------------------------
# QUESTION 13
# ---------------------------------------------------------------------


def letter_grade_heat_map(grades_analysis):
    ...
