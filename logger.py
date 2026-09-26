import logging


def log():
    # Create a custom logger named after our pipeline
    main_logger = logging.getLogger('Main_Logger')
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
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # Handler 2: File Handler(Sends DEBUG and above to a local log file)
    file_handler = logging.FileHandler()
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Attach handlers to our logger
    main_logger.addHandler(console_handler)
    main_logger.addHandler(file_handler)

    return main_logger
