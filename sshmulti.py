#!/usr/bin/env python3
"""
Another multiple ssh launcher. Requires openssh client and tmux.
"""

__author__ = 'Todd Wintermute'
__date__ = '2023-08-27'
__version__ = '0.0.4'

import argparse
import datetime as dt
import shutil
import subprocess
import sys

def parse_arguments():
    """Create command line arguments and auto generated help"""
    parser = argparse.ArgumentParser(
        description = __doc__,
        epilog = 'Please be responsible.',
        )
    parser.add_argument(
        '-v', '--version',
        help = 'show the version number and exit',
        action = 'version',
        version= f'Version: %(prog)s  {__version__}  ({__date__})',
        )
    parser.add_argument(
        'destination',
        type = str,
        nargs = '+',
        help = (
            f'Specifies the user or login name and address on the remote '
            'machine in the form of user@host, user@ip, or just host or ip'
            ),
        )
    parser.add_argument(
        '-l', '--login_name',
        type = str,
        help = f'Specifies the user to log in as on the remote machine',
        )
    return parser

def mssh_using_tmux(sshlist):
    """Creates a new tmux session using the supplied list of addresses"""
    now = dt.datetime.now().replace(microsecond=0)
    tstamp = now.isoformat().translate({ord('-'): '', ord(':'): ''})
    tmux_session = f'sshmulti-{tstamp}'
    window_name = ','.join([dest.split('@')[-1] for dest in sshlist])
    rval = sh_run(f'tmux new-session -d -s {tmux_session}')
    rval = sh_run(f'tmux rename-window {tmux_session}')
    #rval = sh_run(f'tmux rename-window "{window_name}"')
    #rval = sh_run(f'tmux set-option -wg automatic-rename off')
    #rval = sh_run(f'tmux set-option -wg set-titles on')
    #rval = sh_run(f'tmux set-option -wg set-titles-string "sshmulti"')
    rval = sh_run(f'tmux set-option -wg status-left "[sshmulti] "')
    rval = sh_run(f'tmux set-option -wg status-left-length 24')
    rval = sh_run(f'tmux set-option -g pane-border-status top')
    rval = sh_run(f'tmux set-option -g pane-border-format " [ ###P #T ] "')
    rval = sh_run(f'tmux set-option -g base-index 1')
    rval = sh_run(f'tmux set-option -g pane-base-index 1')
    for item in sshlist:
        rval = sh_run(f"tmux split-window 'ssh {item}'")
        rval = sh_run(f'tmux select-pane -T {item}')
        rval = sh_run(f'tmux select-layout tiled')
    rval = sh_run(f'tmux kill-pane -t 1')
    rval = sh_run(f'tmux set-window-option synchronize-panes on')
    rval = sh_run(f'tmux select-layout tiled')
    rval = sh_run(f'tmux attach -t {tmux_session}')
    return rval

def sh_run(command):
    """Runs a shell command via subprocess.run. Return value is int"""
    rval = subprocess.run(command, shell=True)
    return rval.returncode

def main():
    """Start of main program"""
    global args
    parser = parse_arguments()
    args = parser.parse_args()
    # Verify the system has ssh and tmux
    if not shutil.which('ssh'):
        print(
            "`ssh` is required but was not found. "
            "Obtain `ssh`, and ensure `ssh` is on the system path. Bye."
            )
        sys.exit()
    if not shutil.which('tmux'):
        print(
            "`tmux` is required but was not found. "
            "Obtain `tmux`, and ensure `tmux` is on the system path. Bye."
            )
        sys.exit()
    if args.login_name:
        sshlist = [
            f"{args.login_name}@{dest.split('@')[-1]}"
            for dest in args.destination
            ]
    else:
        sshlist = args.destination
    mssh_using_tmux(sshlist)
    print('Done!')

if __name__ == '__main__':
    main()
