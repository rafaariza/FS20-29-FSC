import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
plt.rcParams.update({
  "text.usetex": True,
  "font.family": "Palatino"
})

i = 500
k_interval = np.linspace(-i,i,2**14+1)

def gaussian_function(k,sigma):
    """
    FALTA DOCSTRING
    """
    return np.exp(-k**2/(2*sigma**2))/(sigma*np.sqrt(2*np.pi))

integral = integrate.quad(gaussian_function,-np.inf,np.inf,args=(20,))[0]

fvalues = gaussian_function(k_interval,20)
fft = np.fft.fftshift(np.fft.fft(fvalues))
fft_norm = fft/max(fft)

print(f"El área debajo de la gaussiana es {integral:1.0f}")

plt.subplot(1,2,1)
plt.plot(k_interval,fvalues,'r')
plt.title(r"\(f(k)=\frac{1}{\sigma\sqrt{2\pi}}\ \symrm{e}^{-\frac{k^2}{2\sigma^2}}\) con \(\sigma=20\)",fontsize=18)
plt.subplot(1,2,2)
plt.plot(k_interval,np.abs(fft_norm),'g')
plt.title(r"DFT de \(f(k)\) mediante método FFT",fontsize=18)
plt.xlim(-10,10)

plt.show()
