from data import DATA

def learn(data, row, my):
    my['n'] += 1
    kl = row.cells[data.cols.target_class.at]
    
    print( row.cells)
    print("my ['n']", my['n'])
    if my['n'] > 10:
        my['tries'] += 1
        my['acc'] += 1 if kl == row.likes(my['datas']) else 0
    
    if not my['datas']:
        my['datas'] = {}
    
    my['datas'][kl] = my['datas'].get(kl, DATA(data.cols.names))
    my['datas'][kl].add(row)