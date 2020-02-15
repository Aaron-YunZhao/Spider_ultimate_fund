# Author: Aaron Zhao
# Email: aaron-yunzhao@outlook.com

import pandas as pd


def calc_aaron_ratio(input_df):
    # 计算列表中所有基金的三年汇报总和，三年标准差总和，三年晨星风险系数总和
    # 按照如下公式求得系数coeff，存入df新的一列，该coeff对列表中所有基金一致
    input_df = input_df.astype(
        {'return_3y': 'float', 'dev_3y': 'float', 'ms_risk_3y': 'float'})
    total_return_3y = input_df['return_3y'].sum(axis=0)
    total_dev_3y = input_df['dev_3y'].sum(axis=0)
    total_ms_risk_3y = input_df['ms_risk_3y'].sum(axis=0)
    coeff = total_return_3y / (total_dev_3y + total_ms_risk_3y)
    input_df['coeff'] = coeff

    # 利用coeff按照如下公式计算每支基金的新的ratio，存入df新的一列
    input_df.eval(
        'aaron_ratio = return_3y/coeff - dev_3y - ms_risk_3y',
        inplace=True)
    return input_df


if __name__ == '__main__':
    # 从csv读取基金列表至df
    csv_file = "2020-02-12-18-39_ms_fund_list_filter_mngr.csv"
    df = pd.read_csv(csv_file, low_memory=False)  # 防止弹出警告
    df = calc_aaron_ratio(df)
    print(df.head())
    df.to_csv(csv_file.split('.')[0] + r'_aaron.csv', index=False,
              encoding='utf_8_sig')
