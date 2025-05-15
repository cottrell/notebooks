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


def scan_directories(root_dir, min_files=1000, exclusion_patterns=None):
    if exclusion_patterns is None:
        exclusion_patterns = []

    # Dictionary to track highest level problematic directories
    top_level_dirs = {}

    # First pass: find all directories with .py files
    dirs_with_py = set()
    for dirpath, _, filenames in os.walk(root_dir):
        if any(f.endswith('.py') for f in filenames):
            path = Path(dirpath)
            # Add this dir and all parents to dirs_with_py
            while path != Path(root_dir).parent:
                dirs_with_py.add(str(path))
                path = path.parent

    # Second pass: find directories with many files but no .py files
    for dirpath, dirnames, filenames in os.walk(root_dir):
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

    return [{'path': d, 'file_count': c} for d, c in top_level_dirs.items()]


def main(project_dir=_my_dir, min_files=1000):
    """Find directories with many files but no Python files"""
    # Load VSCode settings
    settings = load_vscode_settings(project_dir)
    exclusion_patterns = []

    # Get VSCode exclusion patterns
    if 'files.watcherExclude' in settings:
        for pattern in settings['files.watcherExclude']:
            if settings['files.watcherExclude'][pattern]:
                exclusion_patterns.append(pattern)

    print(f"Scanning {project_dir} for problematic directories...")
    problematic = scan_directories(project_dir, min_files, exclusion_patterns)

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
