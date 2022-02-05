#!/usr/bin/env python
import os
import glob
import subprocess

_mydir = os.path.dirname(os.path.realpath(__file__))

def run_command_get_output(cmd, shell=True, splitlines=True, raise_exceptions=False):
    """A call to run shell commands and properly handle stdout, stderr and status. No stdin."""
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
    out, err = p.communicate()
    status = p.returncode
    out = out.decode()
    err = err.decode()
    if splitlines:
        out = out.split("\n")
        err = err.split("\n")
    res = dict(out=out, err=err, status=status, cmd=cmd)
    if raise_exceptions and status != 0:
        raise Exception("error running {}".format(res))
    return res

def main():
    filenames = glob.glob(os.path.join(_mydir, '*.epub'))
    res = dict()
    for filename in filenames:
        target = os.path.join(_mydir, 'for_kindle', os.path.basename(filename)[:-5].replace(' (z-lib.org)', '') + '.mobi')
        if os.path.exists(target):
            print(f'{target} exists ... skipping')
        else:
            cmd = f'ebook-convert "{filename}" "{target}"'
            print(cmd)
            res[filename] = run_command_get_output(cmd)
            print(res[filename])
    errs = sum([v['status'] for k, v in res.items()])
    if errs == 0:
        print('success')
    else:
        print(f'there were {errs} errs')
    return res



if __name__ == '__main__':
    main()
