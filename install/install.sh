#!/bin/bash

swString='export SW_BASE=/Users/tbm/software'
envString='export TYPYENV_BASE=$SW_BASE/typyEnv/git'


echo '--> Creating shell initialization file (~/.typyEnv)'
echo "#!/bin/bash"    > ~/.typyEnv
echo " "             >> ~/.typyEnv
echo "$swString"     >> ~/.typyEnv
echo "$envString"    >> ~/.typyEnv
cat  dotTypyEnv.sh   >> ~/.typyEnv

init_str='
if [ -f ~/.typyEnv ]; then
    echo "--> Adding typyEnv to path ::."
    . ~/.typyEnv
fi
'
if  ! $(grep -q '\. ~/.typyEnv' ~/.bashrc) ; then
  echo '--> Adding initialization file to ~/.bashrc'
  echo "$init_str" >> ~/.bashrc
fi
