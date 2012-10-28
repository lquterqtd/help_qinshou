__author__ = 'Administrator'
#coding:cp936
from distutils.core import setup
import py2exe
options = {
    "py2exe":
        {
            "bundle_files" : 1
        }
}
setup(
    options=options,
    console=["get_order_info.py"]
)