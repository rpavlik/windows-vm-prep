# Copyright 2020, Collabora, Ltd.
# SPDX-License-Identifier: BSL-1.0
$env:SCOOP='w:\scoop'
[environment]::setEnvironmentVariable('SCOOP',$env:SCOOP,'User')
Invoke-WebRequest -useb get.scoop.sh | Invoke-Expression

scoop update
scoop install ninja ripgrep curl 7zip