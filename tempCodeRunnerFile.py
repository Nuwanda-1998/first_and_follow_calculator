finni = {'A': ['$'],
         'B': [['~', 'e'], ['f', '~'], 'a'],
         'C': [['f', '~'], 'a', ['f', '~'], [['~', 'e'], ['f', '~'], 'a']],
         'D': ['a', [['~', 'e'], ['f', '~'], 'a']]}


for key,value in finni.items():
    # flat_list = [item for sublist in value for item in sublist]
    flat_list = value
    final_flat_list = value
    rectify_needed = False
    while_ender = True
    while while_ender:
        while_ender = False
        for item in flat_list:
            if isinstance(item, str):
                pass
            else:
                rectify_needed = True
                while_ender = True
        if rectify_needed:
            flat_list = [item for sublist in flat_list for item in sublist]
            final_flat_list = flat_list
    print("Follows of {}: {}".format(key, final_flat_list))