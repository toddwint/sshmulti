---
title: README
date: 2023-08-29
---

# `sshmulti`


## Info

SSH into multiple devices from a single command, splitting the screen, and synchronize the keyboard input.

The devices are supplies at the command line separated by whitespace.


## Overview

Run `sshmulti.py` by supplying the command followed by a list of devices separated by whitespace. Shell expansion can be used.

For example, to run `sshmulti.py` from the current directory with devices named `server1`, `server2`, `server3`, and `server4`, and the username `todd`, run one of the following commands:

```bash
./sshmulti.py todd@server1 todd@server2 todd@server3 todd@server4
```

```bash
./sshmulti.py server1 server2 server3 server4 -l todd
```

```bash
./sshmulti.py todd@server{1..4}
```

```bash
./sshmulti.py server{1..4} -l todd
```

For a list of commands run `sshmulti.py` with the `-h` or `--help` options.


## Screenshots

![Logged into multiple devices and typing the same commands once](https://raw.githubusercontent.com/toddwint/sshmulti/main/docs/figures/sshmulti.py.1.png)


## Requirements

The following are requirements to run this script:

- python3
- ssh
- tmux


## TMUX defaults

It is important to mention that this assumes you have set tmux to start windows and panes at **1** instead of the default **0**. 

Here is my default `.tmux.conf` file for reference.

```
# Improve colors
set -g default-terminal screen-256color

# Set scrollback buffer to 10000
set -g history-limit 10000

# Enable mouse mode (tmux 2.1 and above)
set -g mouse on

# Set first windows and pane to index of 1 (instead of zero)
set -g base-index 1
set -g pane-base-index 1
```
