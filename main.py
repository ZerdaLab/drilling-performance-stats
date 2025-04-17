from utils import ( 
    read_dh_las,
    read_runs_data,
    read_formation_data,
)
from charts import (
    basic_box_plot,
    boxplot_split_by_runs,
    boxplot_by_runs_and_formations,
)


# USER SETS TO TRUE WHICHEVER PLOT THEY WANT TO SEE
NO_SPLIT = False
SPLIT_ONLY_BY_RUN = False
SPLIT_BY_RUN_AND_FORMATION = True

# SET CHANNEL NAME
CHANNEL_NAME = 'OBH'



if __name__ == "__main__":
    # Read data
    dh_df = read_dh_las()
    runs_df = read_runs_data()
    forms_df = read_formation_data()

    if NO_SPLIT:
        basic_box_plot(dh_df, target_column=CHANNEL_NAME, color='#1f77b4')
    elif SPLIT_ONLY_BY_RUN:
        boxplot_split_by_runs(dh_df, runs_df, target_column=CHANNEL_NAME)
    elif SPLIT_BY_RUN_AND_FORMATION:
        boxplot_by_runs_and_formations(dh_df, runs_df, forms_df, target_column=CHANNEL_NAME)

