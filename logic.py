def doEasyMatch(transactions, verifikat):
    
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


def matchKundbet(transactions, verifikat):
    
    #Detta är en Map<'Datum', List<'Verifikat'>> vilket är samma sak som
    #Map<'Datum', List<List<'Rader i verifikat'>>>
    kundbet =  {}

    #Samla alla kundbet verifikat sorterade på datum
    for nr in list(verifikat.keys()):

        rows = verifikat[nr]

        for row in rows:

            if int(row[3]) == 1610:
                if(row[1] in kundbet.keys()):
                    kundbet[row[1]].append(rows)
                else:
                    kundbet[row[1]] = [rows]


    for date in list(kundbet.keys()):
        #Beräkna hur mycket som har kommit in via bankgiro
        sum = 0
        for verifika in kundbet[date]:
            for row in verifika:
                if row[10] != '':
                    sum += float(row[10].replace(',', '.'))


        #Ta bort den bankgiroinsättningen som motsvaras av de verifikaten
        for account in list(transactions.keys()):

            for t in transactions[account]:
                if(t[5] == date and sum == float(t[10])):                    
                    for verifika in kundbet[date]:
                        verifikat.pop(verifika[0][0])
                    
                    transactions[account].remove(t)
                    break



def removeInternalBookkeeping(verifikat):

    #Om ett verifikat inte har något med någon banktransaktion att göra så kommer
    #den inte att kunna matchas mot någon transaktion så då är det meningslöst 
    #att försöka ta hand om den
    bankAccounts = ['1941', '1942', '1943', '1944', '1945', '1946']

    for ver in list(verifikat.values()):

        internalTransaction = True
        for row in ver:
            if row[3] in bankAccounts:
                internalTransaction = False
        
        if(internalTransaction):
            verifikat.pop(ver[0][0])
                

def removeInternalTransactions(transactions, verifikat):

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

                
    



if __name__ == '__main__':
    doEasyMatch()
