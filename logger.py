import logging
import inspect
from pathlib import Path


def log() -> logging.Logger:
    """
    Sets up a logger that dynamically writes to the correct category's logs folder
    and names the log file after the calling script
    """

    # 1. FIND THE CORRECT PATH

    # Inspect the stack to find the frame of the script that called the logger
    caller_frame = inspect.stack()[1]
    caller_file = Path(caller_frame.filename).resolve()
    script_name = caller_file.stem

    # Automatically build the logs path based on where the caller exists
    logs_dir = caller_file.parent / "logs"
    log_file_path = logs_dir / f'{script_name}.log'

    # 2. SET UP THE LOGGER

    # Create a custom logger named after our pipeline
    main_logger = logging.getLogger(script_name)
    # Set base level to capture everything
    main_logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers if the function is called multiple times
    if main_logger.handlers:
        return main_logger

    # Define a rich formatter(Timestamp, Logger Name, Level, File/Line, Message)
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | [%(filename)s:%(lineno)d] | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler 1: Console Handler(Sends INFO and above to the terminal)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Handler 2: File Handler(Sends DEBUG and above to a local log file)
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Attach handlers to our logger
    main_logger.addHandler(console_handler)
    main_logger.addHandler(file_handler)

    return main_logger
