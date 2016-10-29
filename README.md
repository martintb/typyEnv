# typyEnv #

Lightweight environment management written primarily in python. The goal is to efficiently manage environment variables and paths e.g.

* PATH
* CPATH
* LIBRARY_PATH
* LD_LIBRARY_PATH
* CPPFLAGS
* LDFLAGS

## Installation ##
In the install directory, modify the following two lines in install.sh so that the variables correctly point to your software directory and the location of the typyEnv codebase.
``` 
swString='export SW_BASE=/home/tbm/software'
envString='export TYPYENV_BASE=$SW_BASE/typyEnv/0'
```
See the example directory structure below if this isn't clear. Afterwards, running the following will create a typyEnv configuration file as ~/.typyEnv and also add a few lines to your .bashrc to load this file during shell initialization.
```
$ bash install.sh 
```

## Usage ##
See the directory structure below for how to structure your software layout. The attic directories contain the compressed src files for posterity, and each source version is contained in a separate versioned directory. Under each versioned directory, the following standard names are used to recognize specific types of files and paths.

* bin      -> executables     -> PATH
* lib:     -> library files   -> LIBRARY_PATH, LD_LIBRARY_PATH, LDFLAGS
* include: -> header files    -> CPATH, CPPFLAGS
* pylib:   -> python modules  -> PYTHONPATH

The code is written generally enough to handle any environment variable, but these are the ones it handles "automatically". Each package should have a corresponding json file of the following format:
```
{
  "info": {
    "name": "LAMMPS",
    "description": "Large Scale Atomic/Molecular Massively Parallel Simulator!",
    "pkg_prefix":"/home/tbm/software/lammps"
  },
  "defaults": {
    "version":"150525",
    "std_paths":["bin","ldlib","python"],
    "action":"prepend"
  },
  "versions": { "150525": {} , "150525-edit": {} }
}

```
Under the defaults header, the default version is specified as 150525, and typyEnv is told to look for 3 "standard paths": bin, lib, and pylib. If there were specific customization that were needs for specific pacakges, they would go under the "versions" header, which are left as empty {} for now as no customizations are needed. 

Once the directory structure is created, code is compiled, and .json file is written, the package can be loaded with the following command:
```
typyEnv --add lammps --version 150525
```
The --version flag can be omitted and the default will be used. If the --dev flag is used, CPPFLAGS and LDFLAGS will be populated appropriately based on the presence of include and lib directories. 

There is actually quite a bit more typyEnv is capable of and these features will be documented as needed. 

## Example Directory Structure ##
```
software/
├── boost
│   ├── 1.58.0
│   │   ├── include
│   │   ├── lib
│   │   └── src
│   └── attic
│       └── boost_1_58_0.tar.bz2
├── lammps
│   ├── 150525
│   │   ├── bin
│   │   ├── lib
│   │   ├── pylib
│   │   └── src
│   ├── 150525-edit
│   │   ├── bin
│   │   ├── lib
│   │   ├── pylib
│   │   └── src
│   └── attic
│       └── lammps-150525.tar.gz
├── openmpi
│   ├── 1.10.3
│   │   ├── build
│   │   └── src
│   └── attic
│       └── openmpi-1.10.3.tar.bz2
├── json
    ├── boost.json
    ├── lammps.json
    └── openmpi.json

```