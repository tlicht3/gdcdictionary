import sys
sys.path.append('.');
import makemd
from jinja2 import Environment
import os
import os.path
import yaml
from sys import argv, stdout
from pdb import set_trace


if __name__ == '__main__':
    mdmd = makemd.MakeDictMD(template="gloss_template.md.jj")
    f = stdout if not len(argv[1:]) else open(argv[1],"w")
    print >> f, mdmd.render_entry(None)
    
