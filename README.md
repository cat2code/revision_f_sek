# Välkommen till revisionsscriptet

Detta är en guide för hur man ska använda sig av scriptet och vad man ska tänka på

## Filerna

### Aspia

* Logga in i aspia

* Tryck på rapporter upp i högra hörnet

* Under bokföring tryck på Verifikationslista

* Välj "En serie" och "A - Redovisning" i dropdown menyn

* Tryck på export Excel

* Öppna filen i Excel och klicka dig förbi all varningar

* Välj Arkiv - Exportera - Ändra filtyp - CSV - Spara som

* Lägg filen i root mappen för projektet. Default namnet på filen är aspia.csv. Om det inte är det får man ändra filnamnet och path för filen i metoden parse()

### Banken

* Logga in på banken

* Välj ett konto

* Välj "Hittills i år" eller välj hela året manuellt

* Sortera så att de älsta transaktionerna hamnar högst upp, dvs januari ska vara högst upp. *Detta är för att kunna hålla reda på individuella transaktioner. 
Om man inte vänder på det kommer CSV-filen att säga att den nyaste transaktionen har nummer 1 och då kommer man inte kunna ha ett konsistent sätt att hålla reda
på en viss transaktion under året. Man vill att en viss transaktion ska ha samma nummer oavsätt när man laddar ner kontoutdraget*

* Tryck på Ladda ner - Export csv

* Lägg filen i mapppen bankTransaktioner. Default namnen är bankF.csv, bankCafe.csv, bankNollning.csv, bankProjekt.csv, bankProjekt2.csv, bankSexet.csv. Om det inte är så här får man ändra på filnamnen och path i metoden parse()

### ManuellCheck

I den här filen finns alla verifikat och banktransaktion som är manuellt godkända men som scriptet inte klarar av att hantera självt. När man skriver in verifikat och transaktionsnummer är det viktigt att det inte kommer med några mellanslag för då börjar programmet att bråka. Man får inte helller avsluta en rad med ett kommma får då tror programmet att det finns en tom sträng efteråt.


## Scriptet

I skrivande stund finns det två filer som man kan köra för att utföra allt som finns i scriptet. Den första är revision.py som har hela scriptet i en fil vilket gör den ganska lång men lättare att lägga til nya features i eftersom man har tillgång till alla tre outputWriters. Den andra filen är main.py som har sina funktioner fördelade i filerna IO och logic. I den här filen är det mycket lättare att förstå vad som händer på en hög nivå. Ingen av scripten är särskilt optimerade och det finns mycket kodduplicering men det gör också att varje metod / del av scriptet inte använder sig av någon anna del och man behöver inte hoppa runt för att förstå vad som händer. 

### Transactions

Detta är ett objekt där alla transaktioner sparas i en map eller dictionary (beroende på om man är van vid java eller python). Nyckeln är vilket bankkonto det kommer från och visas med hjälp av den siffra som den motsvaras av i bokföringen

### Verifikat

När man har laddar ner verifikaten från aspia kommer de i en lång lista där varje rad är en rad i ett verifikat. Det betyder att de flesta verifikat är fördelade på två rader men det finns de som har fler exempelvis alla Zettle bokföringar.
Verifikat objektet är en map eller dictionary där nyckeln är vilket verifikat (ex A434) och värdet är en lista med alla rader som tillhör just detta verifikat. Notera att varje rad i sin tur är en lista där varje element är en del av verifikatet (ex datum eller kontonummer)

### Parse

I den här metoden parseas alla filer och hamnar i två objekt, ett för alla verifikat och ett för alla transaktioner. Här i finns det en inställning om hur man läser in excel filen med verifikat som har passerat svenska excel på min dator innan den lästes in. Det betyder att den har semikolon som avgränsare istället för vanliga kolon. Om man använder sig av engelska excel är det möjligt att den här raden behöver ändras för att filen är formaterad annorlunda.

### parseAndRemoveManualCheck

