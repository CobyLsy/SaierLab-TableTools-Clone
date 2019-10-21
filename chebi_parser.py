import sys
import libchebipy

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


def find_predecessor(id,classes = None):


    category = (None,None)

    primary = get_primary(id)

    #print('Function Call: ',primary,get_substrate_name(primary))

    if primary in classes:

        return (get_substrate_name(primary),primary)


    primary_chebi = libchebipy.ChebiEntity(primary)

    predecessor = primary_chebi.get_outgoings()


    while len(predecessor) != 0 :


        x = predecessor.pop(0)

        if x.get_type() == 'is_a':

            target_id = get_primary(x.get_target_chebi_id())


            #print('{} {} {} {}({})'.format(x,get_substrate_name(id),x.get_type(),get_substrate_name(target_id),target_id))

            if target_id in classes:

                return (get_substrate_name(target_id),target_id)

            target_chebi = libchebipy.ChebiEntity(target_id)

            predecessor += target_chebi.get_outgoings()


    return category

def find_role(id,classes=None):

    role = (None,None)

    primary = get_primary(id)

    if primary in classes:

        return (get_substrate_name(primary),primary)

    primary_chebi = libchebipy.ChebiEntity(id)

    predecessor = primary_chebi.get_outgoings()



    for pre in predecessor:

        if pre.get_type() =='has_role':

            target_id = get_primary(pre.get_target_chebi_id())


            if target_id in classes:

                return (get_substrate_name(target_id),target_id)

            role = find_predecessor(target_id,classes=classes)

            print(role)

            '''
            if role is not (None,None):

                return role
            '''

    return role


if __name__ == "__main__":

    id = sys.argv[1]

    ce_classes = set(['CHEBI:33696','CHEBI:33838','CHEBI:36976','CHEBI:23888','CHEBI:33281','CHEBI:18059','CHEBI:33229',
                    'CHEBI:25696','CHEBI:33575','CHEBI:24834','CHEBI:25697','CHEBI:36915','CHEBI:33709','CHEBI:16670',
                    'CHEBI:26672','CHEBI:31432','CHEBI:35381','CHEBI:50699','CHEBI:18154','CHEBI:72813','CHEBI:88061',
                    'CHEBI:10545','CHEBI:25367','CHEBI:24403','CHEBI:23357','CHEBI:17627','CHEBI:83821','CHEBI:17237',
                    'CHEBI:24870'])

    role_classes = set(['CHEBI:23888','CHEBI:33281','CHEBI:26672','CHEBI:31432','CHEBI:33229','CHEBI:23357','CHEBI:25212'])


    print(find_predecessor(id,classes=ce_classes))
    print(find_role(id,classes=role_classes))




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
