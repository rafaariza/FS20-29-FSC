"""
DOCSTRING
"""
import time
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({
        'axes.autolimit_mode': 'data',
        'axes.xmargin': 0,
        'axes.ymargin': 0,
        'xtick.direction': 'in',
        'xtick.top': True,
        'ytick.direction' : 'in',
        'text.usetex': True,
        'ytick.right': True})
from matplotlib.colors import ListedColormap

timestr = "DEF"
k0 = 0.05

class FS2029FSC():
    """
    DOCSTRING
    """
    def __init__(self, amplitude, power, size, dimensions, show, method):
        self._amplitude = amplitude
        self._power = int(power)
        self._size = int(np.power(2, size) + 1)
        self._dimensions = dimensions
        self._show = show
        self._method = method

    def generator(self):
        """
        DOCSTRING
        """
        np.random.seed(643753)
        seed_gaussiano = np.random.normal(size=[self._size] * self._dimensions)
        seed_gaussiano_fourier = np.fft.fftn(seed_gaussiano)

        vectork = np.fft.fftfreq(self._size) * self._size
        kx, ky, kz = np.meshgrid(vectork, vectork, vectork, indexing='xy')
        normks = np.sqrt(np.power(kx,2) + np.power(ky,2) + np.power(kz,2))
        if self._power < 0:
            normks[0,0] = 10E20
        else:
            normks[0,0] = 0
        self._normks = normks

        p_spectro, self._name = self._method(self._amplitude, self._normks, self._power)
        p_spectro_root = np.sqrt(p_spectro)
        self._k_realize = seed_gaussiano_fourier * p_spectro_root * (2 * np.pi) / 10**5
        self._x_realize = np.fft.fftn(self._k_realize).real
        
    def show_x_realize(self):
        """
        Realización en el espacio de las posiciones
        """
        if not hasattr(self, '_x_realize'):
            print('Genera primero el campo con generator()')

        planck_cmap = ListedColormap(
        np.loadtxt("R:\\Documentos\\FS20-29-FSC\\scripts\\colormap.txt")/255.)
        planck_cmap.set_bad("gray")
        cmap = planck_cmap
        for ind, realization in enumerate(self._x_realize[::len(self._x_realize)]):
            fig, ax = plt.subplots()
            fig.set_size_inches(w=6,h=3.7)
            plot = ax.imshow(realization, cmap=cmap)
            #fig.suptitle(f'Realización campo gaussiano espacio real XY con potencia {self._power}. {self._name}')
            cbar = fig.colorbar(plot)
            cbar.set_ticks([])
            cbar.set_label(r'$\delta$')
            ax.set_xlabel(r'$x$ (Mpc)')
            ax.set_ylabel(r'$y$ (Mpc)')
            if self._show is True:
                plt.show()
            else:
                plt.savefig(
                    f"R:\\Documentos\\FS20-29-FSC\\scripts64\\img\\{self._name}-({self._power})-{timestr}-{ind}.pgf",
                        dpi=300, bbox_inches='tight')

def transferfunction_k(amplitude, modulus, power):
    """
    DOCSTRING
    """
    q = modulus/0.14
    L0 = np.log(2 * np.exp(1) + 1.8 * q)
    C0 = 14.2 + 731 * np.power(1 + 62.5 * q, -1)
    T0 = L0 * np.power(L0 + C0 * np.power(q, 2), -1)
    T0[0,0] = 0
    name = "TF_method"
    return amplitude * np.power(q, 1 * power) * np.power(T0, 2), name

def k_pol(amplitude, modulus, power):
    """
    DOCSTRING
    """
    name = "Only_polynomial_of_k"
    return amplitude * np.power(modulus/k0, 1 * power), name


for power in range(-4,2):
    TransFunc = FS2029FSC(
        amplitude=2E-9, size=9, power=power, dimensions=3, show=False, method=transferfunction_k)
    TransFunc.generator()
    TransFunc.show_x_realize()

#for power in range(-4,2):
#    polynomial = FS2029FSC(amplitude=2E-9, size=9, power=power, dimensions=3, show=False, method=k_pol)
#    polynomial.generator()
#    polynomial.show_x_realize()
