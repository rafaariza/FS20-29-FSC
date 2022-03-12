"""
DOCSTRING
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class FS2029FSC():
    """
    DOCSTRING
    """
    def __init__(self, amplitude, power, size, dimensions):
        self._amplitude = amplitude
        self._power = power
        self._size = int(2 ** size + 1)
        self._dimensions = dimensions

    def generator(self):
        """
        DOCSTRING
        """
        np.random.seed(8081998)
        seed_gaussiano = np.random.normal(size=[self._size] * self._dimensions)
        seed_gaussiano_fourier = np.fft.fftn(seed_gaussiano)

        vectork = np.fft.fftfreq(self._size) * self._size
        kx, ky, kz = np.meshgrid(vectork, vectork, vectork, indexing='xy')
        normks = np.sqrt(kx ** 2 + ky ** 2 + kz ** 2)
        if self._power > 0:
            normks[0,0] = np.inf
        else:
            normks[0,0] = 0
        self._normks = normks

        vectorx = np.arange(-self._size, self._size+1)
        xx, xy = np.meshgrid(vectorx, vectorx, indexing='xy')
        normxs = np.sqrt(xx ** 2 + xy ** 2)
        self._normxs = normxs

        p_espectro = self._amplitude * (normks ** (-1 * self._power))
        p_espectro_root = np.sqrt(p_espectro)
        self._k_realize = seed_gaussiano_fourier * p_espectro_root
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
        for i, realization in enumerate(self._x_realize[::25]):
            fig, ax = plt.subplots()
            ax.imshow(realization, cmap=cmap)
            fig.suptitle(f'Realización campo gaussiano espacio real XY con potencia -{self._power}')
            #fig.colorbar(plot)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            plt.savefig(
                f"C:\\Users\\Rafa\\Documents\\FS20-29-FSC\\scripts64\\img\\{i}.png",
                    dpi=300, bbox_inches='tight')
            plt.close("all")
        #plt.show()

test = FS2029FSC(amplitude=9E-10, size=9, power=4, dimensions=3)
test.generator()
test.show_x_realize()
