import obonet
import networkx as nx
import sys
import libchebipy

'''
Build Ontology
'''

def build_ontology(obopath):

    return obonet.read_obo(obopath)

'''
Get the Name Associated with a ChEBI ID
'''

def get_substrate_name(id):

    id = libchebipy.ChebiEntity(id)

    return id.get_name()

'''
Find the Predecessor
'''

def find_predecessor(graph,id,classes = None):

    chebi_id = libchebipy.ChebiEntity(id)
    primary = chebi_id.get_parent_id()


    if primary == None:

        primary = id


    if primary in classes:

        return (get_substrate_name(primary),primary)


    pre = graph.successors(primary)


    heiriarchy = []

    for x in pre:

        heiriarchy.append(x)

        if classes != None:

            if x in classes:

                return (get_substrate_name(x),x)

    print(id,get_substrate_name(id),heiriarchy)

    return [(get_substrate_name(x),x) for x in heiriarchy]



if __name__ == "__main__":

    classes = set(['CHEBI:33696','CHEBI:33838','CHEBI:36976','CHEBI:23888','CHEBI:33281','CHEBI:18059','CHEBI:33229',
                    'CHEBI:25696','CHEBI:33575','CHEBI:24834','CHEBI:25697','CHEBI:36915','CHEBI:33709','CHEBI:16670',
                    'CHEBI:26672','CHEBI:31432','CHEBI:35381','CHEBI:50699','CHEBI:18154','CHEBI:72813','CHEBI:88061',
                    'CHEBI:10545','CHEBI:25367','CHEBI:24403','CHEBI:23357','CHEBI:17627','CHEBI:83821','CHEBI:17237'])



    obopath = './chebi.obo'

    graph = build_ontology(obopath)
    print(find_predecessor(graph,'CHEBI:8345',classes=classes))

    '''

    graph = obonet.read_obo(obopath)

    id = libchebipy.ChebiEntity('CHEBI:8345')
    primary = id.get_parent_id()
    print(primary)

    pre = graph.successors(primary)

    for x in pre:

        if x in classes:

            print(x)
            break
    '''

    '''
    ancestors = networkx.descendants(graph,primary)

    print(type(ancestors))
    print(ancestors)
    print(ancestors.intersection(classes))
    '''
