from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET


def read_odt(path):
    """Extract text from LibreOffice ODT document."""
    path = Path(path)
    if not path.exists():
        return ""

    with zipfile.ZipFile(path, "r") as z:
        xml_data = z.read("content.xml")

    root = ET.fromstring(xml_data)

    texts = []
    for elem in root.iter():
        if elem.text:
            texts.append(elem.text)

    return " ".join(texts)
