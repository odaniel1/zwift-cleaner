import re

def strip_position_from_tcx(tcx_path, output_path):
    """
    Removes <Position> elements from a TCX file.

    Parameters:
        tcx_path (str): Path to the input TCX file.
        output_path (str): Path to save the modified TCX file.
    """
    try:
        # Read the content of the TCX file
        with open(tcx_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Define the regular expression pattern to match <Position> tags
        pattern = re.compile(r'<Position>.*?</Position>', re.DOTALL)

        # Remove <Position> tags and their content
        modified_content = re.sub(pattern, '', content)

        # Write the modified content to the output file
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)

        print(f"Position data stripped successfully. Output saved to {output_path}")
    except FileNotFoundError:
        print(f"Error: File not found: {tcx_path}")
    except PermissionError:
        print(f"Error: Permission denied for file: {tcx_path} or {output_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")