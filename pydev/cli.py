# coding=utf-8

import click

from .sketch_dir import generate_sketch


@click.group()
@click.option("--verbose/--no-verbose", default=False)
@click.pass_context
def main(ctx, verbose):
    ctx.ensure_object(dict)

    ctx.obj["verbose"] = verbose


@main.command()
@click.argument("file", type=click.File(mode="r"))
@click.pass_context
def sketchdir(ctx, file):
    generate_sketch(file)
