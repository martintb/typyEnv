from OrderedSet import OrderedSet

class Path(object):
  def __init__(self,path_str,name,sep=':'):
    if path_str is None:
      self.path_set = OrderedSet()
    else:
      self.path_set = OrderedSet(path_str.split(sep))

    #remove empty values
    for val in [' ','']:
      try:
        self.path_set.remove(val)
      except KeyError:
        pass
        
    self.num = len(self.path_set)
    self.sep = sep
    self.name = name.replace(' ','_') #do a bit of sanitization on the path name
  def __str__(self):
    return '<Path name:{} sep:\"{}\" num:{}>'.format(self.name,self.sep,self.num)
  def __repr__(self):
    return self.__str__()
  def join(self):
    return self.sep.join(self.path_set)
  def append(self,path):
    path_list = list(self.path_set)
    path_list.append(path)
    self.path_set = OrderedSet(path_list)
  def prepend(self,path):
    path_list = list(self.path_set)
    path_list.insert(0,path)
    self.path_set = OrderedSet(path_list)
  def remove(self,path):
    try:
      self.path_set.remove(path)
    except KeyError:
      print '.:: Not Found! Skipping removal of {} from {}'.format(path,self.name)
  def modify(self, mod,action=None):
    if not (mod.__class__.__name__ == "PathMod"):
      print '.:: Error! Only PathMod objects should be passed to Path.add()'
      print 'Argument Type:',mod.__class__.__name__
      exit(1)
    if action is None:
      action = getattr(self,mod.action,None)
    else:
      action = getattr(self,action,None)

    if action is None:
      print '.:: Requested action not implemented!'
      print 'Requested Action:',action
      print 'PathMod Obj:',mod
      exit(1)
    action(mod.value)

