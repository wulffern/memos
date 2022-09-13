---
abstract: |
  
author: |
 \IEEEauthorblockN{Carsten Wulff}
 carsten@wulff.no
title: Channel model for ranging in a real world indoor communcation channels
documentclass: IEEEtran
papersize: a4
classoption: journal
colorlinks: true
numbersections: true
---

# Goal
Create training data for transfer functions squared of a real indoor communcation
channel in order to provide a training set for a neural net to determine
distance between two 2.4 GHz device.

# Why
Today there are ranging libraries for 2.4 GHz radios, like
[nrf\_dm](https://github.com/nrfconnect/sdk-nrfxlib/tree/main/nrf_dm)
that measure the transfer function squared over an 80 MHz
bandwidth. To compute distance a common method is to first try and resolve the
transfer function (step 1), then compute the inverse fourier transform (step 2) to get the
impulse response, and do a peak search of the impulse response (step 3) for the shortest delay, which is assumed
to be the shortest path between devices.

The distance estimation in these libraries have limited accuracy, as there are
error sources in each of the three steps. Maybe it's possible to train a neural
net to do the estimation?

In order to train a neural net one needs a large sample set of realistic data.
In the physical world it is non-trival to measure such a dataset, as the two
devices must move, and one must at all times have a known distance. The
measurement would be time consuming if one were to include transmission through
walls.

As such, a realistic physical communication channel model, with sufficient
accuracy, is needed. 



# How
Create a physical model that correctly enough models an indoor space with walls,
and thus reflections.

As a first step, a 2D model should be developed, which is possible to expand
into 3D. 

The generation of data should be fast, so generation should be in a compiled language. Maybe it's
good to prototype in high level language.

At the transmitter the signal can be described as

$$
y_{tx,f} = A_{tx}e^{j f t + \phi_{\Delta}}
$$

where $\phi_{\Delta}$ is the initial phase offset of the transmitter, $f$ is the
carrier frequency, $A_{tx}$ is the amplitude of the transmission.

For a single ray, the reciever would see
$$
y_{rx,f,d} = A_{ch,f,d,\vec{A_r}}e^{j \phi_{ch,f,d,\vec{\phi_r}}}y_{tx,f}
$$

where $A_{ch,f,d,\vec{r},\vec{p}}$ is the amplitude response of the channel as a function of
frequency $f$ and distance $d$, and a vector of reflections or re-transmissions
$\vec{A_r}$ and $\vec{\phi_r}$

As such, assuming Friis path loss, the amplitude would be
$$
A_{ch,f,d} = \frac{c}{4\pi f d^2} \prod{\vec{A_r}} 
$$

Assume that reflected and re-transmitted waves undergo a phase change, then phase would be

$$
\phi_{ch,f,d} = 2 \pi \frac{f d}{ c} + \sum{\vec{\phi_r}}
$$

If we expand to multiple rays, for a fixed distance between devices, the reciever signal will be

$$
y_{rx,f} = H(f) y_{tx,f}
$$

And the transfer function 

$$
H(f) =  \sum_{k=0}^{N}{ A_{ch,f,d[k]} e^{j\phi_{ch,f,d[k]}}}
$$

where $d$ is the distance each ray has traveled, $k$ is the index of the ray, and $N$ is the total number of rays.


The shortest path between two devices must correspond to a direct ray, however,
the direct ray can undergo re-transmission through walls. All
other rays must have a distance longer than direct rays, and can be a series of
reflections and re-transmissions.

# Channel model

The code for the channel model can be found at [model.py](https://github.com/wulffern/memos/blob/main/2022-09-12_Range_model/model.py).

Assume a direct ray. Assume that other rays, $\vec{R}$ have uniformly distributed
distance from the direct ray up to 100 meters. Assume that all reflected rays
undergo a $-\pi$ phase shift. Assume that the $\prod{\vec{A_r}}$ is a normal
distribution with a mean of 0.2 and a standard deviation of 0.05.

Assuming a 80 MHz bandwidth in the 2.4 GHz ISM band, the transfer function 
could be as shown in Figures \ref{fig:oneray}, \ref{fig:tworay}, \ref{fig:hray}.

![10 meter direct path, One ray \label{fig:oneray}](response_r1_d10.0.pdf)

![10 meter direct path, Two rays\label{fig:tworay}](response_r2_d10.0.pdf)

![10 meter direct path, 100 rays\label{fig:hray}](response_r100_d10.0.pdf)


# Further work

The $\prod{\vec{A_r}}$ and $\sum{\vec{\phi_r}}$ should be updated more
accurately reflect real world coefficients for example [Reflection and
Transmission Properties of Common Construction Materials at 2.4 GHz Frequency](https://www.sciencedirect.com/science/article/pii/S1876610217321689?ref=pdf_download&fr=RR-2&rr=749b3de02dcafac8)

The distance of rays should somehow be computed from a real scenario, like the
floorplan of a home, and should include a model of the number of reflections or
transmissions

There might already be ray based models, so literature should be checked.


