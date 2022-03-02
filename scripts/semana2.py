"""
DOCSTRING
"""
import numpy as n
import matplotlib.pyplot as plt

m=2**12
k = n.arange(-m,m+1,1)

n.random.seed(32)
values = list(n.random.normal(size=m)+1j*n.random.normal(size=m))
valuesc = [n.conj(i) for i in values][::-1]
center = [n.random.normal()]

v = n.array(valuesc+center+values)

amplitude = n.sqrt(k**2)

gfield = n.fft.ifft(v * amplitude).real
gfield = gfield - n.mean(gfield)
gfield = gfield/n.std(gfield)

plt.plot(k,gfield,'r')
plt.xlabel("$k$")
plt.ylabel("Gaussian array")
plt.show()
