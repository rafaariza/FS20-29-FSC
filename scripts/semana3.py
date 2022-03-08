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
    def __init__(self, amplitude=1., power=2, size=5, dimensions=2):
        self.amplitude = amplitude
        self.power = power
        self._size = int(2 ** size)
        self.dimensions = dimensions

    def generator(self):
        """
        DOCSTRING
        """
        seed_gaussiano = np.random.normal(size=[self._size] * self.dimensions)
        seed_gaussiano_fourier = np.fft.fft2(seed_gaussiano)

        vectork = np.fft.fftfreq(self._size) * self._size
        kx, ky = np.meshgrid(vectork, vectork, indexing='xy')
        normks = np.sqrt(kx ** 2 + ky ** 2)
        normks[0,0] = np.inf
        self._normks = normks

        vectorx = np.arange(-self._size+1, self._size)
        xx, xy = np.meshgrid(vectorx, vectorx, indexing='xy')
        normxs = np.sqrt(xx ** 2 + xy ** 2)
        self._normxs = normxs

        p_espectro = self.amplitude * (normks ** (-1 * self.power))
        p_espectro_root = np.sqrt(p_espectro)
        self._k_realize = seed_gaussiano_fourier * p_espectro_root
        self._x_realize = np.fft.ifft2(self._k_realize).real

    def show_x_realization(self):
        """
        Realización en el espacio de las posiciones
        """
        if not hasattr(self, '_x_realize'):
            return print('Genera primero el campo con generator()')

        colombi1_cmap = ListedColormap(np.loadtxt("C:\\Users\\Rafa\\Documents\\FS20-29-FSC\\scripts\\colormap.txt")/255.)
        colombi1_cmap.set_bad("gray")
        cmap = colombi1_cmap
        fig, ax = plt.subplots()
        ax.imshow(self._x_realize, cmap=cmap)
        fig.suptitle('Realización campo gaussiano espacio real XY')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        plt.show()

test = FS2029FSC(amplitude=np.random.uniform(0, 10), size=9, power=2)
test.generator()
test.show_x_realization()
