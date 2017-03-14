#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
author:     haifeng.lv
date:       2016/5/16
descirption:自定制logger模块
"""
import logging
from logging.handlers import TimedRotatingFileHandler

'''
loggerName:Logger 标识。
loggerFile:自定制log的存储路径。
isPrint:是否在控制台显示，默认是不显示。
'''


class MoJiLogger(object):
    def __init__(self, logger_name, logger_file, is_print=False, level=logging.DEBUG):
        self.loggerName = logger_name
        self.loggerFile = logger_file
        self.isPrint = is_print
        self.level = level

    def Logger(self):
        logger = logging.getLogger(self.loggerName)
        logger.setLevel(self.level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')
        th = TimedRotatingFileHandler(filename=self.loggerFile, when="midnight", backupCount=15)
        th.setFormatter(formatter)
        logger.addHandler(th)
        # fh = logging.FileHandler(self.loggerFile)
        # fh.setFormatter(formatter)
        # logger.addHandler(fh)

        if self.isPrint:
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            logger.addHandler(ch)
        return logger


project_log = MoJiLogger("Project", "../logs/project.log", is_print=True).Logger()

if __name__ == "__main__":
    project_log = MoJiLogger("Project", "../logs/project.log", is_print=True).Logger()
    project_log.info("info message")
    project_log.debug("debug message")
    project_log.error("error message")
