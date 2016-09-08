from math import ceil, floor
from pprint import pprint as pp
import subprocess as sbp
import time
import tempfile as tmp

import nltk
from nltk.corpus import wordnet as wn
from graphviz import Digraph

# just a math helper function
def float_round(num, places=0, direction=floor):
        return direction(num * (10**places)) / float(10**places)


# Generating the hyponyms
def recur(ss, prefix='', parent_node=''):
        
        ssk = str(ss.name())
        if parent_node == '':
            hypernyms(ss)
        dot.edge_attr.update(arrowhead='normal') 
        pp(prefix + ': ' + ss.name())
        for sss in ss.hyponyms():
            new_node= str(sss.name())
            if parent_node == '':
                dot.node(ssk)
                dot.attr('node', shape='ellipse',fontsize = '12')
            dot.node(new_node)
            w1 = wn.synset(ssk)
            w2 = wn.synset(new_node)
            inter = float_round(w1.wup_similarity(w2), 3)
            simRate = " " +  str(inter)
            dot.edge(ssk, new_node, constraint='true', label=simRate)
            recur(sss, prefix=prefix + ': ' + ss.name(), parent_node=ssk)

node_cache = set()
# Generating the hypernyms
def hypernyms(ss, prefix='', childNode=''):
   
 #   dot.edge_attr.update(arrowhead='normal', arrowsize='1')
    
    sah = str(ss.name())
    pp(prefix + ': ' + ss.name())
    for sd in ss.hypernyms():

        new_node = str(sd.name())
        if new_node in node_cache:
            continue
        if childNode== '':
            dot.node(sah)
            dot.attr('node', shape='box', fontsize='12')
        if dot.node(new_node):
            continue 
        else:
            node_cache.add(new_node)
            dot.node(new_node)
            w1 = wn.synset(new_node)
            w2 = wn.synset(sah)
            inter = float_round(w1.wup_similarity(w2), 3)
            simRate = " " + str(inter)

            dot.edge(new_node, sah, constraint='true', label=simRate, arrowhead='normal')
            hypernyms(sd, prefix=prefix+ ': ' + ss.name(), childNode=sah)

if __name__ == "__main__":
    
    name = input("PLEASE ENTER A WORD. ")
    sense = int(input("SENSE? [IF IN DOUBT, PICK 0] "))
    flatten_deg = input("DEGREE OF FLATTEN-ITUDE? [IF IN DOUBT, PICK 6]")
    gv_f, gv_fname = tmp.mkstemp()
    png_fname = 'test-output/tree-{}-{}.png'.format(name, sense)

    
    dot = Digraph('structs', comment='Semantic Relationship Tree with WUP Similarity Values')
    dot.graph_attr.update(smoothing = "avg_dist", splines = 'polyline')
   
    dot.attr('node', shape='doubleoctagon', fontsize='22')
    recur(wn.synsets(name)[sense])
    
    dot.body.append(r'label = "\n\n Semantic Relationship Diagram with WUP Similarity Values"')
    dot.body.append('fontsize=30')
    
    #uncomment to show graph information
    #print(dot.source)
    dot.render('test-output/tree-{}{}.pdf'.format(name, sense), view=False)
    dot.render(gv_fname, view=False)
   

    gv_process = sbp.Popen(['unflatten', '-l', flatten_deg, gv_fname], stdout=sbp.PIPE)
    sbp.run(['dot', '-Tpng', '-o', png_fname], stdin=gv_process.stdout)
    

    #Command line prompt to make more aesthetically pleasing
    #  unflatten -l 6 test.gv | dot -Tpng -o wide2.png 
    
