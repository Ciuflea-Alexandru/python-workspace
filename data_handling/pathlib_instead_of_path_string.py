import logging
from pathlib import Path

# 1. SETUP LOGGING
logs_dir = Path('data_handling/logs')
logs_dir.mkdir(parents=True, exist_ok=True)
log_file_path = logs_dir / 'pathlib_demo.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('PathlibDemo')


def demonstrate_pathlib():
    logger.info('Starting pathlib demonstration script...')

    base_dir = Path('data')
    data_dir = base_dir / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f'Current working dictionary: {Path.cwd()}')
    logger.info(f'Resolved data directory: {data_dir.resolve()}')

    sample_file = data_dir / 'sample_data.csv'
    sample_content = 'id,name,value\n1,Alpha,100\n2,Beta,200\n3,Gamma,300\n'

    sample_file.write_text(sample_content, encoding='utf-8')
    logger.info(f'Successfully created and wrote to file: {sample_file.name}')

    if sample_file.exists():
        logger.info(f'File name(stem): {sample_file.stem}')
        logger.info(f'File extension: {sample_file.suffix}')
        logger.info(f'Parent directory: {sample_file.parent}')
        logger.info(f'File size(bytes): {sample_file.stat().st_size}')

    content = sample_file.read_text(encoding='utf-8')
    logger.info(f'Read content back from file:\n{content.strip()}')

    logger.info(f'Scanning directory {data_dir} for csv files...')
    for file_path in data_dir.glob('*.csv'):
        logger.info(f'Found csv file via glob: {file_path.name}')

    sample_file.unlink()
    logger.info(f'Cleaned up demo file: {sample_file.name}')


if __name__ == '__main__':
    demonstrate_pathlib()
