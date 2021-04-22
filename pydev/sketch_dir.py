# encoding=utf-8

import queue
import subprocess
from enum import Enum
from typing import List

import click
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class Node:
    def __init__(self, name, context=None):
        self.name = name
        self.context = context

    def create(self):
        raise NotImplementedError()


class DirectoryNode(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self):
        subprocess.run(f"mkdir {self.name}", executable="")


class NodeType(Enum):
    FILE = 1

    DIRECTORY = 2

    @classmethod
    def get_node_type(cls, name):
        return {
            "file": cls.FILE,
            "dir": cls.DIRECTORY,
        }[name]


class GitConfig:
    def __init__(
        self,
        repo=None,
        user_name=None,
        user_email=None,
        readme=None,
        license=None,
        gitignore=None,
        **kwargs,
    ):
        self.repo = repo
        self.user_name = user_name
        self.user_email = user_email
        self.readme = readme
        self.license = license
        self.gitignore = gitignore


class Node:
    def __init__(self, name, node_type, git):
        self.name = name
        self.node_type = NodeType.get_node_type(node_type)
        self.children = []

        if git:
            self.git = GitConfig(**git)

    def add_child(self, child):
        self.children.append(child)


def load_config_from_dict(config):
    root = Node(config["name"], config["type"], config.get("git"))
    for sub_node in config.get("nodes", []):
        node = load_config_from_dict(sub_node)
        root.add_child(node)

    return root


class SketchGenerator:
    def __init__(self, config):
        ...

    def git(self, repo, fullname, readme, license, gitignore):
        ...


def generate_sketch(file):
    config = load(file, Loader=Loader)
    root = load_config_from_dict(config["root"])
    click.echo(root)
