import os
import re

def get_matching_files(directory_path, pattern):
    """
    Returns a list of files in the specified directory that match the given regular expression pattern.

    Parameters:
        directory_path (str): The path to the directory to search.
        pattern (str): The regular expression pattern to match file names.

    Returns:
        list: A list of file names that match the pattern.
    """
    # Compile the regular expression
    regex = re.compile(pattern)
    
    try:
        # Get all files in the specified directory
        files = os.listdir(directory_path)
        
        # Filter files based on the regular expression pattern
        matching_files = [f for f in files if regex.match(f)]
        return matching_files
    except FileNotFoundError:
        print(f"Error: The directory '{directory_path}' does not exist.")
        return []
    except PermissionError:
        print(f"Error: Permission denied for directory '{directory_path}'.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []