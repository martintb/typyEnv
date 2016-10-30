from typyEnv.PathMod import PathMod
import json
import os

class Package(object):
  def __init__(self,base_path,pkg_name):
    self.base_path = base_path
    self.pkg_name = pkg_name
    self.fname = os.path.join(base_path,pkg_name)+'.json'
    self.std_paths = ['bin','include','lib']
    self.std_paths_dict = {
                            'bin':      {'dir':'bin'      ,'name':'PATH'},
                            'include':  {'dir':'include'  ,'name':'CPATH',            'contains':['headers']},
                            'lib':      {'dir':'lib'      ,'name':'LIBRARY_PATH',     'contains':['ldlibraries']},
                            'ldlib':    {'dir':'lib'      ,'name':'LD_LIBRARY_PATH',  'contains':['libraries']},
                            'python':   {'dir':'pylib'    ,'name':'PYTHONPATH'},
                          }
    self.action='prepend'
    self.loaded=False
    self.version=None
    self.path_mods=[]
    self.name=None
    self.dependencies=[]
  def __str__(self):
    if self.loaded:
      return '<Package name:{} version:{}, num_mods:{}, paths:{}>'.format(self.name,self.version,self.num_mods,self.modded_paths)
    else:
      return '<Package name:{} loaded:{}>'.format(self.name,self.action,self.value)
  def __repr__(self):
    return self.__str__()
  def read(self,version=None):
    with open(self.fname,'r') as f:
      pkg = json.load(f)

    # process info block and add to self
    info = pkg.get('info',{})
    for k,v in info.items():
      setattr(self,k,v)

    # process defaults and add them to self
    defaults = pkg.get('defaults',{})
    for k,v in defaults.items():
      setattr(self,k,v)

    #If given store version passed by user. 
    if version is not None:
      self.version = version

    # process version specified in default or locally
    if self.version is not None:
      try:
        vpkg = pkg['versions'][self.version]
      except KeyError:
        print '.:: Error! Requested version not found in json for package!'
        print 'Package:',self.fname
        print 'Version:',self.version
        exit(1)

      for k,v in vpkg.items():
        if k=='path_mods':
          self.path_mods.extend([PathMod(**pd) for pd in v])
        elif k=='dependencies':
          if k not in self.dependencies:
            self.dependencies.extend(v)
        else:
          setattr(self,k,v)
    else:
      print '.:: Error! No version specified!'
      print '.::        or "prefix" in each "version" block'
      exit(1)
    
    # Are we ready to make path mods?
    if hasattr(self,'prefix'):
      self.full_prefix = self.prefix
    elif hasattr(self,'pkg_prefix'):
      self.full_prefix = os.path.join(self.pkg_prefix,self.version)
    else:
      print '.:: Error! Package needs to specify "pkg_prefix" in "info" block'
      print '.::        or "prefix" in each "version" block'
      exit(1)
    
    # make std_paths
    for path in self.std_paths:
      try:
        spd =self.std_paths_dict[path]
      except KeyError:
        print '.:: Error! Standard path information not specified. You asked for:'
        print path
        print '.:: I have specifications for the following standard paths:'
        print self.std_paths_dict.keys()
        exit(1)

      value = os.path.join(self.full_prefix,spd['dir'])
      contains = spd.get('contains',list())
      self.path_mods.append(PathMod(name=spd['name'],action=self.action,value=value,contains=contains))
      
    
    self.modded_paths = [i.name for i in self.path_mods]
    self.num_mods = len(self.path_mods)
    self.loaded=True
  def check(self):
    pass

if __name__=="__main__":
  import ipdb; ist = ipdb.set_trace
  pkg = Package('json/hoomd.json')
  pkg.read('2.0')
  ist()

