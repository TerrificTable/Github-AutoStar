from colorama import Fore
import os


r = Fore.RED
rl = Fore.LIGHTRED_EX
g = Fore.GREEN
gl = Fore.LIGHTGREEN_EX
b = Fore.BLUE
bl = Fore.LIGHTBLUE_EX
c = Fore.CYAN
cl = Fore.LIGHTCYAN_EX
m = Fore.MAGENTA
ml = Fore.LIGHTMAGENTA_EX
y = Fore.YELLOW
yl = Fore.LIGHTYELLOW_EX
w = Fore.WHITE
wl = Fore.LIGHTWHITE_EX


def title(text: str):
    os.system(
        f"title Github Autostar  ^|  {text}  ^|  by TerrificTable55™#5297 ")


class debug():
    @staticmethod
    def working(text):
        print(f"{w}[{g}={w}] {text}")

    @staticmethod
    def error(text):
        print(f"{w}[{r}-{w}] {text}")

    @staticmethod
    def warning(text):
        print(f"{w}[{rl}!{w}] {text}")