Här läser scriptet in manuellCheck-filen och plockar bort allt som inte ska finnas i transkations och verifikat.

### removeInternalTransaction

Här tar jag bort alla transaktioner som sker mellan två av F sektionens konton. Anledningen till att den ligger första är för att det finns två transaktioner kopplade till varje verifikat och om man då kör doEasyMatch först kommer den att bara ta en av transaktionerna för det givna verifikatet

### doEasyMatch

Det här är den viktigaste metoden. Den gör mellan 70%-80% av allt arbete. Vad den gör är att den tar ett bankkonto i taget, sedan väljer den ett verifikat som angår det här bankkontot och försöker matcha det mot en transaktion av samma summa på samma dag. Det finns en chans här att fel verifikat matchas med fel transaktion om det finns flera transaktionern av samma storlek på samma dag

Den kan också ta hänsyn till den nya bokföringen av zettles genom att den går igenom alla rader i verifikatet med kredit och debit för bankkontot och summerar dessa och sedan letar efter slutsumman. Detta gör att det kan bli fel om ett verifikat motsvaras av mer än en banktransaktion. Men det borde den inte ha matchat ändå så no loss

### matchKundbet

Den här metoden hanterar fallet med att bankgiroinbetalningar kommer i klump ofta har flera verifikat kopplade till sig. Det den gör är att den kollar på alla verifikat som går in på bokföringskontot fodringar och summerar alla för en viss dag och försöker matcha det men en transaktion på banken. Den här metoden har begränsningen att om bankgiroinbetalningen inte bokförs som en fodring kommer den här metoden inte att hantera den. Den ser också till att alla verifikat bokför till rätt konto.

### removeInternalBookkeeping

Den här metoden tar bort alla verifikat som inte är kopplade till någon transaktion på banken utan bara hör till budget formaliteter exempelvis när sanning betalar sexet för en fotograf som gick gratis sker det ingen faktisk överföring av pengar med det läggs ändå in som ett verifikat för att hålla koll på budgeten.

### Output

Den här metoden skriver ut alla verifikat i output1 och alla transaktioner i output2 som inte har lyckats matcha. I skrivade stund finns det ingen fil där alla matchade transaktioner och verifikat finns.

## Efter scriptet

När scriptet har körts så har man output1 och output2 och nu måste man ta reda på varför de inte är matchade. Bland verifikat är det vanligaste att det är fel datum på bokföringen. Detta är oftast för att kassören satt och skickade pengar och bokförde på kvällen och då visar sig bokföringsdatument som dagen efter och då fångar inte scriptet det. Det finns också kända begränsningar på hur den hanterar iZettle bokföringen. Sedan är det bara att söka på summor i de olika filerna. Värt att notera är att verifikaten använder sig av kommatecken som skiljetecken för decimal medan transaktionerna använder siga av punkt. 

Ett typiskt förfarande för felsökning av verifikat är:
* Sök på den bokförda summan i filen med de omatchade transaktionerna. Om den finns är det nog fel datum annars kan den vara felvänd (i.e. kredit och debit har bytt plats i bokföringen)
* Sök på den bokförda summan i filen med alla transaktion på kontot där det står att den ska finnas
* Sök på det bokförde datumet och se om du kan hitta om bokföringen är en del av en större transaktion eller om den bokförda summan har ett skrivfel (ex 1168 blev 1186)
* Om man går in på banken och väljer en bankgiroinsättning kan man klicka på en länk för att se alla deltransaktioner

För felsökning av transaktioner är det nästa samma som för verifikat fast omvänt
* Om man gåt in på aspia och klickar på sök belopp kan man söka efter ett givet bokfört belopp bland all verifikat

I sällsynta fall kan man råka ut för Pythons decimalhantering. Ett exempel från verkligheten är 
```py
>>> 51641.24-809.23 == 50831.01
False
```

Om man har bekräftat att allt står rätt till kan man då lägga in relevanta verifikat och transaktioner i manuellCheck.csv