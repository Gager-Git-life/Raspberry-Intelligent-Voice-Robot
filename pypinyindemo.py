#coding:utf-8
import pypinyin
import sys

class Py_pinyin:

  def __init__(self):
    pass
  #不带声调
  def hp(self,word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
      s = s + ''.join(i) + " "
    return s

  #带声调
  def hp2(self,word):
    s = ''
    for i in pypinyin.pinyin(word):
      s = s + ' '.join(i) + " "
    return s



pytarget = Py_pinyin()
result = pytarget.hp(sys.argv[1].decode('utf-8'))
print(result)
"""
if __name__ == "__main__":
  print(hp(sys.argv[1].decode('utf-8')))
  print(hp2(sys.argv[1].decode('utf-8')))
"""
