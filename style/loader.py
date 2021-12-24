import os


class StyleLoader:
    @classmethod
    def load_style(cls, filename="style/style.css"):
        f = open(filename, "r")
        style = f.read()
        f.close()
        return style