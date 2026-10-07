# main.py
import logging
from Egyptian_legal_rag.utils.logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

def main():
    logger.info("ℹ️ start project")

if __name__ == "__main__":
    main()