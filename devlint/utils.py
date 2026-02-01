"""Utility functions for DevLint."""

import os
from pathlib import Path


def find_git_root():
    """Find the root directory of the git repository."""
    current = Path.cwd()
    
    while current != current.parent:
        if (current / '.git').exists():
            return current
        current = current.parent
    
    return None


def ensure_directory(path):
    """Ensure a directory exists, create if it doesn't."""
    Path(path).mkdir(parents=True, exist_ok=True)


def format_file_size(bytes_size):
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def is_git_repository():
    """Check if current directory is inside a git repository."""
    return find_git_root() is not None


def get_project_name():
    """Get the name of the current project/repository."""
    git_root = find_git_root()
    if git_root:
        return git_root.name
    return Path.cwd().name