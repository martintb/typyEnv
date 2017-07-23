from __future__ import print_function
import os
from typyEnv.Path import Path
from typyEnv.PathMod import PathMod

class Environment(object):
  def __init__(self):
    self.paths={}
    self.dev_paths={}
    self.lib_mods=[]
    self.inc_mods=[]
    # right now, this self.paths method doesn't handle adding to the same path twice...
  def add_package(self,pkg,export_dev_paths=False):
    if pkg.loaded:
      print('--> Adding package {} version {} to {}'.format(pkg.name,pkg.version,pkg.modded_paths))
    else:
      print('==> Error! Package not loaded! Need to call pkg.read()!')
      exit(1)
    for mod in pkg.path_mods:
      self.mod_path(mod)
      if export_dev_paths:
        if 'libraries' in mod.contains:
          print('--> Appending library path {} to LDFLAGS'.format(mod.value))
          self.lib_mods.append(PathMod(name='LDFLAGS',action='append',value='-L{}'.format(mod.value)))
        if 'headers' in mod.contains:
          print('--> Appending header path {} to CPPFLAGS'.format(mod.value))
          self.inc_mods.append(PathMod(name='CPPFLAGS',action='append',value='-I{}'.format(mod.value)))
  def mod_path(self,mod,action=None,dev=False,sep=':'):
    if dev:
      paths=self.dev_paths
    else:
      paths=self.paths
    if mod.name not in self.paths:
      paths[mod.name] = Path(os.environ.get(mod.name,None),mod.name,sep=sep)
    paths[mod.name].modify(mod,action=action)
  def remove_package(self,pkg):
    if pkg.loaded:
      print('--> Removing package {} version {} from {}'.format(pkg.name,pkg.version,pkg.modded_paths))
    else:
      print('==> Error! Package not loaded! Need to call pkg.read()!')
      exit(1)
    for mod in pkg.path_mods:
      if mod.name not in self.paths:
        path = Path(os.environ.get(mod.name,None),mod.name)
        self.paths[mod.name] = path
      self.paths[mod.name].modify(mod,action='remove')
  def export(self,export_dev_paths=False):
    variables_str = ''
    export_list = ['export']
    for name,path in self.paths.items():
      variables_str += '{}={};'.format(name,path.join())
      export_list.append('{}'.format(name))

    dev_str=''
    if export_dev_paths:
      for mod in self.lib_mods:
        self.mod_path(mod,dev=True,sep=' ')
      for mod in self.inc_mods:
        self.mod_path(mod,dev=True,sep=' ')
      for name,path in self.dev_paths.items():
        dev_str += '{}=\'{}\';'.format(name,path.join())
        export_list.append('{}'.format(name))

    export_str = ' '.join(export_list)
    export_str += ';'
    return dev_str,variables_str,export_str


