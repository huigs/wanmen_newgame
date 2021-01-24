# encoding=utf-8
import pandas as pd
import requests
from lxml import etree
import re
import collections
 
 
def fund_code_name():
    """ 筛选天天基金，6千多基金机构的，最近一周收益率排在前50强基金"""
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Referer': 'http://fund.eastmoney.com/data/fundranking.html',
        'Cookie': '_adsame_fullscreen_18186=1; st_si=32030334066413; st_asi=delete; qgqp_b_id=a1b6b8fb433276ec83425dad5fc57f93; ASP.NET_SessionId=mgqx045pqz225l34wobrpwqm; _adsame_fullscreen_18503=1; EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; FundWebTradeUserInfo=JTdCJTIyQ3VzdG9tZXJObyUyMjolMjIlMjIsJTIyQ3VzdG9tZXJOYW1lJTIyOiUyMiUyMiwlMjJWaXBMZXZlbCUyMjolMjIlMjIsJTIyTFRva2VuJTIyOiUyMiUyMiwlMjJJc1Zpc2l0b3IlMjI6JTIyJTIyLCUyMlJpc2slMjI6JTIyJTIyJTdE; EMFUND0=null; EMFUND7=01-04%2021%3A56%3A23@%23%24%u5357%u65B9%u519B%u5DE5%u6539%u9769%u7075%u6D3B%u914D%u7F6E%u6DF7%u5408@%23%24004224; EMFUND8=01-04%2022%3A00%3A32@%23%24%u5927%u6210%u9AD8%u65B0%u6280%u672F%u4EA7%u4E1A%u80A1%u7968C@%23%24011066; EMFUND9=01-04 22:00:53@#$%u91D1%u4FE1%u6838%u5FC3%u7ADE%u4E89%u529B%u6DF7%u5408@%23%24009317; st_pvi=85681793104328; st_sp=2021-01-04%2021%3A51%3A43; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=17; st_psi=20210104222201364-0-3677672526'
    }
    #url = 'http://fund.eastmoney.com/data/fundranking.html#tall;c0;r;szzf;pn50;ddesc;qsd20200104;qed20210104;qdii;zq;gg;gzbd;gzfs;bbzt;sfbb'
    
    response = requests.get(
        url='http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=6yzf&st=desc&sd=2020-01-24&ed=2021-01-24&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.12242508929918916', headers=header)
             #http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=zzf&st=desc&sd=2020-01-04&ed=2021-01-04&qdii=&tabSubtype=,,,,,&pi=1&pn=10000&dx=1&v=0.7609006409053407
             #http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=6yzf&st=desc&sd=2020-01-24&ed=2021-01-24&qdii=&tabSubtype=,,,,,&pi=1&pn=50&dx=1&v=0.12242508929918916      
    #response = requests.get(url)
    text = response.text
    data = text.split('=')[1]
    #print(data)
    compile_data = re.findall("{datas:\\[(.*)\\],allRecords", str(data))[0]
    strip_data = str(compile_data).strip('[').strip(']')
    replace_quta = strip_data.replace('"', "")
    quota_arrays = replace_quta.split(",")
    intervals = [[i * 25, (i + 1) * 25] for i in range(258)]
    narrays = []
    for k in intervals:
        start, end = k[0], k[1]
        line = quota_arrays[start:end]
        narrays.append(line)
    header = ["基金代码", "基金简称", "基金条码", "日期",
              "单位净值", "累计净值", "日增长率", "近1周增长率", "近1月增长率", "近3月", "近半年", "近1年", "近2年", "近3年",
              "今年来", "成立来", "其他1", "其他2", "其他3", "其他4", "其他5", "其他6", "其他7", "其他8", "其他9"]
    df = pd.DataFrame(narrays, columns=header)
    df_part = df[["基金代码", "基金简称", "日期",
                  "单位净值", "累计净值", "日增长率", "近1周增长率", "近1月增长率", "近3月", "近半年"]]
    listnum = 50
    df_tmp = df_part.sort_values(by=["近1周增长率"], ascending=False, axis=0)
    rank_fund_code = df_tmp.head(listnum)["基金代码"]
    fund_codes_list = rank_fund_code.values.tolist()
    print("前50强基金：", fund_codes_list)
    df_tmp.head(listnum).to_csv("./本季度前50强基金收益.csv", encoding="utf_8_sig")
    return fund_codes_list
 
 
def get_one_fund_stocks(fund_code):
    """根据基金码,获取每一支基金的最新一季度所有持仓股票池前10支股票"""
    url = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code={}&topline=10&year=&month=&rt=0.5032668912422176".format(
        fund_code)
    head = {
        "Cookie": "EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; EMFUND8=null; EMFUND0=null; st_si=44023331838789; st_asi=delete; EMFUND9=08-16 22:04:25@#$%u4E07%u5BB6%u65B0%u5229%u7075%u6D3B%u914D%u7F6E%u6DF7%u5408@%23%24519191; ASP.NET_SessionId=45qdofapdlm1hlgxapxuxhe1; st_pvi=87492384111747; st_sp=2020-08-16%2000%3A05%3A17; st_inirUrl=http%3A%2F%2Ffund.eastmoney.com%2Fdata%2Ffundranking.html; st_sn=12; st_psi=2020081622103685-0-6169905557"
        ,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"}
 
    response = requests.get(url, headers=head)
    text = response.text  # html subsitue text
    div = re.findall('content:\\"(.*)\\",arryear', text)[0]
    html_body = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>test</title></head><body>%s</body></html>' % (
        div)
    html = etree.HTML(html_body)
    stock_info = html.xpath('//div[1]/div/table/tbody/tr/td/a')
    stock_money = html.xpath('//div[1]/div/table/tbody/tr/td')
    stock_one_fund = []
    for stock in stock_info:
        if stock.text and stock.text.isdigit():
            stock_one_fund.append(stock.text)
    if len(stock_one_fund)>1:
        print("基金代码：{}".format(fund_code), "基金持有前10股票池", stock_one_fund)
    return stock_one_fund  # can return empty list
 
 
def static_best_stock(rank=20):
    """ 统计收益最佳前50机构共同持有股票代码情况,修改rank数量可调整展示股票排名数目"""
    rank_codes = fund_code_name()
    stocks_array = []
    for index, code in enumerate(rank_codes):
        if index < 1:
            print("<" * 30 + "FBI WARNING近1周收益最高基金的排名高到低排序以及股票池情况" + ">" * 30)
        stocks = get_one_fund_stocks(code)
        if len(stocks) > 1 and stocks:
            stocks_array.extend(stocks)
    count_each_stock = collections.Counter(stocks_array)
    print("<" * 30 + "FBI WARNING,{}".format(static_best_stock.__doc__) + ">" * 30)
    print("#" * 30 + "本季度基金机构共同持有股票数目排行前{}股票代码情况".format(rank) + "#" * 30)
    df=pd.DataFrame.from_dict(count_each_stock,orient='index',columns=["持有该股机构数目"])
    df=df.reset_index().rename(columns={"index":"股票代码"})
    # for k, v in count_each_stock.items():
    #     print("股票代码: ", k, "持有该股票机构数量: ", v)
    df=df.sort_values(by="持有该股机构数目",ascending=False)
    print(df.head(rank))
 
 
if __name__ == '__main__':
    static_best_stock()