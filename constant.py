from enum import Enum
from collections import OrderedDict
from copy import deepcopy

STATUS_CODE = {
    "PR-00000000" : "",
    "PR-00000001": "Bạn không thể thực hiện thao tác này! Vui lòng thử lại.",
    "PR-00000002" : "Bạn không có quyền truy cập chức năng này!",
    "PR-00000003" : "Sự cố dịch vụ! \nVui lòng đợi trong giây lát!",
    "PR-00000004" : "Không thể lấy dữ liệu!",
    "PR-00000005" : "Hình ảnh không được để trống!",

}

class Constants(object):
    """Container of constant"""

    __slots__ = ('__dict__')

    def __init__(self, **kwargs):

        if list(filter(lambda x: not x.isupper(), kwargs)):
            raise AttributeError('Constant name should be uppercase.')

        super(Constants, self).__setattr__(
            '__dict__',
            OrderedDict(map(lambda x: (x[0], deepcopy(x[1])), kwargs.items()))
        )

    def sort(self, key=None, reverse=False):
        super(Constants, self).__setattr__(
            '__dict__',
            OrderedDict(sorted(self.__dict__.items(), key=key, reverse=reverse))
        )

    def __getitem__(self, name):
        return self.__dict__[name]

    def __len__(self):
        return  len(self.__dict__)

    def __iter__(self):
        for name in self.__dict__:
            yield name

    def keys(self):
        return list(self)

    def __str__(self):
        return str(list(self))

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, str(self.__dict__))

    def __dir__(self):
        return list(self)

    def __setattr__(self, name, value):
        raise AttributeError("Immutable attribute")

    def __delattr__(*_):
        raise AttributeError("Immutable attribute")
    

