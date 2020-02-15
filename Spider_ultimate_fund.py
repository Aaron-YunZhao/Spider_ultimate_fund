# Title: Spider_ultimate_fund
# Author: Aaron Zhao
# Email: aaron-yunzhao@outlook.com

from Module1_get_ms_fund_list import get_ms_fund_list
from Module2_fund_filter import fund_filter
from Module3_get_fund_manager import get_fund_manager
from Module4_calc_aaron_ratio import calc_aaron_ratio
import time

df = get_ms_fund_list(10)  # 输入需要采集的晨星基金排行榜页数
df = fund_filter(df)  # 剔除不感兴趣的基金，如申购暂停，不知名基金公司等
df = get_fund_manager(df)  # 通过天天基金网抓取基金的经理，任期，和任期收益率
df = calc_aaron_ratio(df)  # 计算我的排名系数
# 输出csv到本地
now = time.strftime("%Y-%m-%d-%H-%M", time.localtime(time.time()))
df.to_csv(now + r'_ms_fund_list_ultimate.csv',
          index=False,
          encoding='utf_8_sig')
