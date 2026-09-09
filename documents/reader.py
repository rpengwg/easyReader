import os

from .odt_reader import read_odt



def read_document(path):


    ext=os.path.splitext(path)[1].lower()



    if ext==".odt":

        return read_odt(path)



    if ext==".txt":

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()



    return None
