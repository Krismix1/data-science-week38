# pylint: disable=C0111,W0105
import os
import numpy as np
import matplotlib.pyplot as plt
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
    # Compute all indices except the selected index
    indices_to_drop = set(range(0, max_subjects)) - {index}

    template_columns = ['Subject', 'Absence']
    columns_to_drop = [
        f'{col}.{idx}'
        for idx in indices_to_drop
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


# noinspection PyShadowingNames
def total_absence_hist(df, plot):
    bins = [i * 10 for i in range(0, 12)] # from 0% to 100%
    absence = np.array(df['Total Absence'])
    plot.hist(absence, bins=bins, align='left', histtype='bar')
    plot.set_xticks(bins)

    plot.set_xlabel('Absence, %')
    plot.set_ylabel('Frequency')
    plot.set_title('Total Class Absence Distribution')


if __name__ == '__main__':
    # Get an absolute to the data file, OS independent
    CURR_DIR = os.path.dirname(os.path.realpath(__file__))
    DATA_FILE = os.path.join(CURR_DIR, 'stud-stat-anonymous.csv')
    # Maximum number of subjects per row of a student
    MAX_SUBJECTS = 4
    subplot = plt.subplot(2, 1, 1)

    # read the CSV file into a DataFrame
    df = pandas.read_csv(DATA_FILE)
    # Drop the first unlabeled column
    df = df.drop(columns=['Unnamed: 0'])

    # Cast all columns with percentage values to floats
    df['Total Absence'] = df['Total Absence'].map(percentage_remap)
    total_absence_hist(df, subplot)

    total_absence_mean = df['Total Absence'].mean()
    total_absence_median = df['Total Absence'].median()
    # Mean Total Absence per Class
    total_absence_mean_per_class = df.groupby(['Class'])['Total Absence'].mean()

    # Recreate the data frame, with the new structure
    # This is needed to make sure that we don't have extra
    # rows from the initial structure
    df = pandas.DataFrame().append([
        keep_only_subject(df, 0, MAX_SUBJECTS),
        keep_only_subject(df, 1, MAX_SUBJECTS),
        keep_only_subject(df, 2, MAX_SUBJECTS),
        keep_only_subject(df, 3, MAX_SUBJECTS)
    ], ignore_index=True).drop(columns=['Total Absence'])

    df = df.dropna()  # drop rows that don't have a subject/absence value
    df['Absence'] = df['Absence'].map(percentage_remap)

    # Mean absence per subject
    mean_per_subject = df.groupby(['Subject'])['Absence'].mean().sort_values()
    most_skipped_subjects = ['Big Data']  # list(mean_per_subject.index)[-3:]

    # for each subject
    # select all rows that have Subject=subject
    # group those rows by the class
    # count the rows for each group
    # display the ratio of group/total
    for subject in most_skipped_subjects:
        students = df.loc[df['Subject'] == subject]
        per_class = students.groupby(['Class'])['Class'].agg(['count']) \
            .rename(columns={'count': 'Student count'})

        slices = per_class['Student count']
        activities = list(per_class.index)
        # plt.pie(slices,
        #     labels=activities,
        #     # explode=(0, 0, 0.2, 0),
        #     autopct='%1.1f%%'
        # )

        # axes = per_class.plot.bar()
        # axes.set_title(subject)

    # axes = mean_per_subject.plot.bar(x='Subject', y='Absence')
    # axes.set_xlabel('Subjects')
    # axes.set_ylabel('Absence, %')
    plt.show()

    # df.sort_values(['Subject', 'Class', 'Id']).to_csv(
    #     os.path.join(CURR_DIR, 'output.csv'),
    #     index=False,
    #     encoding='utf-8'
    # )
