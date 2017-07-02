#! -*- encoding:utf-8 -*-
import logging
from logging.config import fileConfig

fileConfig("log_conf.ini")

logger = logging.getLogger("mpTaskRunLog")

def getlog(logname):
    logger.debug("Can not see me")
    logger.info("I am Info level")
    logger.warn("!!I AM WARN!!")
    logger.error(">> SHIT ERR HAPPENS <<")

if __name__ == "__main__":
    getlog("Shit")
