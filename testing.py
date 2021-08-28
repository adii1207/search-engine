#from  justbackoff import Backoff

#b = Backoff(min_ms=300000, max_ms=3600000, factor=2, jitter=False)
#print(b.duration())
#print(b.duration())
#print(b.duration())

#a = 4
#while a>=0:
#    if a%2 == 0:
#        print(b.duration())
#    a-=1

import datetime
exec_date = datetime.datetime.now()
print(exec_date, end=' ')
timeDelta = datetime.timedelta(0, 10)
newTime = exec_date + timeDelta
print(newTime)
print(type(exec_date))
print(type(newTime))
print(type(datetime.datetime(2009, 11, 6, 16, 30, 5)))