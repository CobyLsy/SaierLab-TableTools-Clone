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

def get_primary(id):

    chebi_id = libchebipy.ChebiEntity(id)

    primary = chebi_id.get_parent_id()

    if primary == None:

        primary = id

    return primary


def find_predecessor(graph,id,classes = None):

    category = (None,None)

    primary = get_primary(id)



    if primary in classes:

        return (get_substrate_name(primary),primary)


    pre = [x for x in graph.successors(primary)]

    #print('Function Call: ',id,get_substrate_name(id),pre)

    primary_chebi = libchebipy.ChebiEntity(id)

    predecessor = primary_chebi.get_outgoings()


    while len(predecessor) != 0 :


        x = predecessor.pop(0)

        if x.get_type() == 'is_a':

            target_id = get_primary(x.get_target_chebi_id())


            print('{} {} {} {}({})'.format(x,get_substrate_name(id),x.get_type(),get_substrate_name(target_id),target_id))

            if target_id in classes:

                return (get_substrate_name(target_id),target_id)

            target_chebi = libchebipy.ChebiEntity(target_id)

            predecessor += target_chebi.get_outgoings()


    return category



if __name__ == "__main__":

    id = sys.argv[1]

    classes = set(['CHEBI:33696','CHEBI:33838','CHEBI:36976','CHEBI:23888','CHEBI:33281','CHEBI:18059','CHEBI:33229',
                    'CHEBI:25696','CHEBI:33575','CHEBI:24834','CHEBI:25697','CHEBI:36915','CHEBI:33709','CHEBI:16670',
                    'CHEBI:26672','CHEBI:31432','CHEBI:35381','CHEBI:50699','CHEBI:18154','CHEBI:72813','CHEBI:88061',
                    'CHEBI:10545','CHEBI:25367','CHEBI:24403','CHEBI:23357','CHEBI:17627','CHEBI:83821','CHEBI:17237',
                    'CHEBI:24870'])



    obopath = './chebi.obo'

    graph = build_ontology(obopath)
    print(find_predecessor(graph,id,classes=classes))




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



    ancestors = networkx.descendants(graph,primary)

    print(type(ancestors))
    print(ancestors)
    print(ancestors.intersection(classes))
    '''
