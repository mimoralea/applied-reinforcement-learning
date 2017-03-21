import numpy as np
import scipy as sp
import scipy.stats as stats
import csv
import time


def random_walk():
    states = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    state_idx = 3
    walk = [states[state_idx]]
    while states[state_idx] != 'A' and states[state_idx] != 'G':
        state_idx += np.random.choice([-1, 1])
        walk.append(states[state_idx])
    return walk


def generate_training_set(size):
    ts = []
    for i in range(0, size):
        ts.append(encode_walk(random_walk()))
    return ts


def prediction(state, weights):
    return np.dot(weights.T, state)


def encode_walk(walk):
    observations = np.zeros((len(walk) - 1, 5))
    i = 0
    last = ''
    for state in walk:
        if 'A' < state < 'G':
            observations[i, ord(state) - ord('B')] = 1
        i += 1
        last = state
    return observations, 1. if last == 'G' else 0.


def td_lambda(a, y, z, seq, weights):
    (l, ws) = seq.shape
    dw = np.array(weights)
    for i in range(0, l):
        p_t = prediction(seq[i], weights)
        p_t1 = z if i + 1 >= l else prediction(seq[i + 1], weights)
        delta = a * (p_t1 - p_t)
        for j in range(0, i + 1):
            l_mbda = y ** (i - j)
            dw += l_mbda * seq[j]
        dw *= delta
    return dw


def offline_training(a, y, ts, weights):
    dw = np.zeros(5)
    for (seq, z) in ts:
        dw += td_lambda(a, y, z, seq, weights)
    return weights + dw


def convergence_training(a, y, ts, weights):
    temp = weights
    new_weights = offline_training(a, y, ts, weights)
    count = 0
    while not np.allclose(new_weights, temp) and count < 1000:
        temp = new_weights
        new_weights = offline_training(a, y, ts, new_weights)
        count += 1
    return new_weights


def online_training(a, y, ts, weights):
    for (seq, z) in ts:
        weights += td_lambda(a, y, z, seq, weights)
    return weights


# noinspection PyTypeChecker
def error_calc(weights, target):
    sq_diff = (weights - target) ** 2
    return np.sqrt(np.mean(sq_diff))


def train_test_set(a, y, tss, expected, trainer, wgts):
    err = []
    for ts in tss:
        err.append(error_calc(trainer(a, y, ts, np.array(wgts)), expected))
    return np.array(err)


# def simple_tests():
#
#     wgts = np.ones(5) * 0.5
#     print online_training(0.1, 0.0, generate_training_set(10), wgts)
#     print online_training(0.1, 0.1, generate_training_set(1), wgts)
#     res = online_training(0.3, 0.3, generate_training_set(10), wgts)
#     print res
#     print error_calc(res, np.array([1. / 6., 1. / 3., 1. / 2., 2. / 3., 5. / 6.]))
#     print online_training(0.1, 0.5, generate_training_set(1), wgts)
#     print online_training(0.1, 0.7, generate_training_set(1), wgts)
#     print online_training(0.1, 0.9, generate_training_set(1), wgts)
#     print online_training(0.1, 1.0, generate_training_set(1), wgts)
#     print online_training(0.2, 1.0, generate_training_set(10), wgts)
#     print online_training(0.3, 1.0, generate_training_set(10), wgts)
#     print online_training(0.4, 1.0, generate_training_set(10), wgts)
#     print online_training(0.5, 1.0, generate_training_set(10), wgts)
#     print online_training(0.6, 1.0, generate_training_set(10), wgts)


def print_walk_stats(n):
    lens = []
    for i in range(0, n):
        lens.append(len(random_walk()))
    l = np.array(lens)
    print np.max(l), np.min(l), np.mean(l), np.std(l), stats.kurtosis(l)


def experiment_one(trials=100, ts_size=10, a=0.05):
    lambdas = [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 1.0]
    ideal_weights = np.array([1. / 6., 1. / 3., 1. / 2., 2. / 3., 5. / 6.])
    training_set = []
    wgts = np.array([0.45751024, 0.39232443, 0.62463452, 0.6664682, 0.33573614])
    # wgts = np.random.uniform(0.25, 0.75, 5)
    # wgts = np.random.sample(5)
    print wgts
    for k in range(0, trials):
        training_set.append(generate_training_set(ts_size))
    print "Running Experiment 1"
    results = []
    for lm in lambdas:
        print "Convergence training for lambda", lm
        test_set = train_test_set(a, lm, training_set, ideal_weights, convergence_training, wgts)
        results.append((lm, np.mean(test_set), np.std(test_set)))
    return results


def experiment_two(trials=100, ts_size=10):
    ideal_weights = np.array([1. / 6., 1. / 3., 1. / 2., 2. / 3., 5. / 6.])
    training_set = []
    for k in range(0, trials):
        training_set.append(generate_training_set(ts_size))

    lm = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    lf = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]

    init_prop = 0.5
    wgts = np.ones(5) * init_prop

    results = []
    err = np.zeros((len(lm), len(lf)))
    print "Running Experiment 2"
    for x in range(len(lm)):
        for y in range(len(lf)):
            print "Online training for lambda", lm[x], "and alpha", lf[y]
            test_set = train_test_set(lf[y], lm[x], training_set, ideal_weights, online_training, wgts)
            mean = np.mean(test_set)
            if np.isnan(mean):
                mean = 1E6
            results.append([lm[x], lf[y], mean])
            err[x, y] = mean
    return results, [[a, b] for (a, b) in zip(lm, np.min(err, axis=1))]


def write_output(filename, data):
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(data)


if __name__ == "__main__":
    # simple_tests()
    print np.__version__
    print sp.__version__
    seed = int(time.time())
    seed = 1474676106
    print seed
    np.random.seed(seed)

    exp1 = experiment_one()
    write_output("experiment1.csv", exp1)

    seed = 1474674565
    exp2, mins = experiment_two()
    write_output("experiment2.csv", exp2)
    write_output("experiment2_1.csv", mins)

