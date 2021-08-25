from  justbackoff import Backoff

b = Backoff(min_ms=300000, max_ms=3600000, factor=2, jitter=False)
print(b.duration())
print(b.duration())
print(b.duration())

#a = 4
#while a>=0:
#    if a%2 == 0:
#        print(b.duration())
#    a-=1