from jsonschema import RefResolver

import glob
import logging
import os
import re
import yaml

MOD_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


class GDCDictionary(object):

    _metaschema_path = 'metaschema.yaml'
    _definitions_paths = [
        '_definitions.yaml',
        '_terms.yaml',
    ]

    logger = logging.getLogger("GDCDictionary")

    def __init__(self, lazy=False, root_dir=None, definitions_paths=None,
                 metaschema_path=None):
        """Creates a new dictionary instance.

        :param root_dir: The directory to find schemas
        :param metaschema_path: The metaschema to validate schemas with
        :param definitions_paths: Paths to resolve $ref to
        :param lazy: If true, wait to load dictionary

        """

        self.root_dir = (root_dir or os.path.join(MOD_DIR, 'schemas'))
        self.metaschema_path = metaschema_path or self._metaschema_path
        self.definitions_paths = definitions_paths or self._definitions_paths
        self.exclude = [self.metaschema_path] + self.definitions_paths
        self.schema = dict()
        if not lazy:
            self.load()

    def load(self):
        """Load and reslove all schemas"""

        self.metaschema = self.load_yaml_schema(self.metaschema_path)
        self.definitions = {}
        self.resolvers = {
            '{}'.format(path):
            RefResolver('{}#'.format(path), self.load_yaml_schema(path))
            for path in self.definitions_paths
        }
        self.load_root_dir()

        map(self.resolve_all, self.schema.values())

    def resolve_all(self, root, doc=None):
        doc = doc or root

        if isinstance(root, dict):
            modified = False
            for k, v in root.items():
                print(k)
                if k == '$ref':

                    print(k, v)
                    base, ref = v.split('#')
                    ref = ref.replace('/', '')
                    print(base, ref)

                    if base == '':
                        resolver = RefResolver('#', doc)
                    else:
                        resolver = self.resolvers[base]

                    referrer, resolution = resolver.resolve(v)
                    root.pop(k)
                    root.update(resolution)
                    modified = True

            for k, v in root.items():
                self.resolve_all(k, doc)

        elif isinstance(root, list):
            for item in root:
                self.resolve_all(root, doc)

    def load_root_dir(self):
        cdir = os.getcwd()
        os.chdir(self.root_dir)
        for name in glob.glob("*.yaml"):
            if name not in self.exclude:
                schema = self.load_yaml_schema(name)
                self.schema[schema['id']] = schema
        os.chdir(cdir)

    def load_yaml_schema(self, name):
        full_path = os.path.join(self.root_dir, name)
        with open(full_path, 'r') as f:
            return yaml.load(f)


gdcdictionary = GDCDictionary()
