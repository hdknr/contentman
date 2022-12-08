def walk_translate(translated, node, path, lang_from="ja", lang_to="en", excludes=None):
    for key, value in node.items():
        current_path = f"{path}.{key}"
        translate_path = f"{path}.{lang_to}"
        if isinstance(value, dict):
            walk_translate(translated, value, current_path, lang_from=lang_from, lang_to=lang_to, excludes=excludes)
            continue
        if key == lang_from:
            if lang_to not in node and (not excludes or current_path not in excludes):
                translated[translate_path] = value + f".{lang_to}"  # TODO


class Translator:
    pass
