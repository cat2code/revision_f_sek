from IO import *
from logic import *

transactions = {}
verifikat = {}

parse(transactions, verifikat)
parseAndRemoveManualCheck(transactions, verifikat)
removeInternalTransactions(transactions, verifikat)
doEasyMatch(transactions, verifikat)
matchKundbet(transactions, verifikat)
removeInternalBookkeeping(verifikat)
output(transactions, verifikat)