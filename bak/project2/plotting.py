import matplotlib.pylab as pl
import numpy as np
import pandas as pd
import matplotlib.patches as patches
from mpl_toolkits.axes_grid.inset_locator import inset_axes
from sklearn.neural_network import MLPRegressor


def make_fig1():
    names = ["iterations", "rewards"]
    df20k = pd.read_csv("tmp/lunar_lander_01/lunar_lander_20k.txt", names=names)    

    fig1 = pl.figure(figsize=(5, 5))
    ax = pl.subplot(111)
    ax.plot(df20k["iterations"][:5000], df20k["rewards"][:5000], "-", 
            color="gray", lw=0.5)    
    ax.set_xlabel("episode")
    ax.set_ylabel("raw reward")
    ax.text(3500, -474, r"$\epsilon = 1.00$", fontsize=12)    
    ax.text(3500, -550, r"$\epsilon_\mathrm{decay} = 0.99$", fontsize=12)    
    ax.text(3500, -625,r"$\gamma = 0.99$", fontsize=12)
    ax.text(3500, -700,r"$\alpha = 10^{-4}$", fontsize=12)
    pl.savefig("fig1.pdf", bbox_inches="tight")
    pl.close("all")

def make_fig2():
    names = ["iterations", "rewards"]
    df20k = pd.read_csv("tmp/lunar_lander_01/lunar_lander_20k.txt", names=names)
    df2 = pd.read_csv("tmp/lunar_lander_03/lunar_lander_5k.txt", names=names)
    df3 = pd.read_csv("tmp/lunar_lander_04_epsilon_scheduled/lunar_lander_5k.txt", names=names)

    fig1 = pl.figure(figsize=(6, 8))
    ax1 = fig1.add_subplot(211)
    ax1.plot(df20k["iterations"], 
            pd.rolling_mean(df20k["rewards"], 100),
            "-", color="blue", lw=2)
    # ax1.add_patch(patches.Rectangle((1000, 150), 13000, 100, 
    #                                alpha=0.3, color="gray"))
    ax1.set_ylim([-300, 320])
    ax1.set_xlabel("episode")
    ax1.set_ylabel("average reward")
    ax1.text(6000, 260, r"trained", fontsize=12)
    ax1.text(14500, -75, r"overfitting", fontsize=12)
    ax1.text(250, -275, "(a)", fontsize=18)

    ax2 = fig1.add_subplot(212)
    ax2.plot(df20k["iterations"][:5000], 
            pd.rolling_mean(df20k["rewards"][:5000], 100),
            "-", color="gray", lw=2, alpha=1.0)    
    ax2.plot(df2["iterations"], 
            pd.rolling_mean(df2["rewards"], 100),
            "-", color="blue", lw=2, alpha=1.0)                
    ax2.plot(df3["iterations"], 
            pd.rolling_mean(df3["rewards"], 100),
            "-", color="magenta", lw=2, alpha=1.0)               
    ax2.set_xlabel("episode")
    ax2.set_ylabel("average reward")
    ax2.text(50, -275, "(b)", fontsize=18)
    ax2.legend([r"$\epsilon_\mathrm{decay}$ = 0.990", 
                r"$\epsilon_\mathrm{decay}$ = 0.995",
                r"$\epsilon$ = adaptive"], 
                fontsize=10, loc=4)
    fig1.tight_layout()
    pl.savefig("fig2.pdf", bbox_inches="tight") 
    pl.close("all")   

