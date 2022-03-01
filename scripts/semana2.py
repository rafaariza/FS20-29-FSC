"""
DOCSTRING
"""
import numpy as n
import matplotlib.pyplot as plt

m=256

k = n.arange(-m,m+1,1)

values = list(n.random.normal(size=m)+1j*n.random.normal(size=m))
valuesc = [n.conj(i) for i in values]
center = [n.random.normal()]

v = n.array(valuesc+center+values)
v[0]=v[-1]

amplitude = n.sqrt(k**2)

gfield = n.fft.ifft(v * amplitude).real
gfield = gfield - n.mean(gfield)
gfield = gfield/n.std(gfield)

plt.plot(k,gfield)
plt.show()
