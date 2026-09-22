import logging
import sys


def setup_pipeline_logger():
    # Create a custom logger named after our pipeline
    pipeline_logger = logging.getLogger('ETL_Pipeline')
    # Set base level to capture everything
    pipeline_logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers if the function is called multiple times
    if pipeline_logger.handlers:
        return pipeline_logger

    # Define a rich formatter(Timestamp, Logger Name, Level, File/Line, Message)
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)-8s | [%(filename)s:%(lineno)d] | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler 1: Console Handler(Sends INFO and above to the terminal)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Handler 2: File Handler(Sends DEBUG and above to a local log file)
    file_handler = logging.FileHandler('logs/logging_not_print.log', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Attach handlers to our logger
    pipeline_logger.addHandler(console_handler)
    pipeline_logger.addHandler(file_handler)

    return pipeline_logger


logger = setup_pipeline_logger()


def demonstrate_log_levels():
    # Shows the 5 standard logging levels in order of severity
    logger.debug('DEBUG: Usethis for granular variable states( row counts, intermediate values)')
    logger.info('INFO: Use this for successful milestones( Connected to S3 bucket)')
    logger.warning('WARNING: Non-breaking issues( Mising optional column, filling with defaults)')
    logger.error('ERROR: A task failed, but the script didnt crash( Failed to parse row 42)')
    logger.critical('CRITICAL: System failure( Database unreachable, shutting down pipeline)')


def demonstrate_exception_logging():
    # Shows how logger.exception() automatically captures tracebacks
    logger.info('Starting a risky data transformation step...')

    try:
        # Simulating a data error(division by zero or type casting error)
        bad_calculation = 100 / 0
    except ZeroDivisionError:
        # logger.exception logs an ERROR level message and appends the full stack trace
        logger.exception('Data transformation crashed due to a mathematical exception')


if __name__ == '__main__':
    logger.info('Pipeline Execution Started')

    demonstrate_log_levels()
    demonstrate_exception_logging()

    logger.info('Pipeline Execution Finished')
