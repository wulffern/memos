#!/usr/bin/env python3
#

import numpy as np

class Distance:
    def __init__(self,distance,count=100,rays=100,model="model_A1"):
        self.distance = distance
        self.count = count
        self.rays = rays
        self.channels = list()
        self.model = model

        ch = Channel()
        if not hasattr(ch,self.model):
            raise(f"Could not find {self.model} in channel.Channel\n")


        self.f = 2.4e9 + np.arange(1,81)*1.0e6

    def create(self):
        for i in range(0,self.count):
            ch = Channel()
            fmodel = getattr(ch, self.model)
            fmodel(self.f,self.rays,self.distance)
            self.channels.append(ch)


    def calc(self):
        for c in self.channels:
            c.calc()




class Channel:

    def __init__(self):
        self.c = 299792458
        self.reflection_mean = 0.15
        self.reflection_std = 0.05
        pass



    def model_A1(self,f,rays,distance):
        N = len(f)
        M = rays
        self.distance = distance
        self.rays = rays
        c = self.c
        A_k = np.concatenate((np.array([1]),self.reflection_mean + self.reflection_std*np.random.randn(M-1)))
        d_k = np.concatenate((np.array([distance]),np.random.uniform(low=distance,high=100,size=(M-1))))
        r_k = np.concatenate((np.array([0.0]),np.ones(M-1)))

        H = np.zeros(N) + 1j*np.zeros(N)
        for i in range(0,N):
            f_i = f[i]
            amp = c/(4*np.pi*f_i)*np.divide(A_k,np.multiply(d_k,2))
            phase = -2*np.pi*f_i*d_k/c -r_k*np.pi #+ (1-np.random.randn(M))*np.pi/10
            cplx = np.multiply(amp,np.exp(1j*phase))
            H[i] = np.sum(cplx)
        self.transfer2 =  np.multiply(H,H)


    def calcCommon(self):

        self.phase = np.unwrap(np.angle(self.transfer2))
        self.magnitude = 10*np.log10(np.abs(self.transfer2))
        self.link_loss = -self.magnitude.mean()

    def calcTransfer(self):
        fstart = 4
        fstop = 78

        tr = np.zeros(len(self.transfer2),dtype=complex)

        #- Do a linear regression to find an optimum slope
        x = np.arange(fstart,fstop,1)
        ang = np.unwrap(np.angle(self.transfer2))
        A = np.vstack([x, np.ones(len(x))]).T
        xang = np.linalg.lstsq(A,ang[fstart:fstop],rcond=None)[0]
        xall = np.arange(0,80,1)
        th_ideal = xang[0]/2*xall + xang[1]/2
        smag = np.sqrt(np.abs(self.transfer2))
        sang = ang/2

        for i in range(fstart,fstop):
            at = th_ideal[i]
            diff = sang[i] - th_ideal[i]
            if(diff > np.pi):
                sang[i]  = sang[i] - np.pi
            elif(diff < -np.pi):
                sang[i] = sang[i] + np.pi

        self.transfer = np.multiply(smag, np.exp( 1j * sang ) )


    def calcImpulse2(self):
        N = 2048
        yfft = np.fft.ifft(self.transfer2,N)
        yf = yfft[0:((int)(len(yfft)/2))]
        self.impulse2 = yf
        self.impulse2_x = np.arange(0,N/2)/N/2/1e6

    def calcImpulse(self):
        N = 2048
        yfft = np.fft.ifft(self.transfer,N)
        yf = yfft[0:((int)(len(yfft)/2))]
        self.impulse = yf
        self.impulse_x = np.arange(0,N/2)/N/1e6

        am = np.argmax(np.abs(self.impulse))



    # Based on Statistical Properties of the RMS Delay-Spread of Mobile Radio Channels with Independent Rayleigh-Fading Paths
    # IEEE TRANSACTIONS ON VEHICULAR TECHNOLOGY, VOL. 45, NO. 1, FEBRUARY 1996
    def calcDelaySpread2(self):
        s = np.abs(self.impulse2)**2

        pwr = np.sum(s)
        p1 = np.sum(np.multiply(s,self.impulse2_x))
        p2 = np.sum(np.multiply(s,self.impulse2_x**2))
        rms = np.sqrt(p2/pwr - (p1/pwr)**2)
        self.delaySpread2 = rms

    def calcDelaySpread(self):

        y = self.impulse

        s = np.abs(y**2)

        s = s/np.max(s)

        #- Remove the lowest values. They are likely artifacts of IFFT.
        s[s < 0.01] = 0

        pwr = np.sum(s)
        p1 = np.sum(np.multiply(s,self.impulse_x))
        p2 = np.sum(np.multiply(s,self.impulse_x**2))
        rms = np.sqrt(p2/pwr - (p1/pwr)**2)

        self.delaySpread = rms


    def calc(self):

        self.calcCommon()
        self.calcTransfer()
        self.calcImpulse()
        self.calcImpulse2()
        self.calcDelaySpread()
