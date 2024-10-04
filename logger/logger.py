from loguru import logger
import os
from pathlib import Path


class Logger:
    def __init__(self):
        self.log_path = os.path.join(Path(__file__).resolve().parent.parent, "log")
        self.stdout_filename = "access.log"

    def log(self):
        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)

        # 日志文件
        log_stdout_file = os.path.join(self.log_path, self.stdout_filename)

        log_config = dict(rotation='10 MB', retention='15 days', compression='tar.gz', enqueue=True)

        # loguru 默认都会打印打控制台，只有 add 后，才会存储到文件

        # stdout
        logger.add(
            log_stdout_file,
            level='INFO',
            filter=lambda record: record['level'].name == 'INFO' or record['level'].no <= 25,
            **log_config,
            backtrace=False,
            diagnose=False,
        )

        # stderr
        logger.add(
            log_stdout_file,
            level='ERROR',
            filter=lambda record: record['level'].name == 'ERROR' or record['level'].no >= 30,
            **log_config,
            backtrace=True,
            diagnose=True,
        )

        return logger


log = Logger().log()
