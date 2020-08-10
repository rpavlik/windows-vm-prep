rem Copyright 2020, Collabora, Ltd.
rem SPDX-License-Identifier: BSL-1.0
curl.exe -l https://gist.githubusercontent.com/rpavlik/c5f297be79bab1077ecd26339dcb674f/raw/5f6245aa806c498ff44be52d8efa7f95558c7460/git-prep.sh | & "C:\Program Files\Git\bin\bash.exe"
& "C:\Program Files\Git\bin\bash.exe" "%~dp0\bootstrap-git-config.sh"
