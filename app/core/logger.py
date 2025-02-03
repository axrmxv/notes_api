import logging


def get_logger(
    name: str = "app",
    log_file: str = "app.log",
    level: int = logging.INFO
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Проверка на наличие обработчиков, чтобы избежать дублирования
    if not logger.handlers:
        # Обработчик для записи логов в файл
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)

        # Формат логов
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger
