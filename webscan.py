# coding: utf-8
import random
from pyfiglet import Figlet,FigletFont
from lib.cli import main

if __name__ == '__main__':
    bannertype=FigletFont().getFonts()
    while True:
        i=random.randint(0, len(bannertype))
        if i!=51 and i!=38:
            break
    f = Figlet(font=bannertype[i])
    print(f.renderText("webscan"))
    print("    版本号 0.9.0 / version 0.9.0\n")
    main()
