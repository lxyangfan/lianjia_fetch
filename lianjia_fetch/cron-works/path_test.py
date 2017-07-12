#encoding:utf-8
import os

print "__file__ :", __file__
print "abspath(__file__):", os.path.abspath(__file__)
print "dirname( abs ( __file__:", os.path.dirname(os.path.abspath(__file__))
print os.path.pardir
print os.path.join(os.path.dirname(__file__),os.path.pardir)
print os.path.abspath(os.path.join(os.path.dirname("__file__"),os.path.pardir))
