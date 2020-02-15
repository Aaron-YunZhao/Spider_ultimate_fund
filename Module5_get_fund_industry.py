# Author: Aaron Zhao
# Email: aaron-yunzhao@outlook.com
# Ref: https://www.cnblogs.com/HuZihu/p/10201445.html

import pandas as pd
import re
from selenium import webdriver


def get_html(url):
    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    html = browser.page_source
    # time.sleep(2)
    # if html is None:  # 2秒后如无数据再等5秒，再无数据输出error
    #     time.sleep(5)
    #     html = browser.page_source
    #     if html is None:
    #         print('Error, no response from the target URL after 7 seconds.')
    return html


def get_fund_industry(input_df):
    fund_df = input_df
    ind_df = pd.DataFrame()

    # 先把fund_code转换成str型，再只取小数点（如有）之前的位数，后用zfill()补充确失的0位至整体6位
    fund_df = fund_df.astype({'fund_code': 'str'})
    for i in fund_df.index:
        fund_code = fund_df.loc[i, 'fund_code'].split('.')[0].zfill(6)
        url = 'http://fundf10.eastmoney.com/hytz_' + fund_code + '.html'  # 天天基金网行业配置页
        data = get_html(url)
        pattern = re.compile(
            '<label class="left"><span>截止.*?，(.*?)占净值比为(.*?)%，排名第一。</span></label>',
            re.S)
        result = re.findall(pattern, data)
        print(result)
        if not result:
            ind_df_page = pd.DataFrame([['null', 'null']])
        else:
            ind_df_page = pd.DataFrame({result[0]})

        ind_df = ind_df.append(ind_df_page, ignore_index=True)
    ind_df.columns = ['top_industry', 'top_industry_ratio']
    output_df = pd.concat([fund_df, ind_df, ], axis=1)
    return output_df


if __name__ == '__main__':
    # 从csv读取基金列表至df
    csv_file = "2020-02-12-19-33_ms_fund_list_ultimate.csv"
    df = pd.read_csv(csv_file, low_memory=False)  # 防止弹出警告
    df = get_fund_industry(df)
    print(df.head())
    df.to_csv(csv_file.split('.')[0] + r'_ind.csv', index=False,
              encoding='utf_8_sig')