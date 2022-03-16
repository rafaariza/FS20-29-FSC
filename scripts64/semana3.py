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
    def __init__(self, amplitude, power, size, dimensions, show):
        self._amplitude = amplitude
        self._power = int(power)
        self._size = int(2 ** size + 1)
        self._dimensions = dimensions
        self._show = show

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

        p_espectro = self._amplitude * np.power(normks, -1 * self._power)
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
        for ind, realization in enumerate(self._x_realize[::len(self._x_realize)]):
            fig, ax = plt.subplots()
            plot = ax.imshow(realization, cmap=cmap)
            fig.suptitle(f'Realización campo gaussiano espacio real XY con potencia -{self._power}')
            fig.colorbar(plot)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            if self._show is True:
                plt.show()
            else:
                plt.savefig(
                    f"C:\\Users\\Rafa\\Documents\\FS20-29-FSC\\scripts64\\img\\{ind}{self._power}.png",
                        dpi=300, bbox_inches='tight')

for power in range(-2,3):
    test = FS2029FSC(amplitude=9E-10, size=9, power=power, dimensions=3, show=False)
    test.generator()
    test.show_x_realize()
