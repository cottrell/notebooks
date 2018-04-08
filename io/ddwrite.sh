#!/bin/sh
dd if=/dev/zero of=testfile bs=1000000 count=1 conv=fdatasync
