class ColorOutput:
    """
    This class help to colorize some tag for the print info
    """
    RESET_COLOR = '\x1b[0m'

    INFO_TAG = '\x1b[1;36m' + "[INFO]" + RESET_COLOR
    ERROR_TAG = '\x1b[1;31m' + "[ERROR]" + RESET_COLOR
    WARNING_TAG = '\033[1;33m' + "[WARN]" + RESET_COLOR
    DEBUG_TAG = '\x1b[1;35m' + "[DEBUG]" + RESET_COLOR
