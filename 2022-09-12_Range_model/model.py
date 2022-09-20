#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys
import click
import channel as chan

#Globals
GHz = 1e9
ns = 1e-9


@click.group()
def cli():
    pass


@cli.command()
@click.option("--rays",default=100,help="Number of rays to use")
@click.option("--count",default=100,help="Number channel realizations")
@click.option("--distance",default=10,help="Distance of line of sight in channel")
@click.option("--model",default="model_A1",help="What model to run in channel")
@click.option("--show/--no-show",default=True)
def response(rays,count,distance,model,show):

    df = chan.Distance(distance,count,rays,model)
    df.create()
    df.calc()
    plotChannels(df.f,df.channels,0,"media/response_r%d_d%.1f.pdf" %(rays,distance),show)

@cli.command()
@click.option("--dstart",default=1.0,help="Distance start")
@click.option("--dstop",default=20.0,help="Distance stop")
@click.option("--steps",default=20,help="Number of steps between start and stop")
@click.option("--rays",default=100,help="Number of rays to use")
@click.option("--count",default=100,help="Number channel realizations")
@click.option("--model",default="model_A1",help="What model to run in channel")
@click.option("--show/--no-show",default=True)
def distance(dstart,dstop,steps,count,rays,model,show):

    dists = list()
    ds = np.linspace(dstart,dstop,steps)
    for d in ds:
        dc = chan.Distance(d,count,rays,model)
        dc.create()
        dc.calc()
        dists.append(dc)


    plotDistances(ds,dists,"media/distance_dstart%d_dstop%d_r%d.pdf" %(dstart,dstop,rays),show)
    pass

def plotDistances(ds,dists,name,show=True):

    fig, ax = plt.subplots(5,1,figsize=(10,10), gridspec_kw={'height_ratios': [0.3, 2,2,2,2]})
    cmap_name = "viridis_r"
    cmap = plt.get_cmap(cmap_name)
    colors = cmap.colors

    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))

    N = len(colors)
    maxdist = 50
    idmult = N/maxdist
    c= 299792458
    ns =1e9

    ax[0].imshow(gradient, aspect='auto', cmap=plt.get_cmap(cmap_name),extent=[0,maxdist,1,0])
    ax[0].get_yaxis().set_visible(False)
    ax[0].set_xlabel("Distance [m]")
    dist_avg = 0
    for d in dists:

        dist = d.distance
        dist_avg += dist
        delay = dist/(c)*ns

        for ch in d.channels:
            xx = ch.impulse_x*ns - delay
            y = np.abs(ch.impulse**2)
            y = y/np.max(y)

            ax[1].plot(xx,y,color=colors[int(idmult*dist)],marker="None",linestyle="solid",alpha=0.3)
            ax[2].plot(ch.link_loss,ch.delaySpread*ns,marker="o",color="black")
            ax[3].plot(dist,ch.delaySpread*ns,marker="o",color="black")
            ax[4].semilogx(dist,ch.link_loss,marker="o",color="black")
    dist_avg = dist_avg/len(dists)
    ax[0].set_title("Average distance = %.2f m, %d distances" % (dist_avg,len(dists)))
    ax[1].set_ylabel("Power")
    ax[1].grid(True)
    ax[2].grid(True)
    ax[3].grid(True)
    ax[4].grid(True)
    ax[1].set_xlabel("Impulse response - delay of distance [ns]")
    ax[2].set_ylabel("RMS delay spread [ns]")
    ax[3].set_ylabel("RMS delay spread [ns]")
    ax[4].set_ylabel("Link loss [dB]")
    ax[2].set_xlabel("Link loss [dB]")
    ax[3].set_xlabel("Estimated distance [m]")
    ax[4].set_xlabel("Estimated distance [m]")
    plt.tight_layout()
    plt.savefig(name)
    if(show):
        plt.show()


def plotChannels(f,channels,impulseXOffsetNs,name,show=True):

    fig, ax = plt.subplots(4,1,figsize=(10,10), gridspec_kw={'height_ratios': [2,2,2,2]})

    #Magnitude
    #plt.subplot(4,1,1)
    for ch in channels:
        ax[0].plot(f/GHz,ch.magnitude)
    ax[0].set_ylabel("Magnitude H(f) [dB]")
    ax[0].set_xlabel("Frequency [GHz]")

    #Phase
    #plt.subplot(4,1,2)
    for ch in channels:
        ax[1].plot(f/GHz,ch.phase)
    ax[1].set_ylabel("Phase H(f) [rad]")
    ax[1].set_xlabel("Frequency [GHz]")

    #Impulse
    #plt.subplot(4,1,3)
    for ch in channels:
        ax[2].plot(ch.impulse_x/ns - impulseXOffsetNs ,np.abs(ch.impulse))
    ax[2].set_ylabel("Impulse response ")
    ax[2].set_xlabel("Time [ns]")

    #RMS delay spread
    #plt.subplot(4,1,4)
    for ch in channels:
        ax[3].plot(ch.magnitude.mean(),ch.delaySpread/ns,marker="o",color="black")

    ax[3].set_ylabel("RMS delay spread [ns]")
    ax[3].set_xlabel("Mean RSSI [dB]")

    for a in ax:
        a.grid(True)

    plt.tight_layout()
    plt.savefig(name)
    if(show):
        plt.show()





if( __name__ == '__main__' ):
    cli()