def make_fig3():
    names = ["iterations", "rewards"]
    # df20k = pd.read_csv("tmp/lunar_lander_01/lunar_lander_20k.txt", names=names)
    df1 = pd.read_csv("tmp/lunar_lander_03/lunar_lander_5k.txt", names=names)
    df2 = pd.read_csv("tmp/lunar_lander_02_epochs=10/lunar_lander_5k.txt", names=names)
    avg_rewards_1 = pd.rolling_mean(df1["rewards"], 100)   
    avg_rewards_2 = pd.rolling_mean(df2["rewards"], 100)   

    fig1 = pl.figure(figsize=(12, 12))
    ax1 = fig1.add_subplot(221)
    ax1.plot(df1["iterations"], avg_rewards_1, "-", 
            color="blue", lw=2)    
    ax1.plot(df2["iterations"], avg_rewards_2, "-", 
            color="green", lw=2)    
    ax1.set_xlabel("episode", size=18)
    ax1.set_ylabel("average reward", size=18)
    ax1.text(2500, 220, "training epochs = 2", color="blue")
    ax1.text(2500, 10, "training epochs = 10", color="green")    
    ax1.text(250, -175, "(a)", fontsize=22)    
    ax1.tick_params(labelsize=16)

    np.random.seed(1)
    ssize = 256
    ones = np.ones((ssize, 1))
    x = np.linspace(-1, 1, ssize).reshape((ssize, 1))
    y = -0.5 + 2 * np.sin(2 * np.pi * x) + np.random.random((ssize, 1))
    X = np.hstack((ones, x))

    regressor = MLPRegressor(hidden_layer_sizes=(50, 50),
                             activation="relu",
                             batch_size=128,
                             max_iter=25,
                             solver="adam")

    alpha_list = np.logspace(-6, -0.8, 1000)
    loss = np.zeros(alpha_list.shape)
    
    for idx, alpha_t in enumerate(alpha_list):    
        regressor.learning_rate_init = alpha_t
        regressor.fit(X, y)
        loss[idx] = regressor.loss_
        print "learning rate = %0.6f, loss_ = %0.3f" % (alpha_t, loss[idx])   

        if np.abs(alpha_t - 1e-2) <= 1e-3:
            yp = regressor.predict(X)

    ax2 = fig1.add_subplot(222)
    ax2.semilogx(alpha_list, loss)
    ax2.set_xlabel("learning rate", size=18)
    ax2.set_ylabel("fitting loss", size=18)
    ax2.tick_params(labelsize=16)
    ax2.text(2e-6, 0.1, "(b)", fontsize=22)

    iax2 = inset_axes(ax2, width="30%", height=1., loc=1)
    iax2.plot(x, y, "o", color="gray", mec="none", ms=2)
    iax2.plot(x, yp, "-", color="red", lw=2)
    iax2.set_xlabel("x", size=11)
    iax2.set_ylabel("y", size=11)
    iax2.tick_params(labelsize=9)

    ax3 = fig1.add_subplot(223)
    df2 = pd.read_csv("tmp/lunar_lander_04_epsilon_scheduled/lunar_lander_5k.txt", names=names)    
    ax3.plot(df1["iterations"], avg_rewards_1, "-", 
             color="blue", alpha=1, lw=2)
    ax3.plot(df2["iterations"], pd.rolling_mean(df2["rewards"], 100),
         color="green", alpha=1, lw=2)
    ax3.set_xlabel("episode", size=18)
    ax3.set_ylabel("average reward", size=18)
    ax3.tick_params(labelsize=16)
    ax3.text(250, -250, "(c)", fontsize=22)
    ax3.legend([r"Decaying $\epsilon$", r"Adaptive $\epsilon$"], loc=2)
    iax3 = inset_axes(ax3, width="50%", height=1., loc=4, borderpad=2.5)
    iax3.plot([0, 50, 50, 100, 100, 150, 150, 200, 200, 500],
              [0.1, 0.1, 0.05, 0.05, 0.02, 0.02, 0.01, 0.01, 0.005, 0.005], 
              "-", color="gray", lw=2)    
    iax3.set_xlim([0, 250])
    iax3.set_xlabel("average reward", size=11)

    iax3.set_ylabel(r"$\epsilon$ schedule", size=11)
    iax3.tick_params(labelsize=9)

    ax4 = fig1.add_subplot(224)
    df1 = pd.read_csv("tmp/lunar_lander_04_epsilon_scheduled/lunar_lander_5k.txt", names=names)
    df2 = pd.read_csv("tmp/lunar_lander_05_gamma=0.75/lunar_lander_5k.txt", names=names)    
    df3 = pd.read_csv("tmp/lunar_lander_06_gamma=1.00/lunar_lander_5k.txt", names=names)
    df4 = pd.read_csv("tmp/lunar_lander_07_gamma=0.995/lunar_lander_5k.txt", names=names)

    ax4.plot(df1["iterations"][:2500], pd.rolling_mean(df1["rewards"][:2500], 100),
             color="black", alpha=0.9, lw=2)
    ax4.plot(df4["iterations"], pd.rolling_mean(df4["rewards"], 100),
         color="gray", alpha=0.9, lw=2)    
    ax4.plot(df2["iterations"], pd.rolling_mean(df2["rewards"], 100),
             color="green", alpha=0.9, lw=2)
    ax4.plot(df3["iterations"], pd.rolling_mean(df3["rewards"], 100),
             color="magenta", alpha=0.9, lw=2)

    ax4.set_xlabel("episode", size=18)
    ax4.tick_params(labelsize=16)
    ax4.legend([r"$\gamma=0.990$", 
                r"$\gamma=0.995$", 
                r"$\gamma=0.750$",
                r"$\gamma=1.000$"], loc=4)
    ax4.text(125, -900, "(d)", fontsize=22)

    fig1.savefig("fig0.pdf", bbox_inches="tight")
    pl.close("all")

if __name__ == '__main__':
    make_fig1()
    make_fig2()
    make_fig3()

