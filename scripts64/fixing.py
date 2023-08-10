import powerbox as pbox

pb = pbox.PowerBox(
    N=8,                     # Number of grid-points in the box
    dim=2,                     # 2D box
    pk = lambda k: 0.1*k**-2., # The power-spectrum
    boxlength = 1.0,           # Size of the box (sets the units of k in pk)
    seed = 1010                # Set a seed to ensure the box looks the same every time (optional)
)

k = pb.k()
mask = k != 0
losk = k[mask]

print(pb.pk(losk).shape, pb.power_array().shape)