#!/usr/bin/env python3
# Copyright 2020, Collabora, Ltd.
# SPDX-License-Identifier: BSL-1.0

from itertools import chain

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
    'coenraads.bracket-pair-colorizer',
    'editorconfig.editorconfig',
    'kevinkyang.auto-comment-blocks',
    'marvhen.reflow-markdown',
    'ms-python.python',
    'ms-vscode-remote.remote-wsl',
    'ms-vscode.cmake-tools',
    'ms-vscode.cpptools',
    'ms-vscode.powershell',
    'twxs.cmake',
    'vscode-icons-team.vscode-icons',
    'yzhang.markdown-all-in-one',
    'ziyasal.vscode-open-in-github',
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
    return 'powershell -executionpolicy remotesigned -command "{}"'.format(ps_command.replace('"', r'\"'))


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
VS_PS = 'vs-update-modify.ps1'

OVERALL_BATCH = 'install-all.cmd'

if __name__ == "__main__":
    print("@echo off")

    calls = [
        ECHO_OFF,
        # Install scoop, set execution policy to remotesigned for this user.
        "call other-scripts\\enable-ps-and-install-scoop.cmd\n"
    ]

    # Install packages using winget
    print(getWingetCommands())
    with open(WINGET_BATCH, 'w') as fp:
        fp.writelines(ECHO_OFF)
        fp.writelines(getWingetCommands())
    calls.append('call ' + WINGET_BATCH)

    # Install vscode extensions
    print()
    cmd = 'code {}'.format(' '.join('--install-extension {}'.format(x)
                                    for x in VSCODE_EXTENSIONS))
    print(cmd)
    with open(VSCODE_BATCH, 'w') as fp:
        fp.writelines(ECHO_OFF)
        fp.writelines(cmd)
        fp.write('\n')
    calls.append('call ' + VSCODE_BATCH)

    with open(VS_PS, 'w') as fp:
        # Update visual studio
        print()
        fp.write('echo "Now updating Visual Studio"\n')
        args = ['update']
        args.extend(VS_INSTALLER_BASE_CMD_ARGS)
        fp.writelines(makeStartProcess(VS_INSTALLER, args))
        fp.write('\n')

        # Install additional components in visual studio
        print()
        fp.write(
            'echo "Now modifying Visual Studio to include all desired components"\n')
        args = ['modify']
        args.extend(VS_INSTALLER_BASE_CMD_ARGS)
        # The chain.from_iterable is so that we can add two items to the list
        # for each single item in the original list and thus the comprehension
        args.extend(chain.from_iterable(("--add", "{};includeRecommended".format(x))
                                        for x in VS_WORKLOADS))
        args.extend(chain.from_iterable(("--add", x) for x in VS_COMPONENTS))
        fp.writelines(makeStartProcess(VS_INSTALLER, args))
        fp.write('\n')
        fp.write('echo "Done messing with Visual Studio"\n')

    calls.append(wrapPowershellForCmd('& .\\' + VS_PS))

    with open(OVERALL_BATCH, 'w') as fp:
        fp.writelines(ECHO_OFF)
        fp.writelines('\n'.join(calls))
