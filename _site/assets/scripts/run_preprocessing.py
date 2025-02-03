import subprocess

commands = [
    "python assets/scripts/process_metadata.py",
    "python assets/scripts/include_lectorate_corrections.py",
    "python assets/scripts/update_coordinates.py",
    "python assets/scripts/update_object_filepaths_to_metadata_file.py",
    "python assets/scripts/date_destruction_nomalize.py"
]

for cmd in commands:
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, text=True)
    if result.returncode != 0:
        print(f"Error occurred while running: {cmd}")
        break
    print(f"Completed: {cmd}")

print("All steps completed.")
