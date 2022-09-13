#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys


c = 3.0e8

def calcImpulse2(H2):
    N = 2048
    yfft = np.fft.ifft(H2,N)
    yf = yfft[1:((int)(len(yfft)/2))]

    #- Normalize impulse
    I2 = yf/yf.max()
    I2_x = np.arange(0,N/2-1)/N/2/1e6
    return (I2_x,I2)

def modelH2(f,rays,distance):
    N = len(f)
    M = rays
    A_k = np.concatenate((np.array([1]),0.2+ 0.05*np.random.randn(M-1)))
    d_k = np.concatenate((np.array([distance]),np.random.uniform(low=distance,high=100,size=(M-1))))
    r_k = np.concatenate((np.array([0.0]),np.ones(M-1)))

    H = np.zeros(N) + 1j*np.zeros(N)
    for i in range(0,N):
        f_i = f[i]
        amp = c/(4*np.pi*f_i)*np.divide(A_k,np.multiply(d_k,2))
        phase = -2*np.pi*f_i*d_k/c -r_k*np.pi #+ (1-np.random.randn(M))*np.pi/10
        cplx = np.multiply(amp,np.exp(1j*phase))
        H[i] = np.sum(cplx)

    return np.multiply(H,H)

if( __name__ == '__main__' ):

    if (len(sys.argv) < 3):
        print(f"Usage: python3 {sys.argv[0]} <rays> <direct distance>")
        exit()

    #- Number of runs
    K = 100
    rays = int(sys.argv[1])
    GHz = 1e9
    ns = 1e-9
    distance = float(sys.argv[2])

    phase = list()
    magnitude = list()
    H2s = list()
    error = np.zeros(K)
    f = 2.4e9 + np.arange(1,81)*1.0e6
    for i in range(0,K):
        H2= modelH2(f,rays,distance)
        H2s.append(H2)
        magnitude.append(10*np.log10(np.abs(H2)))
        phase.append(np.unwrap(np.angle(H2)))
        e_distance = (phase[-1][-1]-phase[-1][0])/(2*np.pi*79e6/c*2)
        error[i] = distance - e_distance

    plt.subplot(3,1,1)
    for m in magnitude:
        plt.plot(f/GHz,m)
    plt.ylabel("Magnitude H(f) [dB]")
    plt.xlabel("Frequency [GHz]")
    plt.subplot(3,1,2)
    for p in phase:
        plt.plot(f/GHz,p)
    plt.ylabel("Phase H(f) [rad]")
    plt.xlabel("Frequency [GHz]")
    plt.subplot(3,1,3)
    for H2 in H2s:
        (I2_x,I2) = calcImpulse2(H2)
        plt.plot(I2_x/ns,np.abs(I2))

    plt.ylabel("Impulse response ")
    plt.xlabel("Time [ns]")
    plt.tight_layout()
    plt.savefig("media/response_r%d_d%.1f.pdf" %(rays,distance))
    if(len(sys.argv) > 3):
        plt.show()
