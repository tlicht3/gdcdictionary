from jinja2 import Environment
import os
import os.path
import yaml
from sys import argv, stdout
from pdb import set_trace

default_gdir="/Users/jensenma/Code/GDC/gdcdictionary/gdcdictionary/glossary"
default_sdir="/Users/jensenma/Code/GDC/gdcdictionary/gdcdictionary/schemas"

class Glossary:
    def __init__(self,gdir=default_gdir):
        self.gdir = gdir
        self.glossary = {}
        term_files = [ fn for fn in os.listdir(gdir) if fn.endswith("yaml") ]
        for fn in term_files:
            try:
                yml = yaml.load( open(os.path.join(gdir,fn)).read() )
                self.glossary[yml['term']] = yml
            except:
                pass
    def get_term(self, term):
        try:
            return self.glossary[term]
        except KeyError:
            return
    def get_definition(self, term):
        try:
            return self.glossary[term]['termdef']['definition']
        except KeyError:
            return
    def get_cde_info(self,term):
        try:
            return self.glossary[term]['termdef']['source']['cde']
        except KeyError:
            return

class MakeDictMD:
    def __init__(self,gloss=Glossary(),template="dict_template.md"):
        self.jinja_env = Environment(trim_blocks=True,
                                     lstrip_blocks=True,
                                     extensions=['jinja2.ext.loopcontrols'])
        self.gloss = gloss
        self.template = self.jinja_env.from_string( open( template ).read() )

    def render_entry(self,yobj,has_terms=True):
        return self.template.render(obj=yobj,gloss=self.gloss,has_terms=has_terms)


if __name__=='__main__':
    mdmd = MakeDictMD()
    dict_files = argv[1:] if len(argv[1:]) else [ fn for fn in os.listdir(default_sdir) if fn.endswith("yaml") ]
    for fn in dict_files:
        if fn.find("metaschema") >= 0 or fn.find("_definitions") >= 0:
            continue
        obj = yaml.load( open( os.path.join(default_sdir, fn) ).read() );
        try:
            f= stdout if len(argv[1:]) else open(obj['id']+".md","w");
            term = [ prop for prop in obj['properties'] if mdmd.gloss.get_term(prop) ]
            print >> f, mdmd.render_entry(obj,has_terms=term)
        except Exception as e:
            print "problem with {name}".format(name=obj['id'])
            print e
        
