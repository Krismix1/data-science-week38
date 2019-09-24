import numpy as np
import matplotlib.pyplot as plt

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



def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        width = rect.get_width()
        plt.annotate('{0:.2f}'.format(float(width)),
                    xy=(width, rect.get_y() + rect.get_height() / 2),
                    xytext=(3, 0),  # 3 points horizontal offset
                    textcoords="offset points",
                    ha='center', va='bottom')