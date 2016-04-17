#!/bin/bash
# AMG evns for afanasy extra env

export AMG_ROOT=$PWD
# plugins
export AMG_PLUGINS="${AMG_ROOT}/plugins"
# scripts
export PATH="${AMG_ROOT}:${AMG_ROOT}/scripts:${AMG_ROOT}/scripts/amg/af/bin:${PATH}"

# temp
# export AMG_TEMP=
# RV Player
# export RVPALYER=

# Call custom setup scripts named "env_*.sh" :
for setup_file in env_*.sh
do
	[ -z "$setup_file"  ] && continue
	[ -f "$setup_file"  ] || continue
	source ./$setup_file ""
done