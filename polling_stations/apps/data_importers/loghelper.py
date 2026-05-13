import logging
import pprint


class LogHelper:
    logger = None

    def __init__(self, verbosity, stream=None):
        logformat = "%(levelname)s: %(message)s"
        config_kwargs = {"format": logformat}

        if stream:
            config_kwargs["stream"] = stream

        logging.basicConfig(**config_kwargs)

        logger = logging.getLogger(__name__)
        if verbosity == 0:
            logger.setLevel(logging.ERROR)
        elif verbosity == 1:
            logger.setLevel(logging.WARNING)
        elif verbosity == 2:
            logger.setLevel(logging.INFO)
        elif verbosity >= 3:
            logger.setLevel(logging.DEBUG)
        self.logger = logger

    def log_message(self, level, message, variable=None, pretty=False):
        log_str = ""
        if variable:
            if pretty:
                try:
                    log_str = message % pprint.pformat(variable._asdict(), indent=4)
                except AttributeError:
                    log_str = message % pprint.pformat(variable, indent=4)
            else:
                log_str = message % variable
        else:
            log_str = message

        self.logger.log(level, log_str)
