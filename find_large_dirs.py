#!/usr/bin/env python
import fnmatch
import json
import os
from pathlib import Path

import argh

_my_dir = os.path.realpath(os.path.dirname(__file__))


def load_vscode_settings(project_root):
    settings_path = os.path.join(project_root, '.vscode', 'settings.json')
    print(f'loading {settings_path}')
    try:
        with open(settings_path, 'r') as f:
            settings = json.load(f)
        return settings
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def is_excluded(path, exclusion_patterns, root_dir):
    """Check if a path should be excluded based on VSCode patterns."""
    # Get path relative to project root
    rel_path = os.path.relpath(path, root_dir)

    # Convert Windows backslashes to forward slashes for consistency
    rel_path = rel_path.replace('\\', '/')

    # Add special case for .git directory
    if '/.git/' in f'/{rel_path}/':
        return True

    # Test against each exclusion pattern
    for pattern in exclusion_patterns:
        # Remove leading ./ from pattern if present
        if pattern.startswith('./'):
            pattern = pattern[2:]

        # Handle patterns with and without ** prefix
        if pattern.startswith('**/'):
            # Match anywhere in path
            if fnmatch.fnmatch(rel_path, pattern[3:]) or fnmatch.fnmatch(rel_path, pattern):
                return True
        else:
            # Match from root
            if fnmatch.fnmatch(rel_path, pattern):
                return True

        # Also try matching with ** appended (for directory patterns)
        if pattern.endswith('/'):
            if fnmatch.fnmatch(rel_path, pattern + '**'):
                return True

    return False


def scan_directories(root_dir, min_files=1000, exclusion_patterns=None, follow_symlinks=True):
    if exclusion_patterns is None:
        exclusion_patterns = []

    # Dictionary to track highest level problematic directories
    top_level_dirs = {}

    # Keep track of visited real paths to prevent symlink cycles
    visited_paths = set()
    symlinks_found = []

    # First pass: find all directories with .py files
    dirs_with_py = set()
    for dirpath, dirnames, filenames in os.walk(root_dir, followlinks=follow_symlinks):
        # Handle symlinks - check for cycles
        real_path = os.path.realpath(dirpath)
        if real_path in visited_paths:
            print(f"Skipping already visited path (symlink): {dirpath} -> {real_path}")
            dirnames[:] = []  # Don't descend further
            continue
        visited_paths.add(real_path)

        # Check for symlinks in current directory list
        i = len(dirnames) - 1
        while i >= 0:
            full_path = os.path.join(dirpath, dirnames[i])
            if os.path.islink(full_path):
                target = os.path.realpath(full_path)
                symlinks_found.append((full_path, target))
                # We keep the symlink in dirnames if follow_symlinks is True
                # VSCode does follow symlinks, so we should too
                if not follow_symlinks:
                    del dirnames[i]
            i -= 1

        if any(f.endswith('.py') for f in filenames):
            path = Path(dirpath)
            # Add this dir and all parents to dirs_with_py
            while path != Path(root_dir).parent:
                dirs_with_py.add(str(path))
                path = path.parent

    # Reset visited paths for second pass
    visited_paths = set()

    # Second pass: find directories with many files but no .py files
    for dirpath, dirnames, filenames in os.walk(root_dir, followlinks=follow_symlinks):
        # Handle symlinks - check for cycles
        real_path = os.path.realpath(dirpath)
        if real_path in visited_paths:
            dirnames[:] = []  # Don't descend further
            continue
        visited_paths.add(real_path)

        # Check symlinks in this level
        i = len(dirnames) - 1
        while i >= 0:
            full_path = os.path.join(dirpath, dirnames[i])
            if os.path.islink(full_path):
                if not follow_symlinks:
                    del dirnames[i]
            i -= 1

        path = Path(dirpath)

        # Skip excluded directories - check the actual path against patterns
        if is_excluded(dirpath, exclusion_patterns, root_dir):
            dirnames[:] = []  # Don't traverse into excluded dirs
            continue

        # Skip if this directory or any parent has .py files
        if dirpath in dirs_with_py:
            continue

        # Count files in this directory and immediate subdirectories
        file_count = len(filenames)
        for dirname in dirnames:
            subdir = os.path.join(dirpath, dirname)
            try:
                file_count += sum(1 for _ in os.scandir(subdir) if _.is_file())
            except (PermissionError, OSError):
                pass

        if file_count >= min_files:
            # Check if any parent directory is already in our results
            is_subdirectory = False
            parent_path = path.parent
            while parent_path != Path(root_dir).parent:
                if str(parent_path) in top_level_dirs:
                    is_subdirectory = True
                    break
                parent_path = parent_path.parent

            if not is_subdirectory:
                # Remove any child directories already in results
                for existing_dir in list(top_level_dirs.keys()):
                    if existing_dir.startswith(dirpath):
                        del top_level_dirs[existing_dir]

                # Add this directory
                top_level_dirs[dirpath] = file_count

    # Print symlinks found
    if symlinks_found:
        print("\nSymlinks found:")
        for src, dst in symlinks_found:
            print(f"  {src} -> {dst}")

    return [{'path': d, 'file_count': c} for d, c in top_level_dirs.items()]


def main(project_dir=_my_dir, min_files=1000, follow_symlinks=True, verbose=False):
    """Find directories with many files but no Python files"""
    # Load VSCode settings
    settings = load_vscode_settings(project_dir)
    exclusion_patterns = []

    # Get VSCode exclusion patterns
    if 'files.watcherExclude' in settings:
        for pattern in settings['files.watcherExclude']:
            if settings['files.watcherExclude'][pattern]:
                exclusion_patterns.append(pattern)
                if verbose:
                    print(f"Using exclusion pattern: {pattern}")

    print(f"Scanning {project_dir} for problematic directories...")
    problematic = scan_directories(project_dir, min_files, exclusion_patterns, follow_symlinks)

    print(f"\nFound {len(problematic)} potential problematic top-level directories:")
    for dir_info in sorted(problematic, key=lambda x: x['file_count'], reverse=True):
        print(f"{dir_info['path']} - {dir_info['file_count']} files")

    if problematic:
        print("\nAdd these to your VSCode settings.json 'files.watcherExclude' section:")
        for dir_info in problematic:
            rel_path = os.path.relpath(dir_info['path'], project_dir)
            rel_path = rel_path.replace('\\', '/')  # Ensure forward slashes
            pattern = f"**/{rel_path}/**"
            print(f'    "{pattern}": true,')
    else:
        print("\nNo problematic directories found that aren't already excluded!")


if __name__ == "__main__":
    argh.dispatch_command(main)
