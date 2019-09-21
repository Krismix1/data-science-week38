# pylint: disable=C0111,W0105
import os
import numpy as np
# import matplotlib.pyplot as plt
import pandas


"""
Cast percentage value to floats
"""
def percentage_remap(percentage):
    return np.float(percentage.replace('%', ''))


"""
Only keep the Subject.n and Absence.n
"""
def keep_only_subject(df, index, max_subjects):
    # Compute all indeces except the selected index
    indeces_to_drop = set(range(0, max_subjects)) - { index }

    template_columns = ['Subject', 'Absence']
    columns_to_drop = [
        f'{col}.{idx}'
        for idx in indeces_to_drop
        for col in template_columns
    ]

    result = df.drop(columns=columns_to_drop)

    # This line assumes that the columns to be renamed
    # Are always at the end, which is not very flexible
    # But it keeps that code simple for now
    result.columns = np.array(list(
        result.columns[:-(len(template_columns))]) + template_columns
    )

    return result


if __name__ == '__main__':
    # Get an absolute to the data file, OS independent
    CURR_DIR = os.path.dirname(os.path.realpath(__file__))
    DATA_FILE = os.path.join(CURR_DIR, 'stud-stat-anonymous.csv')
    # Maximum number of subjects per row of a student
    MAX_SUBJECTS = 4

    # read the CSV file into a DataFrame
    df = pandas.read_csv(DATA_FILE)
    # Drop the first unlabeled column
    df = df.drop(columns=['Unnamed: 0'])
    # TODO: DataFrame.droplevel?

    # Cast all columns with percentage values to floats
    df['Total Absence'] = df['Total Absence'].map(percentage_remap)

    total_absence_mean = df['Total Absence'].mean()
    total_absence_median = df['Total Absence'].median()
    print(total_absence_mean, total_absence_median)
    # Mean Total Absence per Class
    print(df.groupby(['Class'])['Total Absence'].mean())

    # Recreate the data frame, with the new structure
    # This is needed to make sure that we don't duplicate any rows
    df = pandas.DataFrame().append([
        keep_only_subject(df, 0, MAX_SUBJECTS),
        keep_only_subject(df, 1, MAX_SUBJECTS),
        keep_only_subject(df, 2, MAX_SUBJECTS),
        keep_only_subject(df, 3, MAX_SUBJECTS)
    ], ignore_index=True).drop(columns=['Total Absence'])
    df = df.dropna()
    df['Absence'] = df['Absence'].map(percentage_remap)
    # Mean absence per subject
    print(df.groupby(['Subject'])['Absence'].mean())
    df.sort_values(['Subject', 'Class', 'Id']).to_csv(
        os.path.join(CURR_DIR, 'output.csv'),
        index=False,
        encoding='utf-8'
    )
