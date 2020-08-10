#!/bin/sh
# Copyright 2020, Collabora, Ltd.
# SPDX-License-Identifier: BSL-1.0
# Set user name/email from this repo's latest commit user name/email.
git config --global user.name $(git show --no-patch --format='%an')
git config --global user.email $(git show --no-patch --format='%ae')