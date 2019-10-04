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
Helper Function to Perform Search

def search(graph,id,queue,classes):

    while len(queue) != 0:

        curr = queue.pop(0)

        if curr in classes:

            return (get_substrate_name(curr),curr)

        chebi_id = libchebipy.ChebiEntity(curr)

        for parent in chebi_id.get_outgoings():

            print('Parent: ',parent,parent.get_type())

            if parent.get_target

            if parent.get_type() == 'is_a':
'''


'''
Find the Predecessor
'''
'''
def find_predecessor(graph,id,classes = None):

    chebi_id = libchebipy.ChebiEntity(id)
    primary = chebi_id.get_parent_id()

    if primary == None:

        primary = id

    if primary in classes:

        #print('EARLY EXIT')

        return (get_substrate_name(primary),primary)


    predecessor = [x for x in graph.successors(primary)]

    while len(predecessor) != 0 :

        pre = predecessor.pop(0)

        if pre in classes:

            return (get_substrate_name(pre),pre)

        predecessor += [x for x in graph.successors(pre)]

'''
def find_predecessor(graph,id,classes = None):

    category = (None,None)

    chebi_id = libchebipy.ChebiEntity(id)
    primary = chebi_id.get_parent_id()


    if primary == None:

        primary = id


    if primary in classes:

        #print('EARLY EXIT')

        return (get_substrate_name(primary),primary)


    #pre = [x for x in graph.successors(primary)]

    #print('Function Call: ',id,get_substrate_name(id),pre)

    primary_chebi = libchebipy.ChebiEntity(id)

    predecessor = primary_chebi.get_outgoings()


    while len(predecessor) != 0 :

        x = predecessor.pop(0)

        if x.get_type() == 'is_a':

            target_id = x.get_target_chebi_id()

            #print('{} {} {}'.format(get_substrate_name(id),x.get_type(),get_substrate_name(target_id)))

            if target_id in classes:

                return (get_substrate_name(target_id),target_id)

            target_chebi = libchebipy.ChebiEntity(target_id)

            predecessor += target_chebi.get_outgoings()

    '''
    if classes != None:


        for x in pre:


            #print(x)

            if x in classes:


                return (get_substrate_name(x),x)



            chebi_id = libchebipy.ChebiEntity(x)


            for parent in chebi_id.get_outgoings():

                print('Parent: ',parent,parent.get_type())

                if parent.get_type() == 'is_a':


                    return find_predecessor(graph,x,classes=classes)
    '''


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
