#!/usr/bin/env python3
# Copyright 2020, Collabora, Ltd.
# SPDX-License-Identifier: BSL-1.0

WINGET_PACKAGES = (
    "git",
    "python",
    "notepad++",
    "Kitware.CMake",
    "KhronosGroup.VulkanSDK",
    "Microsoft.Powertoys",
    "Microsoft.WindowsTerminal",
    "Mozilla.Firefox",
)

VS_WORKLOADS = (
    'Microsoft.VisualStudio.Workload.NativeDesktop',
)

VS_COMPONENTS = (
    'Microsoft.VisualStudio.Component.VC.Llvm.Clang',
    'Microsoft.VisualStudio.ComponentGroup.NativeDesktop.Llvm.Clang',
    'Component.GitHub.VisualStudio',
    'Microsoft.VisualStudio.Component.VC.14.20.ARM',
    'Microsoft.VisualStudio.Component.VC.14.20.ARM64'
)
VS_CHANNEL = "VisualStudio.16.Release"
VS_PRODUCT = "Microsoft.VisualStudio.Product.Community"
VS_INSTALLER = "C:\\Program Files (x86)\\Microsoft Visual Studio\\Installer\\vs_installer.exe"

VS_INSTALLER_BASE_CMD_ARGS = [
    "--channelId", VS_CHANNEL,
    "--productId", VS_PRODUCT,
    "--quiet",
    # "--installWhileDownloading",
    # "--noRestart"
]

VSCODE_EXTENSIONS = (
    'ms-vscode.cmake-tools',
    'ms-vscode.cpptools',
    'ms-python.python',
    'yzhang.markdown-all-in-one',
    'ziyasal.vscode-open-in-github',
    'vscode-icons-team.vscode-icons',
    'marvhen.reflow-markdown',
    'twxs.cmake',
)


def makeStartProcess(cmd, args):
    """Return a powershell command to start and wait for a process with the given args."""
    ret = [
        "Start-Process",
        "-FilePath",

        '"{}"'.format(cmd),
        "-ArgumentList",
    ]
    quoted_arg_list = ','.join('"{}"'.format(x) for x in args)
    ret.append(quoted_arg_list)
    ret.append("-Wait")
    return ' '.join(ret)


def wrapPowershellForCmd(ps_command):
    """Wrap a powershell command for invocation from cmd."""
    # We're technically escaping for cmd here.
    return "powershell -executionpolicy remotesigned -command '{}'".format(ps_command.replace("'", r"\'"))


def getWingetCommands():
    lines = []
    for pkg in WINGET_PACKAGES:
        lines.append("winget install {}".format(pkg))
        lines.append(
            r"if %ERRORLEVEL% EQU 0 Echo {} installed successfully. ".format(pkg))
    return '\n'.join(lines)

ECHO_OFF = "@echo off\n"
WINGET_BATCH = 'winget-packages.cmd'
VSCODE_BATCH = 'vscode-extensions.cmd'
VS_BATCH = 'vs-update-modify.cmd'

OVERALL_BATCH = 'install-all.cmd'

if __name__ == "__main__":
    print("@echo off")

    calls = [ ECHO_OFF ]

    # Install packages using winget
    print(getWingetCommands())
    with open(WINGET_BATCH, 'w') as fp:
        fp.writelines(ECHO_OFF)
        fp.writelines(getWingetCommands())
    calls.append('call '+ WINGET_BATCH)

    # Install vscode extensions
    print()
    cmd = 'code {}'.format(' '.join('--install-extension {}'.format(x)
                                    for x in VSCODE_EXTENSIONS))
    print(cmd)
    with open(VSCODE_BATCH, 'w') as fp:
        fp.writelines(ECHO_OFF)
        fp.writelines(cmd)
        fp.write('\n')
    calls.append('call '+ VSCODE_BATCH)


    with open(VS_BATCH, 'w') as fp:
        fp.writelines(ECHO_OFF)
        # Update visual studio
        print()
        args = ['update']
        args.extend(VS_INSTALLER_BASE_CMD_ARGS)
        fp.writelines(wrapPowershellForCmd(makeStartProcess(VS_INSTALLER, args)))
        fp.write('\n')

        # Install additional components in visual studio
        print()
        args = ['modify']
        args.extend(VS_INSTALLER_BASE_CMD_ARGS)
        args.extend("--add {};includeRecommended".format(x) for x in VS_WORKLOADS)
        args.extend("--add {}".format(x) for x in VS_COMPONENTS)
        fp.writelines(wrapPowershellForCmd(makeStartProcess(VS_INSTALLER, args)))
        fp.write('\n')

    calls.append('call ' + VS_BATCH)
    with open(OVERALL_BATCH, 'w') as fp:
        fp.writelines(ECHO_OFF)
        fp.writelines('\n'.join(calls))
