# project.py


import pandas as pd
import numpy as np
from pathlib import Path

import plotly.express as px


# ---------------------------------------------------------------------
# QUESTION 1
# ---------------------------------------------------------------------


def get_assignment_names(grades):
    filtered_grades = grades.drop(columns=[col for col in grades.columns if len(col.split(' ')) > 1 or "_free_response" in col])

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

    max_pts = []
    earned_pts = []

    for project in projects:
        earned_pts.append(project)
        max_pts.append(project + ' - Max Points')
        if project + '_free_response' in grades.columns:
            max_pts.append(project + '_free_response - Max Points')
            earned_pts.append(project + '_free_response')
            
    
    earned = grades[earned_pts].fillna(0).sum(axis=1)
    total = grades[max_pts].sum(axis=1)
    
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
    processed = pd.DataFrame()
    labs = get_assignment_names(grades)['lab']
 
    for lab in labs:
        max_pts = lab + ' - Max Points'
        penalties = lab + ' - Lateness (H:M:S)'
        processed[lab] = (
            grades[lab].fillna(0) / grades[max_pts]
            * lateness_penalty(grades[penalties])
        )
 
    return processed


# ---------------------------------------------------------------------
# QUESTION 5
# ---------------------------------------------------------------------


def lab_total(processed_labs):
    return (processed_labs.sum(axis=1) - processed_labs.min(axis=1)) / (processed_labs.shape[1] - 1)


# ---------------------------------------------------------------------
# QUESTION 6
# ---------------------------------------------------------------------


def total_points(grades):
    grades = grades.fillna(0)
    lab_score = lab_total(process_labs(grades)) * 0.2
    project_score = projects_total(grades) * 0.3
    midterm_score = grades['Midterm'] / grades['Midterm - Max Points'] * 0.15
    final_score = grades['Final'] / grades['Final - Max Points'] * 0.30

    def component_score(component):
        cols = get_assignment_names(grades)[component]
        max_pts = []
        for col in cols:
            max_pts.append(col + ' - Max Points')
        earned = grades[cols].fillna(0).sum(axis=1)
        total = grades[max_pts].sum(axis=1)
        return (earned / total) * 0.025

    disc_score = component_score('disc')
    checkpoint_score = component_score('checkpoint')
    
    return lab_score + project_score + midterm_score + final_score + disc_score + checkpoint_score


# ---------------------------------------------------------------------
# QUESTION 7
# ---------------------------------------------------------------------


def final_grades(total):
    conditions = [
        total >= 0.9,
        total >= 0.8,
        total >= 0.7,
        total >= 0.6
    ]
    choices = ['A', 'B', 'C', 'D']
    return pd.Series(np.select(conditions, choices, default='F'), index=total.index)
 
 
def letter_proportions(course_grades):
    active = course_grades[course_grades > 0]
    letters = final_grades(active)
    counts = letters.value_counts().sort_values(ascending=False)
    n = len(active)
    
    props = {}
    running_sum = 0.0
    for i, (letter, count) in enumerate(counts.items()):
        if i == len(counts) - 1:
            props[letter] = 1.0 - running_sum
        else:
            props[letter] = count / n
            running_sum += props[letter]
    
    return pd.Series(props)


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
