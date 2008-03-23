from numarray import matrix

def ecintersection(*devides):
    if len(devides) == 0:
        return 1
    # construct set
    complete_set = set()
    for ec in devides[0]:
        for element in ec:
            complete_set.add(element)
    print complete_set
    ec_array = []
    ec_dict_template = {}
    for element in complete_set:
        ec_dict_template[element] = set()
    for devide in devides:
        ec_dict = ec_dict_template.copy()
        for ec in devide:
            ec_set = set()
            for element in ec:
                ec_set.add(element)
            for element in ec:
                ec_dict[element] = ec_dict[element].union(ec_set)
        ec_array.append(ec_dict)
    #print ec_array
    
    ec_insect = {}
    for element in complete_set:
        for ec_dict in ec_array:
            try:
                ec_insect[element]
            except KeyError:
                ec_insect[element] = ec_dict[element]
                continue
            ec_insect[element].intersection_update(ec_dict[element])
    print ec_insect
    
    # constrct ec
    
# test

ecintersection([[0,1], [2,3,4], [5]], [[0],[1,2], [3,4], [5]])
