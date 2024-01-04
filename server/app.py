import asyncio

from src import main
from src.utils.logging import create_logger, get_root_logger

from dotenv import load_dotenv

if __name__ == '__main__':
    logger = create_logger(__name__)
    get_root_logger()
    load_dotenv()
    asyncio.run(main())