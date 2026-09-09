from odf.opendocument import load
from odf.text import P


def read_odt(path):

    doc = load(path)


    paragraphs = doc.getElementsByType(
        P
    )


    result=[]


    for p in paragraphs:

        text=""

        for node in p.childNodes:

            if hasattr(node,"data"):

                text += node.data


        if text.strip():

            result.append(
                text.strip()
            )


    return "\n".join(result)
