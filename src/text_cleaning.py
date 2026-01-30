import re


def text_cleaning(text):
    texts = text.strip()
    texts = re.sub(r"[ \t]+", " ", texts)
    texts = re.sub(r"\s+([.,!?;:])", r"\1", texts)
    texts = re.sub(r"([.,!?;:])[ \t]*([^\s])", r"\1 \2", texts)
    texts = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", texts)
    texts = re.sub(r"[\u200b\u200c\u200d\u002a\u2217\u22c6\u2731\ufeff�#]", "", texts)

    return texts
