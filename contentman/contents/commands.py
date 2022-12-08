import json
from pathlib import Path

import click

from . import models
from .serializer import JSONEncoder


@click.group()
@click.pass_context
def content(ctx):
    pass


def dumps(data):
    return json.dumps(data, ensure_ascii=False, indent=2, cls=JSONEncoder)


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
            json.dump(data, out, ensure_ascii=False, indent=2, cls=JSONEncoder)


@content.command
@click.option("--content_type", "-t", default=None)
@click.pass_context
def entry_list(ctx, content_type):
    """Entry (list)"""
    env = ctx.obj["env"]
    model = factory(models.Entry, env)

    query = dict(
        content_type=content_type,
    )
    query["fields.pagePath.ja"] = "/"

    for item in model.list(**query).items:
        data = item.to_json()
        print(dumps(data["fields"]))
        print("\n\n\n")
