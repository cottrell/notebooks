#!/bin/bash -e

# 1. Pull root repo first
branch=$(git rev-parse --verify master 2>/dev/null 1>&2 && echo master || echo main)
git checkout -q "$branch"
git pull origin "$branch:$branch"

# 2. Pull submodules level by level (shallow to deep)
paths=$(git submodule status --recursive | awk '{print $2}')
max_depth=$(echo "$paths" | awk -F'/' '{print NF}' | sort -nr | head -n1)

for (( d=1; d<=max_depth; d++ )); do
  level_paths=$(echo "$paths" | awk -F'/' -v depth="$d" 'NF==depth')
  [ -z "$level_paths" ] && continue

  for p in $level_paths; do
    (
      cd "$p"
      branch=$(git rev-parse --verify master 2>/dev/null 1>&2 && echo master || echo main)
      git checkout -q "$branch"
      git pull origin "$branch:$branch"
    ) &
  done
  wait
done

