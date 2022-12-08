from pathlib import Path

import click

from . import models
from .serializer import dump, dumps
from .translation import find_node, translate


@click.group()
@click.pass_context
def content(ctx):
    pass


def factory(cls, env):
    return cls(
        token=env.str("CONTENTFUL_MANAGEMENT_TOKEN"),
        space_id=env.str("CONTENTFUL_SPACE_ID"),
        space_name=env.str("CONTENTFUL_SPACNE_NAME"),
        environment_id=env.str("CONTENTFUL_ENVIRONMENT"),
    )


@content.command
@click.option("--path", default="/tmp")
@click.pass_context
def contenttype_list(ctx, path):
    """Content Type (list)"""
    env = ctx.obj["env"]
    model = factory(models.ContentType, env)
    for item in model.list().items:
        data = item.to_json()
        with open(Path(path) / f"{model.space_name}.{data['sys']['id']}.json", "w") as out:
            dump(data, out)


@content.command
@click.argument("content_type")
@click.argument("queries", nargs=-1)
@click.pass_context
def entry_list(ctx, content_type, queries):
    """Entry (list)"""
    env = ctx.obj["env"]
    model = factory(models.Entry, env)

    query = dict((("content_type", content_type),) + tuple(i.split("=") for i in queries))

    for item in model.list(**query).items:
        data = item.to_json()
        print(dumps(data))


@content.command
@click.argument("excludes", nargs=-1)
@click.pass_context
def entry_translate(ctx, excludes):
    """Entry Translate"""
    from functools import reduce

    def _transale(attributes, path, lang_to):
        splited = path.split(".")
        lang_from = splited[-1]
        node = reduce(lambda a, i: a[i], splited[:-1], attributes)
        node[lang_to] = translate(node[lang_from], lang_from, lang_to)

    env = ctx.obj["env"]
    model = factory(models.Entry, env)

    query = dict((("content_type", "page"), ("fields.pagePath.ja", "/debug")))

    lang_from = "ja"
    lang_to = "en"
    root = "fields"
    for item in model.list(**query).items:
        data = item.to_json()
        paths = []

        find_node(paths, data[root], lang_from=lang_from, lang_to=lang_to, path=root)
        results = set(paths) - set(excludes)
        if not results:
            continue

        for path in results:
            _transale(data, path, lang_to)

        item.update(attributes=data)
