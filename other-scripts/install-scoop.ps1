# Copyright 2020, Collabora, Ltd.
# SPDX-License-Identifier: BSL-1.0
$env:SCOOP='w:\scoop'
[environment]::setEnvironmentVariable('SCOOP',$env:SCOOP,'User')
iwr -useb get.scoop.sh | iex

scoop update
scoop install ninja ripgrep