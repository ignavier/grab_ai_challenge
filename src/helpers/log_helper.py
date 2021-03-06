import sys
import logging
import pathlib
from datetime import datetime
from pytz import timezone, utc


class LogHelper(object):
    """
    Helper class to configure logger
    """
    log_format = '%(asctime)s %(levelname)s - %(name)s - %(message)s'

    @staticmethod
    def setup(log_path, level_str='INFO'):
        logging.basicConfig(
             filename=log_path,
             level=logging.getLevelName(level_str),
             format= LogHelper.log_format,
         )

        def customTime(*args):
            utc_dt = utc.localize(datetime.utcnow())
            my_tz = timezone("Asia/Hong_Kong")
            converted = utc_dt.astimezone(my_tz)
            return converted.timetuple()

        logging.Formatter.converter = customTime

        # Set up logging to console
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(logging.Formatter(LogHelper.log_format))
        # Add the console handler to the root logger
        logging.getLogger('').addHandler(console)

        # Abit hacky, redirect sys.stdout for logging (needed to log lightgbm training verbose)
        # Refer to https://github.com/Microsoft/LightGBM/issues/1493
        sys.stdout = open(log_path, 'a', 1)

        # Log for unhandled exception
        logger = logging.getLogger(__name__)
        sys.excepthook = lambda *ex: logger.critical('Unhandled exception', exc_info=ex)

        logger.info('Finished configuring logger.')