export TYPYENV_BIN=$TYPYENV_BASE/typyEnv/bin
export TYPYENV_JSON_PREFIX=$SW_BASE/json


# TYPY needs to be added to the PYTHONPATH
# This allows the typy.typyenv module to import the 
# necessary modules and classes within itself
if [[ -z "$PYTHONPATH" ]]; then
	export PYTHONPATH=$TYPYENV_BASE
else
	export PYTHONPATH=$TYPYENV_BASE:$PYTHONPATH
fi

# The directory containing the typyEnv_driver python 
# script needs to in your $PATH for the bash
# typyEnv function (top of this script) to be able
# to call it
if [[ -z "$PATH" ]]; then
	export PATH=$TYPYENV_BIN
else
	export PATH=$TYPYENV_BIN:$PATH
fi

# When installing new software, it is often best to not load
# any "extra" software that are direct dependencies of the 
# software being compiled. This function runs any bash script
# in a subshell without loading any user configuration. 
typyCleanShell() {
  env -i bash --rcfile /etc/profile $*
}

############################
### BASH DRIVER FUNCTION ###
############################

typyEnv() {
  python_output_str=$(typyEnv_driver $*)

  dev_line_incoming=false
  variables_line_incoming=false
  export_line_incoming=false

  # Need to split the python output from the 
  # strings that needs to be exec'd
  #  The variables line and export line need to be 
  #  processed a bit differently for sanitization.
  #  
  while read -r line; do
    if [[ "$variables_line_incoming" == true ]];then
      # echo "$line"
      #replace all spaces with underscores
      eval_str="${line// /_}"
      eval_str="${eval_str//[^0-9a-zA-z\/\;\=\-\_\:\.]/}"
      eval "$(echo ${eval_str})"
      variables_line_incoming=false
    elif [[ "$export_line_incoming" == true ]];then
      # echo "$line"
      eval_str="${line//[^0-9a-zA-z\_ ]/}"
      eval "$(echo ${eval_str})"
      export_line_incoming=false
    elif [[ "$dev_line_incoming" == true ]];then
      # echo "$line"
      eval_str="${line//[^0-9a-zA-z\/\_\-\.\=\;\' ]/}"
      eval "$(echo ${eval_str})"
      dev_line_incoming=false
    elif [[ "$line" == '[[EXPORT]]' ]];then
      # echo "$line"
      export_line_incoming=true
    elif [[ "$line" == '[[VARIABLES]]' ]];then
      # echo "$line"
      variables_line_incoming=true
    elif [[ "$line" == '[[DEV]]' ]];then
      # echo "$line"
      dev_line_incoming=true
    else
      echo "$line"
    fi
  done <<< "$python_output_str"
}

if [[ ! "$1" == "CLEAN" ]] ; then
  echo ".:: Nothing to load..."
  # typyEnv --add python
  # typyEnv --add vmd
  # typyEnv --add vmd_script
  # typyEnv --add cmake
  # typyEnv --add vtk
  # typyEnv --add tcl
  # typyEnv --add mayavi
fi
