def find_node(results, node, path, lang_from="ja", lang_to="en"):
    if isinstance(node, dict):
        for key, value in node.items():
            current_path = f"{path}.{key}"
            if key == lang_from and lang_to not in node:
                results.append(current_path)
            find_node(results, value, current_path, lang_from=lang_from, lang_to=lang_to)



class Translator:
    pass
