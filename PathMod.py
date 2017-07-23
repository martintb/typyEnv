from __future__ import print_function

class PathMod(object):
  def __init__(self,*args,**kwargs):
    self.contains = kwargs.get('contains',list())

    if all(k in kwargs for k in ('name','action','value')):
      self.name   = kwargs['name']
      self.action = kwargs['action']
      self.value  = kwargs['value'].replace(' ','_') #for sanitizing malicious commands in the paths
    else:
      print('==> Error! Can\'t build PathMod with given args:')
      for k,v in kwargs.items():
        print('{}: {}',format(k,v))
      exit(1)
  def __str__(self):
    return '<PathMod name:{} action:{} value:{}>'.format(self.name,self.action,self.value)
  def __repr__(self):
    return self.__str__()
