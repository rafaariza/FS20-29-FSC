import powerbox as pbox
import matplotlib.pyplot as plt

pb = pbox.PowerBox(
    N=512,                     # Number of grid-points in the box
    dim=3,                     # 2D box
    pk = lambda k: 10000*k, # The power-spectrum
    boxlength = 1.0,           # Size of the box (sets the units of k in pk)
    seed = 101010,
    ensure_physical=True                # Set a seed to ensure the box looks the same every time (optional)
)

plt.imshow(pb.delta_x()[0])
plt.colorbar()
plt.show()