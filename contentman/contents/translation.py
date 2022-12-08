"""
poetry add "googletrans>=4.0.0rc1"
"""
from googletrans import Translator
from logging import getLogger

logger = getLogger()

_translator = Translator()


def find_node(results, node, path, lang_from="ja", lang_to="en"):
    if isinstance(node, dict):
        for key, value in node.items():
            current_path = f"{path}.{key}"
            if key == lang_from and lang_to not in node:
                results.append(current_path)
            find_node(results, value, current_path, lang_from=lang_from, lang_to=lang_to)


def translate(data, lang_from, lang_to, parent=None):
    if isinstance(data, dict):
        return dict((key, translate(value, lang_from, lang_to, parent=data)) for key, value in data.items())
    if isinstance(data, list):
        return [translate(i, lang_from, lang_to) for i in data]
    if parent and parent.get("nodeType", None) == "text" and isinstance(data, str) and data:
        try:
            res = _translator.detect(data)
            if res.lang != lang_to:
                data = _translator.translate(data, src=lang_from, dest=lang_to).text
        except Exception as e:
            logger.error(str(e))

    return data


class Translator:
    pass
