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
        self._size = int(2 ** size)
        self._dimensions = dimensions

    def generator(self):
        """
        DOCSTRING
        """
        np.random.seed(32)
        seed_gaussiano = np.random.normal(size=[self._size] * self._dimensions)
        seed_gaussiano_fourier = np.fft.fftn(seed_gaussiano)

        vectork = np.fft.fftfreq(self._size) * self._size
        kx, ky = np.meshgrid(vectork, vectork, indexing='xy')
        normks = np.sqrt(kx ** 2 + ky ** 2)
        normks[0,0] = np.inf
        self._normks = normks

        vectorx = np.arange(-self._size, self._size+1)
        xx, xy = np.meshgrid(vectorx, vectorx, indexing='xy')
        normxs = np.sqrt(xx ** 2 + xy ** 2)
        self._normxs = normxs

        p_espectro = self._amplitude * (normks ** (-1 * self._power))
        p_espectro_root = np.sqrt(p_espectro)
        self._k_realize = seed_gaussiano_fourier * p_espectro_root
        self._x_realize = np.fft.ifftn(self._k_realize).real

    def show_x_realize(self):
        """
        Realización en el espacio de las posiciones
        """
        if not hasattr(self, '_x_realize'):
            print('Genera primero el campo con generator()')

        fig, ax = plt.subplots()
        colombi1_cmap = ListedColormap(\
        np.loadtxt("C:\\Users\\Rafa\\Documents\\FS20-29-FSC\\scripts\\colormap.txt")/255.)
        colombi1_cmap.set_bad("gray")
        cmap = colombi1_cmap
#        for kz in range(20):
        ax.imshow(self._x_realize, cmap=cmap)
#            fig.suptitle(f'Realización campo gaussiano espacio real XY con potencia -{self._power}')
#            ax.set_xlabel('x')
#            ax.set_ylabel('y')
#            plt.savefig(\
#                f"C:\\Users\\Rafa\\Documents\\FS20-29-FSC\\scripts64\\img\\{kz}.png",\
#                    dpi=300, bbox_inches='tight')
        plt.show()

test = FS2029FSC(amplitude=np.random.uniform(0, 10), size=10, power=2, dimensions=2)
test.generator()
test.show_x_realize()
