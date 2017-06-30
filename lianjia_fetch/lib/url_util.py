#! -*- encoding:utf-8 -*-

from urllib import urlencode, quote


def url_encode_from_dict(dic):
    if type(dic) != dict:
        raise TypeError("输入参数不是dict类型！")
    n_dic = {}
    for k, v in dic.items():
        if type(v) == unicode:
            n_dic[k] = v.encode("gbk")
    return urlencode(n_dic)


def url_encode_unicode(uni):
    n_str = u""
    if type(uni) == unicode:
        n_str = uni.encode("gbk")
    return quote(n_str)


if __name__ == "__main__":
    print url_encode_from_dict({"k1": u"张家辉", "k2": "张家辉"})
    print url_encode_unicode("上海浦东")
