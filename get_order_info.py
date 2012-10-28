__author__ = 'olly'
#coding:utf-8
import urllib
import urllib2
from xml.etree import ElementTree

def read_xml(order_info):
    order_info = order_info.replace("\">", "\"/>")
    get_response = ElementTree.fromstring(order_info)
    error_info = get_response.find("error")
    all_item = []
    if error_info.text == None:
        output_info("查询订单信息成功，详细信息如下：")
        for item in get_response.iter("Item"):
            output_info(item.attrib, 1)
            all_item.append(item.attrib)
        return all_item
    else:
        output_info("条形码不存在")
        return []

def check_order_id(order_id):
    if len(order_id) == 0:
        return False
    return True

def get_order_id():
    return raw_input("请输入订单号：")

def get_order_info(order_id):
    """
    输入订单号，获得订单的信息，返回解析后的字典
    """
    url = "http://top.xgw.so/getorderinfo.aspx?barcode=" + order_id
    try:
        order_info = urllib.urlopen(url)
    except:
        output_info("连接失败，请检查网络是否正常")
        return []
    if order_info.code == 200:
        return read_xml(order_info.read())
    else:
        output_info("code:%d" % order_info.code)
        return []

def output_info(info, type=0):
    """
    0 --- 字符串
    1 --- 产品信息
    """
    if type == 0:
        print info
    elif type == 1:
        print u"产品名称:%s 属性:%s 产品编号:%s 重量:%s 数量:%s" % (
            info["ProductName"], info["Property"], info["ProductNum"],
            info["Weight"], info["Quantity"]
            )

def get_barcode():
    return raw_input("扫描条形码：")

def check_barcode(barcode):
    return True

def get_product_info_by_barcode(barcode):
    return {'ProductName': u'北极绒 U凸款莫代尔男士内裤', 'Property': u'XL|灰色', 'ProductNum': 'B9801', 'Weight': '0.12', 'Quantity': '1'}

def get_product_info():
    output_info("开始扫描条形码，直接按回车结束：")
    local_prodocut_info = []
    while True:
        barcode = get_barcode()
        if len(barcode) == 0:
            return local_prodocut_info
        if not check_barcode(barcode):
            output_info("条形码不正确")
            continue
        else:
            product = get_product_info_by_barcode(barcode)
            if len(product) == 0:
                output_info("获得信息出错，请重试")
            else:
                output_info(product, 1)
                local_prodocut_info.append(product)
    return local_prodocut_info

def compare_info(order_info, local_prodocut_info):
    output_info("----------------------------------------------------------------")
    output_info("扫描的产品信息列表：")
    for l_item in local_prodocut_info:
        output_info(l_item, 1)
    output_info("----------------------------------------------------------------")
    output_info("订单中的产品列表：")
    for r_item in order_info:
        output_info(r_item, 1)
    output_info("----------------------------------------------------------------")
    output_info("开始进行匹配......")
    matched_items = []
    for l_item in local_prodocut_info:
        for r_item in order_info:
            if l_item["ProductName"] == r_item["ProductName"] and l_item["Property"] == r_item["Property"] and\
               l_item["ProductNum"] == r_item["ProductNum"] and l_item["Weight"] == r_item["Weight"]:
                matched_items.append(l_item)
                local_prodocut_info.remove(l_item)
                quantity = int(r_item["Quantity"])
                quantity = quantity - 1
                r_item["Quantity"] = str(quantity)
                if quantity == 0:
                    order_info.remove(r_item)
    output_info("结果：")
    if len(order_info) == 0:
        output_info("匹配成功！")
    else:
        output_info("不完全匹配，未匹配产品列表为：")
        for r_item in order_info:
            output_info(r_item, 1)
        output_info("----------------------------------------------------------------")

def process():
    order_id = get_order_id()
    if not check_order_id(order_id):
        output_info("订单号不正确")
        return False
    order_info = get_order_info(order_id)
    if len(order_info) == 0:
        return False
    local_prodocut_info = get_product_info()
    compare_info(order_info, local_prodocut_info)

def main():
    while True:
        process()

if "__main__" == __name__:
    main()

