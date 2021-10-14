import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def main():
    df = pd.read_csv('analysed_data.csv')
    df = df.dropna()

    # CBO
    cbo_mean = df['cbo'].mean()
    cbo_median = df['cbo'].median()
    cbo_std = df['cbo'].std()

    logger.info(f'CBO values:\nMean: {cbo_mean}\nMedian: {cbo_median}\nStandard Deviation: {cbo_std}')

    # DIT
    dit_mean = df['dit'].mean()
    dit_median = df['dit'].median()
    dit_std = df['dit'].std()

    logger.info(f'DIT values:\nMean: {dit_mean}\nMedian: {dit_median}\nStandard Deviation: {dit_std}')

    # LCOM
    lcom_mean = df['lcom'].mean()
    lcom_median = df['lcom'].median()
    lcom_std = df['lcom'].std()

    logger.info(f'LCOM values:\nMean: {lcom_mean}\nMedian: {lcom_median}\nStandard Deviation: {lcom_std}')


if __name__ == '__main__':
    main()
