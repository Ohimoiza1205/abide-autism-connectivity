import numpy as np
import matplotlib.pyplot as plt

# Load one participant's CC200 ROI time series
ts = np.loadtxt("data/Pitt_0050003_rois_cc200.1D")

print("Time-series shape:", ts.shape)

# Functional connectivity = correlation between brain regions
fc = np.corrcoef(ts.T)

print("Connectivity matrix shape:", fc.shape)

# Visualize
plt.imshow(fc, vmin=-1, vmax=1)
plt.colorbar(label="Pearson correlation")
plt.title("Pitt_0050003 — CC200 Functional Connectivity")
plt.xlabel("Brain region")
plt.ylabel("Brain region")
plt.show()