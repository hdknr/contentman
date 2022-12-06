import json
from pathlib import Path

import click

from .contentful import Management
from .serializer import JSONEncoder


@click.group()
@click.pass_context
def content(ctx):
    pass


@content.command
@click.option("--path", default="/tmp")
@click.pass_context
def contenttype_list(ctx, path):
    """Content Type (list)"""
    env = ctx.obj["env"]
    man = Management(
        token=env.str("CONTENTFUL_MANAGEMENT_TOKEN"),
        space_id=env.str("CONTENTFUL_SPACE_ID"),
        space_name=env.str("CONTENTFUL_SPACNE_NAME"),
        environment_id=env.str("CONTENTFUL_ENVIRONMENT"),
    )
    contenttype_set = man.cotennttype_set
    for item in contenttype_set.items:
        data = item.to_json()
        with open(
            Path(path) / f"{man.space_name}.{data['sys']['id']}.json", "w"
        ) as out:
            json.dump(data, out, ensure_ascii=False, indent=2, cls=JSONEncoder)
