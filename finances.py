import datetime

from import_chase import *
from learning import *


i = ImportChase('chase.csv',datetime.datetime(2016, 8, 1))
i.run()

l = LearnRules()
l.run()