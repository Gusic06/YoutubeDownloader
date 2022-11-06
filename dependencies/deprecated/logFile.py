import logging as log
from datetime import datetime
def logFile():
    sysTime = str(datetime.now())
    logName = sysTime.replace(" : ", "_")
    log.basicConfig(level=log.INFO, filename=logName+".log", filemode="w")
if __name__ == "__main__":
    logFile()