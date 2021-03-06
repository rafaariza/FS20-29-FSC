"""
DOCSTRING
"""
import numpy as np
import matplotlib.pyplot as plt

m = 2**9
k = np.arange(-m,m+1,dtype=float)

np.random.seed(32)
values = list(np.random.normal(size=m)+1j*np.random.normal(size=m))
valuesc = [np.conj(i) for i in values][::-1]
center = [np.random.normal()]

v = np.array(center+values+valuesc)

amplitude = k**2

gfield = np.fft.ifftshift(v)
gfield = gfield - np.mean(gfield)
gfield = gfield/np.std(gfield)

gfield2 = np.fft.fftshift(v)
gfield2 = gfield2 - np.mean(gfield2)
gfield2 = gfield2/np.std(gfield2)

plt.plot(k,gfield.real,'k',alpha=.5,label='IFFT')
plt.plot(k,gfield2.real,'r',alpha=.5,label='FFT')
plt.xlabel("$x$")
plt.ylabel("Gaussian array")
plt.legend(fontsize='x-large')
plt.show()
