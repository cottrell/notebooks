#!/bin/bash -e

# 1. Push submodules level by level (deepest leaves first to shallowest)
paths=$(git submodule status --recursive | awk '{print $2}')
max_depth=$(echo "$paths" | awk -F'/' '{print NF}' | sort -nr | head -n1)

for (( d=max_depth; d>=1; d-- )); do
  level_paths=$(echo "$paths" | awk -F'/' -v depth="$d" 'NF==depth')
  [ -z "$level_paths" ] && continue

  for p in $level_paths; do
    (
      cd "$p"
      branch=$(git rev-parse --verify master 2>/dev/null 1>&2 && echo master || echo main)
      git checkout -q "$branch"
      git push origin "$branch"
    ) &
  done
  wait
done

# 2. Push root repo last
git push --recurse-submodules=on-demand origin

