import subprocess

def fit_to_tcx(fit_path, tcx_path):
    """
    Converts a .fit file to .tcx format using the fittotcx tool.

    Parameters:
        fit_path (str): Path to the input .fit file.
        tcx_path (str): Path to save the output .tcx file.
    """
    # Define the command to run the fittotcx tool
    command = ['fittotcx', fit_path]

    try:
        # Open the output file in write mode and run the command
        with open(tcx_path, 'w') as output_file:
            result = subprocess.run(
                command,
                stdout=output_file,
                stderr=subprocess.PIPE,
                text=True,
                check=True  # Raise an exception if the command fails
            )
        print(f"Conversion successful: {fit_path} -> {tcx_path}")
    except FileNotFoundError:
        print("Error: 'fittotcx' tool not found. Ensure it is installed and in your PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Command failed with return code {e.returncode}")
        print(f"Stderr: {e.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")