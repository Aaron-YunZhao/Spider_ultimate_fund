# Author: Aaron Zhao
# Email: aaron-yunzhao@outlook.com

import pandas as pd

# 格式设置在pycharm里print时更好地显示dataFrame
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)


def fund_filter(filter_df):
    # 条件1： 资产大于5亿
    filter_df = filter_df[filter_df.net_asset.map(lambda x:float(x)) > 5]
    # 条件2： 申购条件开放
    filter_df = filter_df[filter_df.buy_cond == '开放']
    # 条件3： 出自以下top基金公司
    filter_df = filter_df[filter_df.fund_name.str.contains(
        '易方达|中银|博时|华夏|汇添富|南方|广发|嘉实|招商|富国|工银瑞信|鹏华|建信|华安|兴全|民生加银|农银汇理|银华|交银施罗德|平安|中欧|国泰')]
    filter_df = filter_df.reset_index(drop=True)
    return filter_df


if __name__ == '__main__':
    # 从csv读取基金列表至df
    csv_file = "2020-02-12-20-45_ms_fund_list.csv"
    df = pd.read_csv(csv_file, low_memory=False)  # 防止弹出警告
    df = fund_filter(df)

    df.to_csv(csv_file.split('.')[0] + r'_filter.csv', index=False,
              encoding='utf_8_sig')
    print(df.head())
