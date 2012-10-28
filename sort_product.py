__author__ = 'Administrator'
# coding=cp936

from get_order_info import output_info, get_order_info, read_xml, get_order_id
import re

Specified_Order = (
    '03', 'B1', 'B9', '04', '09', '01',
    'L3', 'L4', 'L5', 'L8', '02', 'SWM',
    'SWN', 'SWS', 'HD', 'SD', 'B07', 'E',
    'PM001', 'PM00', 'B08', 'WB', 'B26', 'B32',
    'B25', 'B36', 'B41'
)

def sort_all_order_info(all_order_info):
    distinct_product_list = set(all_order_info)
    for product in distinct_product_list:
        quantity = all_order_info.count(product)
        product["Quantity"] = quantity
        output_info(product, 1)
        output_info("-----数量：%d" % (all_order_info.count(product)))
    #准备对distinct_product_list进行排序

    classified_product_list = {}
    for prefix in Specified_Order:
        classified_product_list[prefix] = []
        pattern = '^' + prefix
        for product in all_order_info:
            m = re.match(pattern, product["ProductNum"])
            if m:
                classified_product_list[prefix].append(product)
                all_order_info.remove(product)
        classified_product_list[prefix].sort(cmp=lambda x,y:cmp(x.get('ProductNum'), y.get('ProductNum')))

    output_info("-------------" * 10)
    output_info("排序结果：")
    for prefix in Specified_Order:
        for product in classified_product_list[prefix]:
            output_info(product, 1)
def get_all_order_info(all_order_id):
    all_order_info = []
    for id in all_order_id:
        s_order_info = get_order_info(id)
        for item in s_order_info:
            all_order_info.append(item)
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
    sort_all_order_info(all_order_info)
    output_info("-------------" * 10)

def main():
    while True:
        process()

if "__main__" == __name__:
    main()