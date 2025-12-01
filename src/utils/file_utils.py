"""
File utilities for reading and writing rFactor files.

rFactor files use Windows-1252 encoding (cp1252) and CRLF line endings.
"""

from pathlib import Path
from typing import List, Optional


# Standard encoding for rFactor files
RFACTOR_ENCODING = 'cp1252'
RFACTOR_LINE_ENDING = '\r\n'


def read_rfactor_file(filepath: str) -> str:
    """
    Read a rFactor file with the correct encoding.

    Args:
        filepath: Path to the file to read

    Returns:
        File content as string

    Raises:
        FileNotFoundError: If the file doesn't exist
        UnicodeDecodeError: If the file can't be decoded with cp1252
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(path, 'r', encoding=RFACTOR_ENCODING) as f:
        return f.read()


def write_rfactor_file(filepath: str, content: str) -> None:
    """
    Write a rFactor file with the correct encoding and line endings.

    Args:
        filepath: Path to the file to write
        content: Content to write

    Raises:
        PermissionError: If the file can't be written
    """
    path = Path(filepath)

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    # Normalize line endings to CRLF
    normalized_content = content.replace('\r\n', '\n').replace('\n', RFACTOR_LINE_ENDING)

    with open(path, 'w', encoding=RFACTOR_ENCODING, newline='') as f:
        f.write(normalized_content)


def find_files_by_extension(directory: str, extension: str, recursive: bool = True) -> List[Path]:
    """
    Find all files with a specific extension in a directory.

    Args:
        directory: Directory to search in
        extension: File extension to search for (e.g., '.rcd', '.veh')
        recursive: Whether to search recursively in subdirectories

    Returns:
        List of Path objects for matching files

    Raises:
        NotADirectoryError: If the directory doesn't exist
    """
    path = Path(directory)
    if not path.exists():
        raise NotADirectoryError(f"Directory not found: {directory}")

    if not path.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    # Normalize extension
    if not extension.startswith('.'):
        extension = '.' + extension

    pattern = f"**/*{extension}" if recursive else f"*{extension}"
    return sorted(path.glob(pattern))


def get_filename_without_extension(filepath: str) -> str:
    """
    Get the filename without extension.

    Args:
        filepath: Path to the file

    Returns:
        Filename without extension

    Example:
        >>> get_filename_without_extension("path/to/BrandonLang.rcd")
        'BrandonLang'
    """
    return Path(filepath).stem


def normalize_name_to_filename(name: str) -> str:
    """
    Normalize a name to a valid filename (remove spaces).

    Args:
        name: Name to normalize (e.g., "Brandon Lang")

    Returns:
        Normalized filename (e.g., "BrandonLang")

    Example:
        >>> normalize_name_to_filename("Brandon Lang")
        'BrandonLang'
    """
    return name.replace(' ', '')


def file_exists(filepath: str) -> bool:
    """
    Check if a file exists.

    Args:
        filepath: Path to check

    Returns:
        True if file exists, False otherwise
    """
    return Path(filepath).exists()


def ensure_directory_exists(directory: str) -> None:
    """
    Ensure a directory exists, create it if it doesn't.

    Args:
        directory: Directory path to ensure exists
    """
    Path(directory).mkdir(parents=True, exist_ok=True)


def get_relative_path(filepath: str, base_path: str) -> str:
    """
    Get the relative path from base_path to filepath.

    Args:
        filepath: Target file path
        base_path: Base path to calculate relative path from

    Returns:
        Relative path as string with backslashes (rFactor format)

    Example:
        >>> get_relative_path(
        ...     "C:/rFactor/GameData/Talent/BrandonLang.rcd",
        ...     "C:/rFactor"
        ... )
        'GameData\\\\Talent\\\\BrandonLang.rcd'
    """
    path = Path(filepath)
    base = Path(base_path)

    try:
        relative = path.relative_to(base)
        # Convert to Windows-style path (backslashes)
        return str(relative).replace('/', '\\')
    except ValueError:
        # If filepath is not relative to base_path, return absolute path
        return str(path).replace('/', '\\')


def normalize_rfactor_path(path: str) -> str:
    """
    Normalize a path to rFactor format (uppercase, backslashes).

    Args:
        path: Path to normalize

    Returns:
        Normalized path with backslashes and uppercase

    Example:
        >>> normalize_rfactor_path("gamedata/vehicles/rhez/car.veh")
        'GAMEDATA\\\\VEHICLES\\\\RHEZ\\\\CAR.VEH'
    """
    return path.replace('/', '\\').upper()
