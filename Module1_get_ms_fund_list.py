# Author: Aaron Zhao
# Email: aaron-yunzhao@outlook.com
# Ref: https://blog.csdn.net/weixin_41832414/article/details/83587950

import pandas as pd
import time
from bs4 import BeautifulSoup
import re
from selenium import webdriver


def get_ms_fund_list(total_page):
    html = 'http://cn.morningstar.com/fundselect/default.aspx'  # 晨星基金筛选首页
    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(html)

    fund_df = pd.DataFrame()  # 准备接受数据的DataFrame

    # 定义起始页码
    page_num = 1
    # 爬取所有三年晨星评级5星的基金，手动查看得知共10页
    while page_num <= total_page:

        # 初始页为快照页，获取页的源代码
        data = browser.page_source
        # 如果网页没加载完成，则再等待10秒
        if data is None:
            time.sleep(10)
            data = browser.page_source
        # 利用BeautifulSoup解析网页源代码
        bs = BeautifulSoup(data, 'lxml')
        class_list = ['gridItem', 'gridAlternateItem']  # 数据在这两个类下面

        # 列表用于存放爬取的数据
        code_list = []  # 基金代码
        name_list = []  # 基金名称
        fund_cat = []  # 基金分类
        ms_eval_3y = []  # 晨星评级（三年）
        ms_eval_5y = []  # 晨星评级（五年）
        fund_date = []  # 净值日期
        fund_value = []  # 单位净值
        fund_value_change = []  # 净值日变动
        return_curr_y = []  # 今年以来回报（%）

        # 取出所有类的信息，并保存到对应的列表里
        for i in range(len(class_list)):
            for tr in bs.find_all('tr', {'class': class_list[i]}):
                tds_text = tr.find_all('td', {'class': "msDataText"})
                # print(tds_text)
                # print(tds_text[0].find_all('a')[0].string)
                tds_nume = tr.find_all('td', {'class': "msDataNumeric"})
                code_list.append(tds_text[0].find_all('a')[0].string)
                name_list.append(tds_text[1].find_all('a')[0].string)
                fund_cat.append(tds_text[2].string)
                ms_eval_3y.append(
                    re.search(
                        r'\d',
                        tds_text[3].find_all('img')[0]['src']).group())
                ms_eval_5y.append(
                    re.search(
                        r'\d',
                        tds_text[4].find_all('img')[0]['src']).group())
                fund_date.append(tds_nume[0].string)
                fund_value.append(tds_nume[1].string)
                fund_value_change.append(tds_nume[2].string)
                return_curr_y.append(tds_nume[3].string)

        # 点击翻到业绩与风险页
        next_version = browser.find_element_by_link_text('业绩和风险')
        next_version.click()
        time.sleep(2)
        # 获取页的源代码
        data = browser.page_source
        # 如果网页没加载完成，则再等待10秒
        if data is None:
            time.sleep(10)
            data = browser.page_source
        # 利用BeautifulSoup解析网页源代码
        bs = BeautifulSoup(data, 'lxml')
        class_list = ['gridItem', 'gridAlternateItem']  # 数据在这两个类下面

        return_1d = []  # 1天回报（%）
        return_1w = []  # 1周回报（%）
        return_1m = []  # 1月回报（%）
        return_3m = []  # 3月回报（%）
        return_6m = []  # 6月回报（%）
        return_1y = []  # 1年回报（%）
        return_2y = []  # 2年回报（%）
        return_3y = []  # 3年回报（%）
        return_5y = []  # 5年回报（%）
        return_10y = []  # 10年回报（%）
        return_since_est = []  # 设立以来总回报（%）
        dev_3y = []  # 三年标准差
        ms_risk_3y = []  # 晨星三年风险系数

        for i in range(len(class_list)):
            for tr in bs.find_all('tr', {'class': class_list[i]}):
                tds_text = tr.find_all('td', {'class': "msDataText"})
                tds_nume = tr.find_all('td', {'class': "msDataNumeric"})
                return_1d.append(tds_nume[0].string)
                return_1w.append(tds_nume[1].string)
                return_1m.append(tds_nume[2].string)
                return_3m.append(tds_nume[3].string)
                return_6m.append(tds_nume[4].string)
                return_1y.append(tds_nume[5].string)
                return_2y.append(tds_nume[6].string)
                return_3y.append(tds_nume[7].string)
                return_5y.append(tds_nume[8].string)
                return_10y.append(tds_nume[9].string)
                return_since_est.append(tds_nume[10].string)
                dev_3y.append(tds_nume[11].string)
                ms_risk_3y.append(tds_nume[12].string)

        # 点击翻到投资组合页
        next_version = browser.find_element_by_link_text('投资组合')
        next_version.click()
        time.sleep(2)
        # 获取页的源代码
        data = browser.page_source
        # 如果网页没加载完成，则再等待10秒
        if data is None:
            time.sleep(10)
            data = browser.page_source
        # 利用BeautifulSoup解析网页源代码
        bs = BeautifulSoup(data, 'lxml')
        class_list = ['gridItem', 'gridAlternateItem']  # 数据在这两个类下面

        stock_ratio = []  # 股票仓位（%）
        bond_ratio = []  # 债券仓位（%）
        top10_stock_ratio = []  # 前十大持股（%）
        top10_bond_ratio = []  # 前十大债券（%）
        net_asset = []  # 净资产（亿元）

        for i in range(len(class_list)):
            for tr in bs.find_all('tr', {'class': class_list[i]}):
                tds_text = tr.find_all('td', {'class': "msDataText"})
                tds_nume = tr.find_all('td', {'class': "msDataNumeric"})
                stock_ratio.append(tds_nume[0].string)
                bond_ratio.append(tds_nume[1].string)
                top10_stock_ratio.append(tds_nume[2].string)
                top10_bond_ratio.append(tds_nume[3].string)
                net_asset.append(tds_nume[4].string)

        # 点击翻到购买信息页
        next_version = browser.find_element_by_link_text('购买信息')
        next_version.click()
        time.sleep(2)
        # 获取页的源代码
        data = browser.page_source
        # 如果网页没加载完成，则再等待10秒
        if data is None:
            time.sleep(10)
            data = browser.page_source
        # 利用BeautifulSoup解析网页源代码
        bs = BeautifulSoup(data, 'lxml')
        class_list = ['gridItem', 'gridAlternateItem']  # 数据在这两个类下面

        est_date = []  # 成立日期
        buy_cond = []  # 申购状态
        redeem_cond = []  # 赎回状态
        min_buy = []  # 最小投资额（元）
        front_fee = []  # 前端收费（%）
        back_fee = []  # 后端收费（%）
        redeem_fee = []  # 赎回费（%）
        admin_fee = []  # 管理费（%）
        trust_fee = []  # 托管费（%）
        sell_service_fee = []  # 销售服务费（%）

        for i in range(len(class_list)):
            for tr in bs.find_all('tr', {'class': class_list[i]}):
                tds_text = tr.find_all('td', {'class': "msDataText"})
                tds_nume = tr.find_all('td', {'class': "msDataNumeric"})
                est_date.append(tds_nume[0].string)
                buy_cond.append(tds_nume[1].string)
                redeem_cond.append(tds_nume[2].string)
                min_buy.append(tds_nume[3].string)
                front_fee.append(tds_nume[4].string)
                back_fee.append(tds_nume[5].string)
                redeem_fee.append(tds_nume[6].string)
                admin_fee.append(tds_nume[7].string)
                trust_fee.append(tds_nume[8].string)
                sell_service_fee.append(tds_nume[9].string)

        # 当前页读取的25支基金所有数据
        fund_df_page = pd.DataFrame(
            dict(
                fund_code=code_list,
                fund_name=name_list,
                fund_cat=fund_cat,
                ms_eval_3y=ms_eval_3y,
                ms_eval_5y=ms_eval_5y,
                fund_date=fund_date,
                fund_value=fund_value,
                fund_value_change=fund_value_change,
                return_y_pct=return_curr_y,
                return_1d=return_1d,
                return_1w=return_1w,
                return_1m=return_1m,
                return_3m=return_3m,
                return_6m=return_6m,
                return_1y=return_1y,
                return_2y=return_2y,
                return_3y=return_3y,
                return_5y=return_5y,
                return_10y=return_10y,
                return_since_est=return_since_est,
                dev_3y=dev_3y,
                ms_risk_3y=ms_risk_3y,
                stock_ratio=stock_ratio,
                bond_ratio=bond_ratio,
                top10_stock_ratio=top10_stock_ratio,
                top10_bond_ratio=top10_bond_ratio,
                net_asset=net_asset,
                est_date=est_date,
                buy_cond=buy_cond,
                redeem_cond=redeem_cond,
                min_buy=min_buy,
                front_fee=front_fee,
                back_fee=back_fee,
                redeem_fee=redeem_fee,
                admin_fee=admin_fee,
                trust_fee=trust_fee,
                sell_service_fee=sell_service_fee))
        # 当前页基金数据加到已得到的所有基金表中
        fund_df = fund_df.append(fund_df_page, ignore_index=True)

        # 翻下一页前回到快照页面
        next_version = browser.find_element_by_link_text('快照')
        next_version.click()
        time.sleep(2)
        # 找到换页按钮然后点击
        next_page = browser.find_element_by_link_text('>')
        next_page.click()
        page_num += 1
        time.sleep(2)
    return fund_df


if __name__ == '__main__':
    df = get_ms_fund_list(1)
    now = time.strftime("%Y-%m-%d-%H-%M", time.localtime(time.time()))
    df.to_csv(now + r'_ms_fund_list.csv',
              index=False,
              encoding='utf_8_sig')
    print(df.head())
