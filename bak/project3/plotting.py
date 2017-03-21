import os
import pandas as pd
import numpy as np
import matplotlib.pylab as pl
import pdb

def draw_and_save(folder, datafilename, imagefilename):
    pth = os.path.join(folder, datafilename)
    df = pd.read_csv(pth, sep=" ", names="t v".split())
    dvals = np.abs(df.v.diff(periods=1))
    fig = pl.figure(figsize=(5, 5))
    ax = fig.add_subplot(111)    
    ax.plot(df.t / 1.0E5, dvals, "k-")
    ax.set_xlabel(r"Simulation iteration ($10^5$)")
    ax.set_ylabel("Q-value difference")
    ax.set_ylim([0, 0.5])
    fig.savefig(imagefilename, bbox_inches="tight")

if __name__ == "__main__":
    # infilenames = ["ceq.txt", "foe.txt", "friend.txt", "qlearning.txt"]
    infilenames = ["ceq.txt", "foe1.txt", "foe2.txt", "foe3.txt"]
    imagefilenames = ["ceq.pdf", "foe.pdf", "friend.pdf", "qlearning.pdf"]

    for dtfile, imgfile in zip(infilenames, imagefilenames):
        draw_and_save(".", dtfile, imgfile)