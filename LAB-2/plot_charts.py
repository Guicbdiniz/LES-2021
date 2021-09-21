# Gráficos a serem plotados:
# 1.1) Número de estrelas / CBO
# 1.2) Número de estrelas / DIT
# 1.3) Número de estrelas / LCOM
#
# 2.1) LOC / CBO
# 2.2) LOC / DIT
# 2.3) LOC / LCOM
#
# 3.1) Número de releases / CBO
# 3.2) Número de releases / DIT
# 3.3) Número de releases / LCOM
#
# 4.1) Idade / CBO
# 4.2) Idade / DIT
# 4.3) Idade / LCOM

import logging
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

CHARTS_FOLDER_NAME = 'charts'
ANALYSED_DATA_CSV_FILENAME = 'analysed_data.csv'

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def plot_charts():
    df = pd.read_csv(ANALYSED_DATA_CSV_FILENAME)
    df = df.dropna()  # Drop null rows

    stars_cbo_chart = sns.regplot(x=df['stargazers'], y=df['cbo'])
    stars_cbo_chart.title.set_text('Stars / CBO')
    stars_cbo_chart.figure.savefig(f'{CHARTS_FOLDER_NAME}/stars_cbo_.png')
    plt.close('all')

    stars_dit_chart = sns.regplot(x=df["stargazers"], y=df["dit"])
    stars_dit_chart.title.set_text('Stars / DIT')
    stars_dit_chart.figure.savefig(f'{CHARTS_FOLDER_NAME}/stars_dit_.png')
    plt.close('all')

    stars_lcom_chart = sns.regplot(x=df["stargazers"], y=df["lcom"])
    stars_lcom_chart.title.set_text('Stars / LCOM')
    stars_lcom_chart.figure.savefig(f'{CHARTS_FOLDER_NAME}/stars_lcom_.png')
    plt.close('all')

    loc_cbo_chart = sns.regplot(x=df['loc'], y=df['cbo'])
    loc_cbo_chart.title.set_text('LOC / CBO')
    loc_cbo_chart.figure.savefig(f'{CHARTS_FOLDER_NAME}/loc_cbo_.png')
    plt.close('all')

    loc_dit_chart = sns.regplot(x=df['loc'], y=df['dit'])
    loc_dit_chart.title.set_text('LOC / DIT')
    loc_dit_chart.figure.savefig(f'{CHARTS_FOLDER_NAME}/loc_dit_.png')
    plt.close('all')

    loc_lcom_chart = sns.regplot(x=df['loc'], y=df['lcom'])
    loc_lcom_chart.title.set_text('LOC / LCOM')
    loc_lcom_chart.figure.savefig(f'{CHARTS_FOLDER_NAME}/loc_lcom_.png')
    plt.close('all')

    releases_cbo_chart = sns.regplot(x=df['releases'], y=df['cbo'])
    releases_cbo_chart.title.set_text('Releases / CBO')
    releases_cbo_chart.figure.savefig(f'{CHARTS_FOLDER_NAME}/releases_cbo_.png')
    plt.close('all')

    releases_dit_chart = sns.regplot(x=df['releases'], y=df['dit'])
    releases_dit_chart.title.set_text('Releases / DIT')
    releases_dit_chart.figure.savefig(f'{CHARTS_FOLDER_NAME}/releases_dit_.png')
    plt.close('all')

    releases_lcom_chart = sns.regplot(x=df['releases'], y=df['lcom'])
    releases_lcom_chart.title.set_text('Releases / LCOM')
    releases_lcom_chart.figure.savefig(f'{CHARTS_FOLDER_NAME}/releases_lcom_.png')
    plt.close('all')

    age_cbo_chart = sns.regplot(x=df['age'], y=df['cbo'])
    age_cbo_chart.title.set_text('Age / CBO')
    age_cbo_chart.figure.savefig(f'{CHARTS_FOLDER_NAME}/age_cbo_.png')
    plt.close('all')

    age_dit_chart = sns.regplot(x=df['age'], y=df['dit'])
    age_dit_chart.title.set_text('Age / DIT')
    age_dit_chart.figure.savefig(f'{CHARTS_FOLDER_NAME}/age_dit_.png')
    plt.close('all')

    age_lcom_chart = sns.regplot(x=df['age'], y=df['lcom'])
    age_lcom_chart.title.set_text('Age / LCOM')
    age_lcom_chart.figure.savefig(f'{CHARTS_FOLDER_NAME}/age_lcom_.png')
    plt.close('all')


if __name__ == '__main__':
    plot_charts()
