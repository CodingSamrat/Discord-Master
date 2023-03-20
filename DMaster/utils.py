from time import strftime
from colorama import Fore, Style


class Alart:
    DEBUG = "DEBUG"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"


class LOG:

    @staticmethod
    def debug(*args, **kwargs):
        my_dict: dict = kwargs
        text = LOG.__get_text(my_dict)

        # Check if text is empty
        if text:
            # Generating final string
            final_msg = LOG.__get_final_msg(Alart.DEBUG, text)

            # Printing to the console
            print(final_msg)

    @staticmethod
    def success(*args, **kwargs):
        my_dict: dict = kwargs
        text = LOG.__get_text(my_dict)

        # Check if text is empty
        if text:
            # Generating final string
            final_msg = LOG.__get_final_msg(Alart.SUCCESS, text)

            # Printing to the console
            print(final_msg)

    @staticmethod
    def warning(*args, **kwargs):
        my_dict: dict = kwargs
        text = LOG.__get_text(my_dict)

        # Check if text is empty
        if text:
            # Generating final string
            final_msg = LOG.__get_final_msg(Alart.WARNING, text)

            # Printing to the console
            print(final_msg)

    @staticmethod
    def error(*args, **kwargs):
        my_dict: dict = kwargs
        text = LOG.__get_text(my_dict)

        # Check if text is empty
        if text:
            # Generating final string
            final_msg = LOG.__get_final_msg(Alart.ERROR, text)

            # Printing to the console
            print(final_msg)

    @staticmethod
    def __get_final_msg(alert: str, text: str) -> str:
        # Getting Log time
        current_time = strftime("%Y-%m-%d %H:%M:%S")

        # msg
        final_msg = ""

        # Set default Color
        color = Fore.WHITE

        # Set time Color
        current_time = Fore.CYAN + Style.DIM + current_time + Style.NORMAL

        # Set Color for Alerts
        if alert == Alart.DEBUG:
            color = Fore.WHITE
            final_msg = f"{current_time} {color + Style.BRIGHT} [{Alart.DEBUG}]{Style.NORMAL} {text}{Fore.WHITE}"
        elif alert == Alart.SUCCESS:
            color = Fore.GREEN
            final_msg = f"{current_time} {color + Style.BRIGHT} [{Alart.SUCCESS}]{Style.NORMAL} {text}{Fore.WHITE}"
        elif alert == Alart.WARNING:
            color = Fore.YELLOW
            final_msg = f"{current_time} {color + Style.BRIGHT} [{Alart.WARNING}]{Style.NORMAL} {text}{Fore.WHITE}"
        elif alert == Alart.ERROR:
            color = Fore.RED
            final_msg = f"{current_time} {color + Style.BRIGHT} [{Alart.ERROR}]{Style.NORMAL} {text}{Fore.WHITE}"

        return final_msg

    @staticmethod
    def __get_text(my_dict: dict) -> str:
        text: str = ""
        if "TEXT" in my_dict.keys() or "text" in my_dict.keys():
            if "TEXT" in my_dict.keys():
                text = my_dict['TEXT']

            elif "text" in my_dict.keys():
                text = my_dict['text']

        return text


