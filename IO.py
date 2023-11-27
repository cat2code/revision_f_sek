import csv

def parse(transactions, verifikat):
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

    #Här skapas all csv reader/writers för framtida användning
    # Try 2 use below if error with unicode characters.
    # bankFReader = csv.reader(open(bankfFile, encoding='utf-8', errors='ignore'), dialect='excel')
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

    #För att tala lite java som är begripligt så har jag gjort en typ av 
    # Map<'VerifikatNr', List<'Rader i verifikatet'>>
    #Detta är eftersom även om de flesta verifikaten bara har två rader finns det vissa 
    #som har betydligt fler rader. Dock kommer detta att bli rörigt att arbeta med


    next(aspiaReader)
    for row in aspiaReader:
        r = [row]
        if r[0][0] in verifikat.keys():
            verifikat[r[0][0]].extend(r)
        else:
            verifikat[r[0][0]] = r


    #För att återigen tala lite java med vad transactions är så är det en 
    #Map<'Bankkonto', List<'Transaktion'>>


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

    
def output(transactions, verifikat):


    outputFile1 = 'output1.csv'
    outputFile2 = 'output2.csv'
    outputFile3 = 'output3.csv'

    outputWriter1 = csv.writer(open(outputFile1, 'w', newline=''), dialect='excel')
    outputWriter2 = csv.writer(open(outputFile2, 'w', newline=''), dialect='excel')
    outputWriter3 = csv.writer(open(outputFile3, 'w', newline=''), dialect='excel')


    outputWriter1.writerows(verifikat.values())

    for a in transactions:
        outputWriter2.writerow([a])
        for r in transactions[a]:

            outputWriter2.writerow(r)



def parseAndRemoveManualCheck(transactions, verifikat):

    bankFAccount = 1941
    bankCafeAccount = 1942
    bankNollningAccount = 1946
    bankProjektAccount = 1944
    bankProjekt2Account = 1945
    bankSexetAccount = 1943


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


if __name__ == '__main__':
    parse()