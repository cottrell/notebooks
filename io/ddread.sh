#!/bin/sh
dd of=/dev/null if=testfile bs=1G count=1 oflag=direct conv=fdatasync
