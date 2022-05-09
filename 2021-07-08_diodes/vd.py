#!/usr/bin/env python3
# based on Streetman
from scipy import constants
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="dark")

h = constants.physical_constants["Planck constant"][0]
k = constants.Boltzmann
pi = constants.pi
m0 = constants.m_e
q = constants.physical_constants["elementary charge"][0]
eV = constants.physical_constants["electron volt"][0]
cm3 = 1e-6
m = 1e3


# |----------------- Ec = Conduction band
# |  |
# |  Eg  = Band gap
# |  |
# |  |
# |----------------- Ev = Valence band
#
Eg = 1.12 *eV #Bandgap of Silicon, changes with temperature, but we ignore that



mn = m0
mp = m0


def calc_ni(T):
    #Calculate intrinsic carrier concentration as a function of temperature in Kelvin

# The intrinsic carrier concentration depends on the fermi level and the density of states, which depends
# on the effective mass of electrons and holes. See page 90 - 95 in Streetman
    Nc = 2*np.sqrt(np.power((2*pi*k*T*mn)/(h**2),3))
    Nv = 2*np.sqrt(np.power((2*pi*k*T*mp)/(h**2),3))

    ni = np.sqrt(Nc*Nv)*np.exp(-Eg/(2*k*T))
    return ni*cm3

if __name__ == "__main__":
    TNOM = 300.15

    T = np.arange(TNOM-26.75 - 40,TNOM + 100)

    #- Doubling per 11 C
    n_i_simple = 1.1e10 * 2**((T - TNOM)/11)

    #- BSIM 4.8 model
    n_i_bsim = 1.45e10*(TNOM/300.15) * np.sqrt(T/300.15) \
        * np.exp(21.5565981 - (Eg)/(2*k*T))

    #- Use full calculation
    n_i_adv = calc_ni(T)

    #- Doping consentrations@
    NA = 1e19
    ND = 1e19

    #- Area of diode cm^2
    A = 1e-8

    #- Diffusion constant of electrons
    Dn = 36 # cm^2/s
    Dp = 12 # cm^2/s

    #- Mean lifetime of electrons. Strongly depends on doping density.
    #http://www.ioffe.ru/SVA/NSM/Semicond/Si/electric.html
    tau_n = 8e-8
    tau_p = 8e-8

    I_s = q*A*n_i_adv**2*(1/NA*np.sqrt(Dn/tau_n) + 1/ND*np.sqrt(Dp/tau_p))

    I_c = 1e-6

    V_T = k*T/q

    Vd = V_T*np.log(I_c/I_s)

    C = T - 273.15

    Bc = 2*np.sqrt(np.power((2*pi*k*mn)/(h**2),3))
    Bv = 2*np.sqrt(np.power((2*pi*k*mp)/(h**2),3))
    Nc = 2*np.sqrt(np.power((2*pi*k*T*mn)/(h**2),3))
    Nv = 2*np.sqrt(np.power((2*pi*k*T*mp)/(h**2),3))

    #ell = np.log(I_c) - np.log(A*q) - np.log(((1/NA*np.sqrt(Dn/tau_n) + 1/ND*np.sqrt(Dp/tau_p)))) - np.log(Bv*Bc*cm3)

    ni_2_log = 2*np.log(np.sqrt(Bc*Bv)) + 3*np.log(T) + 2*np.log(cm3) - Eg/(k*T)

    ell = np.log(I_c) - np.log(q*A*(1/NA*np.sqrt(Dn/tau_n) + 1/ND*np.sqrt(Dp/tau_p))) - 2*np.log(np.sqrt(Bc*Bv)) - 2*np.log(cm3)

    vd_paper = V_T*(ell - 3*np.log(T)) + Eg/eV

    print(ell)

    #- Find error from linear
    line = np.polynomial.polynomial.polyfit(T,Vd,1)
    vd_lin_err = Vd - (T*line[1] + line[0])

    #vd_paper = k*T/q*(ell - 3*np.log(T) )  + Eg/q

    plt.figure(1)

    #- Plot ni

    plt.semilogy(C,n_i_adv,label="Advanced")
    plt.semilogy(C,n_i_simple,label="Simple")
    plt.semilogy(C,n_i_bsim,label="BSIM 4.8")
    plt.grid()
    plt.legend()
    plt.ylabel(" $n_i$ [$1/cm^3$]")

    plt.savefig("media/ni.pdf")

    plt.figure(2)

    #- Plot Vd
    plt.subplot(2,1,1)
    plt.plot(C,Vd)
    #plt.plot(C,vd_paper,"r")
    plt.grid(True)
    plt.ylabel("Diode voltage [V]")


    #- Plot Vd linear error
    plt.subplot(2,1,2)
    plt.grid(True)
    plt.plot(C,vd_lin_err*m)

    plt.ylabel("Non-linear component (mV)")
    plt.xlabel("Temperature [C]")

    plt.savefig("media/vd.pdf")

    plt.show()
