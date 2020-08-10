@echo off
rem Copyright 2020, Collabora, Ltd.
rem SPDX-License-Identifier: BSL-1.0
powershell -executionpolicy remotesigned -command "Set-ExecutionPolicy RemoteSigned -scope CurrentUser"
powershell -executionpolicy remotesigned -command "%~dp0\\install-scoop.ps1"
