__author__ = 'olly'
#coding:cp936
import urllib
import urllib2
from xml.etree import ElementTree

def read_xml(order_info, order_id):
    order_info = order_info.replace("\">", "\"/>")
    get_response = ElementTree.fromstring(order_info)
    error_info = get_response.find("error")
    all_item = []
    if error_info.text == None:
        output_info("��ѯ����%s��Ϣ�ɹ�����ϸ��Ϣ���£�" % order_id)
        for item in get_response.iter("Item"):
            output_info(item.attrib, 1)
            all_item.append(item.attrib)
        return all_item
    else:
        output_info("�����벻����")
        return []

def check_order_id(order_id):
    if len(order_id) == 0:
        return False
    return True

def get_order_id():
    return raw_input("�����붩���ţ�")

def get_order_info(order_id):
    """
    ���붩���ţ���ö�������Ϣ�����ؽ�������ֵ�
    """
    url = "http://top.xgw.so/getorderinfo.aspx?barcode=" + order_id
    try:
        order_info = urllib.urlopen(url)
    except:
        output_info("����ʧ�ܣ����������Ƿ�����")
        return []
    if order_info.code == 200:
        return read_xml(order_info.read(), order_id)
    else:
        output_info("��ѯ������Ϣʧ��")
        return []

def output_info(info, type=0):
    """
    0 --- �ַ���
    1 --- ��Ʒ��Ϣ
    """
    if type == 0:
        print info
    elif type == 1:
        print u"��Ʒ����:%-50s ����:%-30s ��Ʒ���:%-20s ����:%-8s ����:%-5s" % (
            info["ProductName"], info["Property"], info["ProductNum"],
            info["Weight"], info["Quantity"]
            )

def get_barcode():
    return raw_input("ɨ�������룺")

def check_barcode(barcode):
    return True

def get_product_info_by_barcode(barcode):
    return {'ProductName': u'������ U͹��Ī������ʿ�ڿ�', 'Property': u'XL|��ɫ', 'ProductNum': 'B9801', 'Weight': '0.12', 'Quantity': '1'}

def get_product_info():
    output_info("��ʼɨ�������룬ֱ�Ӱ��س�������")
    local_prodocut_info = []
    while True:
        barcode = get_barcode()
        if len(barcode) == 0:
            return local_prodocut_info
        if not check_barcode(barcode):
            output_info("�����벻��ȷ")
            continue
        else:
            product = get_product_info_by_barcode(barcode)
            if len(product) == 0:
                output_info("�����Ϣ����������")
            else:
                output_info(product, 1)
                local_prodocut_info.append(product)
    return local_prodocut_info

def compare_info(order_info, local_prodocut_info):
    output_info("----------------------------------------------------------------")
    output_info("ɨ��Ĳ�Ʒ��Ϣ�б�")
    for l_item in local_prodocut_info:
        output_info(l_item, 1)
    output_info("----------------------------------------------------------------")
    output_info("�����еĲ�Ʒ�б�")
    for r_item in order_info:
        output_info(r_item, 1)
    output_info("----------------------------------------------------------------")
    output_info("��ʼ����ƥ��......")
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
    output_info("�����")
    if len(order_info) == 0:
        output_info("ƥ��ɹ���")
    else:
        output_info("����ȫƥ�䣬δƥ���Ʒ�б�Ϊ��")
        for r_item in order_info:
            output_info(r_item, 1)
        output_info("----------------------------------------------------------------")

def process():
    order_id = get_order_id()
    if not check_order_id(order_id):
        output_info("�����Ų���ȷ")
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

