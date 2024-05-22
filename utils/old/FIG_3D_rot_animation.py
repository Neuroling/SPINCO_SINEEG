import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D


# Define sampling rate, number of cycles, fundamental frequency, and length for the wavelet
fs = 500
n_cycles = 5
freq = 5
scaling = 1.0
omega = n_cycles
wavelet_len = int(n_cycles * fs / freq)

# Create wavelet
wavelet = signal.morlet(wavelet_len, omega, scaling)

# Plot the real part of the wavelet
#_, ax = plt.subplots()
#ax.plot(np.real(wavelet))
#ax.set_axis_off()


# %%  Plot real and imaginary components in a 3D plot
plt.close('all')
fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')
#ax.plot(np.linspace(0, scaling, wavelet.size), wavelet.real, wavelet.imag)
ax.plot(np.linspace(0, scaling, wavelet.size), wavelet.real, wavelet.imag)
ax.set(xlabel='Scaling', ylabel='Real Amplitude', zlabel='Imag Amplitude')

def init():
    return fig

# rotate the axes and update
for angle in range(0, 360):
    ax.view_init(30, angle)
    plt.draw()
    plt.pause(.001)


def animate(i):
    ax.view_init(elev=10., azim=i)
    return fig,

# Animate
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=360, interval=20, blit=True)
# % Save

anim.save('FIG_3Drot.gif', writer='imagemagick', fps=60) 