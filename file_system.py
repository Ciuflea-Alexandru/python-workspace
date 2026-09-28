import inspect
from pathlib import Path


def main_directories(categories: list[str], base_path: str | Path | None = None) -> None:
    """
    Ensures that 'logs' and 'data' directories exist inside each category folder.

    Args:
        categories (list[str]): List of category folder names.
        base_path (str | Path | None): The root directory. If None, automatically
                                       resolves to the directory of the script calling this function.
    """
    if base_path is None:
        # Inspect the caller's stack frame to find the file path of the script that invoked this
        caller_frame = inspect.currentframe().f_back
        caller_file = inspect.getfile(caller_frame)
        base = Path(caller_file).resolve().parent
    else:
        base = Path(base_path)

    for category in categories:
        cat_path = base / category
        subdirs = ['logs', 'data']

        for subdir in subdirs:
            target_dir = cat_path / subdir

            # parents=True: creates parent category folders if they don't exist yet
            # exist_ok=True: suppresses FileExistsError if the directory already exists
            target_dir.mkdir(parents=True, exist_ok=True)
            print(f'[SUCCESS] Ready {target_dir}')


# Define your project structure categories
if __name__ == '__main__':
    project_categories = [
        'data_handling',
        'math_and_logic',
        'object_oriented'
    ]

    # Now you can just call it cleanly without specifying any paths!
    main_directories(project_categories)