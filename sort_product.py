__author__ = 'Administrator'
# coding=cp936

from get_order_info import output_info, get_order_info, read_xml, get_order_id
import re
from GenPDF import GenPDF

Specified_Order = (
    '03', 'B1', 'B9', '04', '09', '01',
    'L3', 'L4', 'L5', 'L8', '02', 'SWM',
    'SWN', 'SWS', 'HD', 'SD', 'B07', 'E',
    'PM00111', 'PM00121', 'B08', 'WB', 'B26', 'B32',
    'B25', 'B36', 'B41'
    )

Bag_Seqence = (
    'A1', 'A2', 'A3', 'A4',
    'B1', 'B2', 'B3', 'B4',
    'C1', 'C2', 'C3', 'C4',
    'D1', 'D2', 'D3', 'D4',
    'A5', 'A6', 'A7', 'A8',
    'B5', 'B6', 'B7', 'B8',
    'C5', 'C6', 'C7', 'C8',
    'D5', 'D6', 'D7', 'D8'
    )

FILENAME = "Result.pdf"

def distributed_products(classified_product_list, all_order_info):
    output_info("-----分配结果：")
    for p_left in classified_product_list:
        temp = []
        distribution_str = ''
        for p_right in all_order_info:
            if p_right["ProductNum"] == p_left["ProductNum"] and \
                p_right["ProductName"] == p_left["ProductName"] and \
                p_right["Property"] == p_left["Property"]:
                temp.append(p_right)

        for item in temp:
            distribution_str = distribution_str + '%s->%s,' % (item["Quantity"], item["Bag"])
        #去掉最后一个多余的逗号
        distribution_str = distribution_str[0:-1]
        p_left["DistributionStr"] = distribution_str
        output_info('%s:%s:%s' % (p_left["ProductNum"], p_left["Property"], p_left["DistributionStr"]))
def sort_all_order_info(all_order_info):
    #获得不含重复元素的订单序列
    distinct_product_list = []
    #比较时不看数量
    import copy
    all_order_info_copy = copy.deepcopy(all_order_info)
    all_order_info_copy_distinct = []
    for item in all_order_info_copy:
        del item["Quantity"]
    for x in all_order_info_copy:
        if x not in all_order_info_copy_distinct:
            all_order_info_copy_distinct.append(x)

    for x in all_order_info_copy_distinct:
        x["Quantity"] = 0

    for y in all_order_info_copy_distinct:
        for x in all_order_info:
            if x["ProductName"] == y["ProductName"] and x["Property"] == y["Property"] and \
                x["Weight"] == y["Weight"] and x["ProductNum"] == y["ProductNum"]:
                y["Quantity"] = y["Quantity"] + int(x["Quantity"])

    distinct_product_list = all_order_info_copy_distinct

    distributed_products(distinct_product_list, all_order_info)

    classified_product_list = {}
    for prefix in Specified_Order:
        classified_product_list[prefix] = []
        pattern = '^' + prefix
        for product in distinct_product_list:
            m = re.match(pattern, product["ProductNum"])
            if m:
                classified_product_list[prefix].append(product)
                #distinct_product_list.remove(product)
        classified_product_list[prefix].sort(cmp=lambda x,y:cmp(x.get('ProductNum'), y.get('ProductNum')))

    output_info("-------------" * 10)
    output_info("排序结果：")
    for prefix in Specified_Order:
        for product in classified_product_list[prefix]:
            output_info(product, 1)
    return classified_product_list
def get_all_order_info(all_order_id):
    all_order_info = []
    loop = 0
    for id in all_order_id:
        s_order_info = get_order_info(id)
        for item in s_order_info:
            item["Bag"] = Bag_Seqence[loop]
            all_order_info.append(item)
        loop = loop + 1
    return  all_order_info

def get_all_order_id():
    #return ['2200163758','2200163763','2200163768','2200163765','2200163767','2200163719','2200163670','2200163680']
    output_info("请逐条输入订单号，直接按回车结束")
    all_order_id = []
    while True:
        order_id = get_order_id().strip()
        if len(order_id) == 0:
            output_info(all_order_id)
            return  all_order_id
        else:
            all_order_id.append(order_id)

def process():
    all_order_id = get_all_order_id()
    all_order_info = get_all_order_info(all_order_id)
    classified_product_list = sort_all_order_info(all_order_info)
    output_info("-------------" * 10)
    output_info('开始生成清单的PDF文件......')
    try:
        GenPDF(FILENAME, classified_product_list, Specified_Order)
    except IOError, e:
        output_info(FILENAME + '已经被打开，请关闭后重试！')
    else:
        output_info('清单已生成在当前目录' + FILENAME + '文件中，请打开查看')
    output_info("-------------" * 10)

def main():
    while True:
        process()

if "__main__" == __name__:
    main()