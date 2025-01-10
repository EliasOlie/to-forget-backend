from loguru import logger
import sys
import logging

def setup_logger():
    """
    Configura o logger para capturar logs do FastAPI com Loguru.
    """
    # Remove o handler padrão do Loguru
    logger.remove()

    # Adiciona um novo handler para o Loguru com saída para o console
    logger.add(
        sys.stdout,
        level="DEBUG",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    )

    # Redirecionar logs do sistema de logging padrão para o Loguru
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            loguru_level = {
                50: "CRITICAL",
                40: "ERROR",
                30: "WARNING",
                20: "INFO",
                10: "DEBUG",
                0: "NOTSET",
            }.get(record.levelno, "INFO")
            logger.log(loguru_level, record.getMessage())

    logging.basicConfig(handlers=[InterceptHandler()], level=logging.DEBUG)

    # Capturar logs de bibliotecas específicas
    for logger_name in ("uvicorn", "uvicorn.access"):
        logging.getLogger(logger_name).handlers = [InterceptHandler()]
        logging.getLogger(logger_name).propagate = False

    logger.info("Loguru configurado com sucesso!")
