import csv

bankFAccount = 1941
bankCafeAccount = 1942
bankNollningAccount = 1946
bankProjektAccount = 1944
bankProjekt2Account = 1945
bankSexetAccount = 1943

#Deklarera alla filnamn så att de är samlade på ett och samma ställe
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
# Map<'VerifikatNr', List<'Rader i verifikatet'>>
#Detta är eftersom även om de flesta verifikaten bara har två rader finns det vissa 
#som har betydligt fler rader. Dock kommer detta att bli rörigt att arbeta med

verifikat = {}

next(aspiaReader)
for row in aspiaReader:
    r = [row]
    if r[0][0] in verifikat.keys():
        verifikat[r[0][0]].extend(r)
    else:
        verifikat[r[0][0]] = r


#För att återigen tala lite java med vad transactions är så är det en 
#Map<'Bankkonto', List<'Transaktion'>>

transactions = {}


def appendTransactions(reader, account):
    next(reader)
    next(reader) #Skip the first two lines in each reader because they are not transactions
    t = []
    for row in reader:
        t.append(row)

    transactions[account] = t

appendTransactions(bankFReader, bankFAccount)
appendTransactions(bankCafeReader, bankCafeAccount)
appendTransactions(bankNollningReader, bankNollningAccount)
appendTransactions(bankProjektReader, bankProjektAccount)
appendTransactions(bankProjekt2Reader, bankProjekt2Account)
appendTransactions(bankSexetReader, bankSexetAccount)

bankAccounts = [1941, 1942, 1943, 1944, 1945, 1946]

for nr in list(verifikat.keys()):
    rows = verifikat[nr]

    if len(rows) == 2:
        row1 = rows[0]
        row2 = rows[1]
        account1 = float(row1[3])
        account2 = float(row2[3])
        if(account1 in bankAccounts and account2 in bankAccounts):
            sum1 = 0
            #Här väljer man vilken av kolumnerna som har värdet beroende på
            #om man har banken på debit eller kredit.
            if(row1[10] != ''):
                #Minustecken för att dettta är kredit och det kommer synas som minus på banken
                sum1 = -float(row1[10].replace(',', '.')) 
            else:
                sum1 = float(row1[9].replace(',', '.'))
        
            date1 = row1[1]
            t1 = 0
            for t in transactions[account1]:
                if sum1 == float(t[10]) and t[5] == date1:
                    t1 = t



            sum2 = 0
            if(row2[10] != ''):
                sum2 = -float(row2[10].replace(',', '.')) 
            else:
                sum2 = float(row2[9].replace(',', '.'))

            date2 = row2[1]
            t2 = 0
            for t in transactions[account2]:
                if sum2 == float(t[10]) and t[5] == date2:
                    t2 = t


            if (t1 != 0 and t2 != 0):
                transactions[account1].remove(t1)
                transactions[account2].remove(t2)
                verifikat.pop(nr)                

            






for account in list(transactions.keys()):

    for nr in list(verifikat.keys()):

        rows = verifikat[nr]
        correctAccount = False
        sum = 0
        date = rows[0][1]
        for row in rows:
            if int(row[3]) == account:
                correctAccount = True
                #Här väljer man vilken av kolumnerna som har värdet beroende på
                #om man har banken på debit eller kredit.
                if(row[10] != ''):
                    #Minustecken för att dettta är kredit och det kommer synas som minus på banken
                    sum = sum-float(row[10].replace(',', '.')) 
                else:
                    sum = sum+float(row[9].replace(',', '.'))
        
        if(correctAccount):
            for t in transactions[account]:
                if(t[5] == date and sum == float(t[10])):

                    verifikat.pop(nr)
                    transactions[account].remove(t)
                    break



#Detta är en Map<'Datum', List<'Verifikat'>> vilket är samma sak som
#Map<'Datum', List<List<'Rader i verifikat'>>>
kundbet =  {}

for nr in list(verifikat.keys()):


    rows = verifikat[nr]

    for row in rows:

        if int(row[3]) == 1610:
            if(row[1] in kundbet.keys()):
                kundbet[row[1]].append(rows)
            else:
                kundbet[row[1]] = [rows]


for date in list(kundbet.keys()):
    sum = 0
    for verifika in kundbet[date]:
        for row in verifika:
            if row[10] != '':
                sum += float(row[10].replace(',', '.'))


    for account in list(transactions.keys()):

        for t in transactions[account]:
            if(t[5] == date and sum == float(t[10])):
                outputWriter3.writerow(t)
                outputWriter3.writerow(kundbet[date])
                
                for verifika in kundbet[date]:
                    verifikat.pop(verifika[0][0])
                
                transactions[account].remove(t)
                break


#Detta är för att ta bort internbokföring

bankAccounts = ['1941', '1942', '1943', '1944', '1945', '1946']

for ver in list(verifikat.values()):

    internalBookkeeping = True
    for row in ver:
        if row[3] in bankAccounts:
            internalBookkeeping = False
    
    if internalBookkeeping:
        verifikat.pop(ver[0][0])
            


manuellCheckFile = 'manuellCheck.csv'

manuellCheckReader = csv.reader(open(manuellCheckFile, 'r'), dialect='excel')

checkedVerifikat = next(manuellCheckReader)
checkedBankF = next(manuellCheckReader)
checkedBankCafe = next(manuellCheckReader)    
checkedBankNollning = next(manuellCheckReader)
checkedBankProjekt = next(manuellCheckReader)
checkedBankProjekt2 = next(manuellCheckReader)
checkedBankSexet = next(manuellCheckReader)


for v in checkedVerifikat:
    if v != 'Verifikat':
        verifikat.pop(v)


def checkedBank(checkedBank, firstString, account):
    for t in checkedBank:
        if t != firstString:
            for T in transactions[account]:
                if T[0] == t:
                    transactions[account].remove(T)

checkedBank(checkedBankF, 'BankF_1941', bankFAccount)
checkedBank(checkedBankCafe, 'BankCafe_1942', bankCafeAccount)
checkedBank(checkedBankNollning, 'BankNollning_1946', bankNollningAccount)
checkedBank(checkedBankProjekt, 'BankProjekt_1944', bankProjektAccount)
checkedBank(checkedBankProjekt2, 'BankProjekt2_1945', bankProjekt2Account)
checkedBank(checkedBankSexet, 'BankSexet_1943', bankSexetAccount)


outputWriter1.writerows(verifikat.values())

for a in transactions:
    outputWriter2.writerow([a])
    for r in transactions[a]:

        outputWriter2.writerow(r)


