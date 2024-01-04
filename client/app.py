import asyncio

from dotenv import load_dotenv

from src import main
from src.utils.logging import create_logger, get_root_logger


if __name__ == '__main__':
    logger = create_logger(__name__)
    get_root_logger()
    load_dotenv(".env")
    asyncio.run(main())