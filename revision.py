import csv


bankFAccount = 1941
bankCafeAccount = 1942
bankNollningAccount = 1946
bankProjektAccount = 1944
bankProjekt2Account = 1945
bankSexetAccount = 1943

#Deklarera alla fil namn så att de är samlade på ett och samma ställe
f = './BankTransaktioner/'

bankfFile = f + 'bankF.csv'
bankCafeFile = f + 'bankCafe.csv'
bankNollningFile = f + 'bankNollning.csv'
bankProjektFile = f + 'bankProjekt.csv'
bankProjekt2File = f + 'bankProjekt2.csv'
bankSexetFile = f + 'bankSexet.csv'


aspiaFile = 'aspia.csv'
outputFile1 = 'output1.csv'
outputFile2 = 'output2.csv'
outputFile3 = 'output3.csv'



#Här skapas all csv reader/writers för framtida användning
bankFReader = csv.reader(open(bankfFile, 'r'), dialect='excel')
bankCafeReader = csv.reader(open(bankCafeFile, 'r'), dialect='excel')
bankNollningReader = csv.reader(open(bankNollningFile, 'r'), dialect='excel')
bankProjektReader = csv.reader(open(bankProjektFile, 'r'), dialect='excel')
bankProjekt2Reader = csv.reader(open(bankProjekt2File, 'r'), dialect='excel')
bankSexetReader = csv.reader(open(bankSexetFile, 'r'), dialect='excel')

#Eftersom aspiafilen är exporterad som en excelfil och sedan sparad som en 
#csvfil så använder datorn mina svenska inställningar och använder ; som kolumn 
#byten så att den kan använda , som decimaltecken istället för .
#Ha detta i åtanke när i kör själva
aspiaReader = csv.reader(open(aspiaFile, 'r'), delimiter=';')


outputWriter1 = csv.writer(open(outputFile1, 'w', newline=''), dialect='excel')
outputWriter2 = csv.writer(open(outputFile2, 'w', newline=''), dialect='excel')
outputWriter3 = csv.writer(open(outputFile3, 'w', newline=''), dialect='excel')



#För att tala lite java som är begripligt så har jag gjort en typ av 
# Map<'VerifikatNr', List<'Hela verifikat'>>
#Detta är eftersom även om de flesta verifikaten bara har två rader finns det vissa 
#som har betydligt fler rader. Dock kommer detta att bli rörigt att arbeta med

next(aspiaReader)
verifikat = {}
for row in aspiaReader:
    r = [row]
    if r[0][0] in verifikat.keys():
        verifikat[r[0][0]].extend(r)
    else:
        verifikat[r[0][0]] = r


#Reader är den bank filen vi vill kolla  och konto är det kontonummer som motsvarar 
#den banken som vi vill kolla exempelvis bankFReader med konton nummer 1941
def matchTransaction(reader, account):

    transactions = []
    next(reader)
    next(reader) #Skip the first two lines in each reader because they are not transactions
    for row in reader:
        transactions.append(row)


    keys = list(verifikat.keys())
    for nr in keys:
        candidates = []
        rows = verifikat[nr]
        correctAccount = False
        sum = 0
        date = rows[0][1]
        for row in rows:
            if int(row[3]) == account:
                correctAccount = True
                if(row[10] != ''):
                    sum = -float(row[10].replace(',', '.')) #Minustecken för att dettta är kredit och det kommer synas som minus på banken
                else:
                    sum = float(row[9].replace(',', '.'))
        
        if(correctAccount):
            for t in transactions:
                if(t[5] == date and sum == float(t[10])):
                    a = []
                    a.extend(verifikat[nr])
                    a.extend(t)
                    outputWriter3.writerow(a)

                    verifikat.pop(nr)
                    transactions.remove(t)
                    break

    outputWriter2.writerows(transactions)
                    

        

matchTransaction(bankFReader, bankFAccount)
matchTransaction(bankCafeReader, bankCafeAccount)
matchTransaction(bankNollningReader, bankNollningAccount)
matchTransaction(bankProjektReader, bankProjektAccount)
matchTransaction(bankProjekt2Reader, bankProjekt2Account)
matchTransaction(bankSexetReader, bankSexetAccount)


outputWriter1.writerows(verifikat.values())


