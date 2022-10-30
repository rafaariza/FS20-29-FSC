"""
Módulo Python del TFG Generación de campos gaussianos en teorías inflacionarias.
"""
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({
        'axes.autolimit_mode': 'data',
        'axes.xmargin': 0,
        'axes.ymargin': 0,
        'xtick.direction': 'in',
        'xtick.top': True,
        'ytick.direction' : 'in',
        'ytick.right': True,
        'text.usetex': True})
from matplotlib.colors import ListedColormap, CenteredNorm
from powerbox.tools import _magnitude_grid as _mgrid
from powerbox.powerbox import _make_hermitian as _hermitian
from powerbox.dft import fftfreq as _fftfreq, ifft as _ifftn

timestr = "DEF"
k0 = 0.05

class FS2029FSC():
    """
    Calcula campos gaussianos en espacio real y de fourier generados con un espectro de potencia dado.
    """
    def __init__(self, amplitude, power, size, dimensions, show, method,
                boxlength=1.0, normalise=True, a=1., b=1.):

        self._amplitude = amplitude
        self._boxlength = boxlength
        self._normalise = normalise
        self._coef_a = a
        self._coef_b = b
        self._power = int(power)
        self._size = int(np.power(2, size))
        self._dimensions = dimensions
        self._show = show
        self._method = method
        self._volume = self._boxlength ** self._dimensions
        self._dx = float(boxlength) / self._size
        self._n = self._size + 1

    def generator(self):
        """
        Genera el campo de fluctuaciones de densidad de energía δ(x).
        """
        rng = np.random.default_rng(seed=42)
        seed_gaussiano_mag = rng.normal(0.0,1.0, size=[self._n] * self._dimensions)
        seed_gaussiano_phase = 2 * np.pi * rng.uniform(size=[self._n] * self._dimensions)
        seed_gaussiano_hermitian = _hermitian(seed_gaussiano_mag, seed_gaussiano_phase)
        cutindex = (slice(None, -1),) * self._dimensions
        seed_gaussiano_hermitian = seed_gaussiano_hermitian[cutindex]

        self._vectork = _fftfreq(self._size, d=self._dx, b=self._coef_b)
        normks = _mgrid(self._vectork, self._dimensions)
        mask = normks != 0
        self._normks = normks
        self._normks[mask], self._name = self._method(self._amplitude, self._normks[mask], self._power)

        if self._normalise:
            p_spectro = self._normks / self._volume
        else:
            p_spectro = self._normks

        p_spectro_root = np.sqrt(p_spectro)
        self._k_realize = seed_gaussiano_hermitian * p_spectro_root
        self._x_realize = np.empty((self._size,) * self._dimensions,
        dtype='complex128')
        self._x_realize[...] = self._k_realize
        self._x_realize[...] = self._volume * _ifftn(self._x_realize, 
        L=self._boxlength, a=self._coef_a, b=self._coef_b)[0]
        self._x_realize = np.real(self._x_realize)
        np.clip(self._x_realize, -1, np.inf, self._x_realize)

        return self._x_realize

    def show_x_realize(self):
        """
        Realización en el espacio de las posiciones.
        """
        if not hasattr(self, '_x_realize'):
            print('Genera primero el campo con generator()')

        planck_cmap = ListedColormap(
        np.loadtxt("R:\\Documentos\\FS20-29-FSC\\scripts\\colormap.txt")/255.)
        planck_cmap.set_bad("gray")
        planck_cmap.set_under("white")
        cmap = planck_cmap
        for ind, realization in enumerate(self._x_realize[::8]):
            fig, ax = plt.subplots(figsize=(6,6))
            ax.yaxis.get_major_locator().set_params(integer=True)
            fig.subplots_adjust(top = 0.95, bottom = 0.12, right = 1, left = 0)
            ax.set_box_aspect(1)
            plot = ax.imshow(realization, norm=CenteredNorm(), cmap=cmap,
                extent=(0,self._boxlength*self._size,0,self._boxlength*self._size), rasterized=True)
            cbar = fig.colorbar(plot, orientation='horizontal', fraction=0.042,
                                pad=0.15)
            cbar.set_label(r'$\delta(\mathbf{x})$', rotation=0, size=12)
            ax.set_xlabel(r'$x$ (Mpc)')
            ax.set_ylabel(r'$y$ (Mpc)')
            if self._show is True:
                plt.show()
            else:
                plt.savefig(
                    f"R:\\Documentos\\FS20-29-FSC\\scripts64\\img\\gif\\transfercmbgif-{ind}.pgf",
                        dpi=900, bbox_inches='tight', pad_inches=0.0)
            plt.close(fig)

def transferfunction_k(amplitude, modulus, power):
    """
    espectro de potencias en época de recombinación.
    """
    q = modulus/(0.14*k0)
    L0 = np.log(2 * np.exp(1) + 1.8 * q)
    C0 = 14.2 + 731 * np.power(1 + 62.5 * q, -1)
    T0 = L0 * np.power(L0 + C0 * np.power(q, 2), -1)
    name = "transfer"
    return amplitude * np.power(q, 1 * power) * np.power(T0, 2), name

def k_pol(amplitude, modulus, power):
    """
    Espectro de potencias primordial.
    """
    name = "pdek"
    return amplitude * (modulus/k0) ** power, name

delta_x = FS2029FSC(amplitude=2.101E-9, power=0.965, size=9, dimensions=3, show=False, method=transferfunction_k, boxlength=0.25)
delta_x.generator()
delta_x.show_x_realize()