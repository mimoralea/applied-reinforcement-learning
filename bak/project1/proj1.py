import numpy as np
import pdb
import matplotlib.pylab as pl

# Define constants
DIM = 5

# True weights
WTS_TRUE = np.arange(1, DIM + 1).reshape((DIM, 1)) / (1.0 + DIM)        

def uvec(i, dim):
    """
    Creates a unit vector with 1 in `i`th position.
    """
    x = np.zeros((dim, 1), dtype=np.uint8)
    x[i] = 1
    return x
  
def generate_sequence(dim):
    """
    Generates a single sequence of the 5-state random walk and the reward.
    """
    idx = 2  
    seq = uvec(idx, dim)  
    while True:    
        idx = np.random.choice([idx + 1, idx - 1])
        if idx == -1:
            return seq, 0
        elif idx == DIM:
            return seq, 1
        else:
            seq = np.append(seq, uvec(idx, dim), axis=1)

def generate_training_set(dim):
    """
    Generates training set consisting of 10 sequences.
    """
    for _ in range(10):
        yield generate_sequence(dim)

def rms_diff(x1, x2):
    """
    Calculates RMS difference between vectors `x1` and `x2`.
    """
    if x1.shape == x2.shape:
        d_ = x1 - x2
        MSE = np.sum(d_ * d_) / float(len(d_))
        return np.sqrt(MSE)
    else:
        raise RuntimeError("Mismatched dimensions")  

def run_sequence(seq, wts, alpha, lambda_):
    """
    Calculate weight updates from a single sequence
    """
    X, z = seq
    dwts = np.zeros((DIM, 1))
    X = np.asmatrix(X)            
    P_next = np.dot(wts.T, X[:, 0])[0, 0]
    err = X[:, 0]
    _, m = X.shape

    # Looping over steps in a single walk                
    for t in range(m):
        P_prev = P_next
        if t == m - 1:
            P_next = z
        else:                
            x_next = X[:, t + 1]
            P_next = np.dot(wts.T, x_next)[0, 0]                   
        dwts += alpha * (P_next - P_prev) * err  
        err = x_next + lambda_ * err
    return dwts
    
def run_training_set(training_set, wts, alpha, lambda_, mode):            
    """
    Calculates weight updates from one training set
    """
    dwts_tot = np.zeros((DIM, 1))
    for sn, seq in enumerate(training_set):                     
        dwts = run_sequence(seq, wts, alpha, lambda_)
        if mode == "online":
            wts += dwts
        elif mode == "batch":
            dwts_tot += dwts
            
    # Add total accumulated updates to wts       
    if mode == "batch":
        wts += dwts_tot
    return wts

def run_experiment1():    
    MAX_ITER = 100 
    TRAINING_BATCH_SIZE = 100
    
    alpha = 0.027
    lambda_list = np.arange(0, 1.1, 0.1)
    rms_lambda = np.zeros(lambda_list.shape)
    rms_lambda_err = np.zeros(lambda_list.shape)
    
    for idx, lambda_ in enumerate(lambda_list):                
        rms_errors = []    
        for seed in range(TRAINING_BATCH_SIZE):
            np.random.seed(seed)
            training_set = list(generate_training_set(DIM))
            wts_new = np.full((DIM, 1), 0.5)
            wts_old = np.zeros((DIM, 1))                    
            niter = 0 
            while (niter < MAX_ITER) and (rms_diff(wts_new, wts_old) > 0.01):            
                wts_old = np.copy(wts_new)
                wts_new = run_training_set(training_set, wts_new, alpha, lambda_, "batch")
                niter += 1                  
            rms_errors.append(rms_diff(wts_new, WTS_TRUE))
            
        rms_lambda[idx] = np.mean(rms_errors)
        rms_lambda_err[idx] = np.std(rms_errors) / np.sqrt(TRAINING_BATCH_SIZE)
        print "lambda = %0.2f, RMSE = %0.6f" % (lambda_, np.mean(rms_errors))
        
    pl.close("all")
    fig = pl.figure(figsize=(5, 5))
    pl.errorbar(lambda_list, rms_lambda, yerr=rms_lambda_err / 2, 
                fmt='bo-', mec="none")
    pl.xlabel(r"$\lambda$")
    pl.ylabel(r"RMSE at best $\alpha$")
    pl.xlim([-0.1, 1.1])
    pl.ylim([0.08, 0.18])
    pl.savefig("fig3.pdf", bbox_inches="tight")

def run_experiment2():                
    TRAINING_BATCH_SIZE = 100
    lambda_list = np.arange(0, 1.1, 0.1)    
    alpha_list = np.arange(0.01, 0.65, 0.05)   
    nl = lambda_list.shape[0]
    na = alpha_list.shape[0]
    rms_alpha_lambda = np.zeros((nl, na))
    rms_alpha_lambda_err = np.zeros((nl, na))
    
    for il, lambda_ in enumerate(lambda_list):                
        for ia, alpha in enumerate(alpha_list):
            print "lambda_ = %0.2f, alpha = %0.2f" % (lambda_, alpha)
            rms_errors = []    
            for seed in range(TRAINING_BATCH_SIZE):
                np.random.seed(seed)
                training_set = generate_training_set(DIM)                        
                wts = run_training_set(training_set, 
                                       np.full((DIM, 1), 0.5), 
                                       alpha / 1.3, 
                                       lambda_, 
                                       "online")
                rms_errors.append(rms_diff(wts, WTS_TRUE))
                
            rms_alpha_lambda[il, ia] = np.mean(rms_errors)
            rms_alpha_lambda_err[il, ia] = np.std(rms_errors) / np.sqrt(TRAINING_BATCH_SIZE)                    

    # Figure 4
    pl.close("all")
    fig4 = pl.figure(figsize=(5,5))    
    for idx in range(nl):
        lambda_ = lambda_list[idx]
        if round(lambda_, 2) in [0.0, 0.3, 0.8, 1.0]:
            rms_lambda = rms_alpha_lambda[idx, :]
            rms_lambda_err = rms_alpha_lambda_err[idx, :]
            pl.errorbar(alpha_list, rms_lambda, yerr=rms_lambda_err / 2, 
                        fmt="o-", mec="none")                
            xc, yc = np.max(alpha_list) + 0.03, min(0.75, rms_lambda[-1])        
            pl.text(xc, yc, r"$\lambda = $ %0.1f" % lambda_list[idx])            
    pl.xlabel(r"$\alpha$")
    pl.ylabel("RMSE")
    pl.xlim([-0.07, 0.8])
    pl.ylim([0, 0.8])
    fig4.savefig("fig4.pdf", bbox_inches="tight")

    # Figure 5
    fig5 = pl.figure(figsize=(5,5))
    rms_best = np.min(rms_alpha_lambda, axis=1)
    pl.plot(lambda_list, rms_best, "ro-", mec="none", lw=2)
    pl.xlabel(r"$\lambda$")
    pl.ylabel(r"RMSE at best $\alpha$")
    pl.xlim([-0.07, 1.07])
    pl.ylim([0.08, 0.2])        
    fig5.savefig("fig5.pdf", bbox_inches="tight")

if __name__ == '__main__':
    run_experiment1()
    run_experiment2()
    
      
