"""
DOCSTRING
"""
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

timestr = time.strftime("%Y%m%d-%H%M%S")

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
        np.random.seed(8081998)
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
        self._k_realize = seed_gaussiano_fourier * p_spectro_root
        self._x_realize = np.fft.fftn(self._k_realize).real

    def show_x_realize(self):
        """
        Realización en el espacio de las posiciones
        """
        if not hasattr(self, '_x_realize'):
            print('Genera primero el campo con generator()')

        planck_cmap = ListedColormap(
        np.loadtxt("C:\\Users\\Rafa\\Documents\\FS20-29-FSC\\scripts\\colormap.txt")/255.)
        planck_cmap.set_bad("gray")
        cmap = planck_cmap
        for ind, realization in enumerate(self._x_realize[::len(self._x_realize)]):
            fig, ax = plt.subplots()
            plot = ax.imshow(realization, cmap=cmap)
            fig.suptitle(f'Realización campo gaussiano espacio real XY con potencia {self._power}. {self._name}')
            fig.colorbar(plot)
            ax.set_xlabel(r'$x$ (Mpc)')
            ax.set_ylabel(r'$y$ (Mpc)')
            if self._show is True:
                plt.show()
            else:
                plt.savefig(
                    f"C:\\Users\\Rafa\\Documents\\FS20-29-FSC\\scripts64\\img\\{self._name}-{timestr}-{ind}.png",
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
    name = "TF method"
    return amplitude * np.power(modulus, 1 * power) * np.power(T0, 2), name

def k_pol(amplitude, modulus, power):
    """
    DOCSTRING
    """
    name = "Only polynomial of k"
    return amplitude * np.power(modulus, 1 * power), name


TransFunc = FS2029FSC(
    amplitude=9E-10, size=9, power=1, dimensions=3, show=False, method=transferfunction_k)
TransFunc.generator()
TransFunc.show_x_realize()

k_pol = FS2029FSC(amplitude=9E-10, size=9, power=-4, dimensions=3, show=False, method=k_pol)
k_pol.generator()
k_pol.show_x_realize()
