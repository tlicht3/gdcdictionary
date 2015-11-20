from jinja2 import Environment
import os
import os.path
import yaml
#from pdb import set_trace

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

env = Environment(trim_blocks=True,
                  lstrip_blocks=True)
gloss = Glossary()
objname = "demographic"
tmplf = "dict_template.md"
obj = yaml.load( open( os.path.join(default_sdir, objname+".yaml") ).read() )

properties = obj['properties'].keys()

# get terms

try:
    term = yaml.load( open( "../../glossary/"+objname+".yaml").read() )
except:
    term ={}

template = env.from_string( open( tmplf ).read() )
print template.render(obj=obj,gloss=gloss)
