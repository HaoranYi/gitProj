# use rand5() function to genereate rand21()

def rand21():
    table = [i for i in range(25)]
    table[21:] = -1
    result = -1
    while result != -1:
        idx = rand5() + 5*rand5()
        result = table[idx]
    return result

