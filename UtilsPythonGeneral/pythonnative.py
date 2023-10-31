def diff_between_two_dict(d1, d2):
    """
    Returns keys and or values from one dict that are not 
    found in the other WHERE DICT VALUE IS LIST - Doesnt work on string and int values!
    Ex. {a:[1,2,3],b:[1,2]} - {a:[1,3], c:[6,7]} = {a:[2],b:[1,2]}
    """
    diff_in_d1_not_in_d2={}
    for key, val in d1.items():
        if key in d2:
            res=set(val) - set(d2[key])
            if len(res)>0:
                diff_in_d1_not_in_d2[key]=res
            else:
                pass
        elif key not in d2:
            diff_in_d1_not_in_d2[key]=val

    return diff_in_d1_not_in_d2
