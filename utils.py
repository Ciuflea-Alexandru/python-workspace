from pathlib import Path


def setup_project_directories(categories: list[str], base_path: str | Path = '.') -> None:
    """
        Ensures that 'logs' and 'data' directories exist inside each category folder.

        Args:
            categories (list[str]): List of category folder names.
            base_path (str): The root directory where categories should be created.
        """
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

    setup_project_directories(project_categories)
