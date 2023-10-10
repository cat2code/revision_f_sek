import csv


with open('aspia.csv', newline='') as aspia, open('swedbank.csv', newline='') as swedbank:

    aspiaReader = csv.reader(aspia, dialect='excel')
    swedbankReader = csv.reader(swedbank, dialect='excel')

    print(next(aspiaReader)[0].split(';'))

    print(next(swedbankReader)[0].split(';'))

    verifikat = []
    transaktioner = []


    for v in aspiaReader:
        verifikat.append(v[0].split(';'))
    
    a = 0
    temp = []
    print(len(verifikat))
    for i in range(len(verifikat)):
        if(a % 2 == 1):
            temp.append(verifikat[i])
        a = a+1
    print(len(temp))

    for t in swedbankReader:
        transaktioner.append(t[0].split(';'))

    ver = temp.copy()
    

    for v in temp:
        for t in transaktioner:
            try:
                if(v[1] == t[1] and -int(v[10])==int(t[6].replace(' ', ''))):
                    #print(v)
                    #print(t)
                    temp.remove(v)
            except IndexError:
                None
            except ValueError:
                None

    for v in temp:
        if(v[0] == 'A848'):
            print(v)

