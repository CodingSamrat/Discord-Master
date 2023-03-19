from time import strftime


class LOG:
    DEBUG = "DEBUG"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"

    def __init__(self, *args, **kwargs):
        current_time = strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time} {args[1]} {args[0].__class__.__name__} {kwargs['TEXT']}")
