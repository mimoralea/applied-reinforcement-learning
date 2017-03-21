import numpy as np
import matplotlib.pyplot as plt
import random


def sample(states, start, terminal_states):
    if start not in states or len(set(terminal_states) - set(states)) > 0:
        return []
    st_index = states.index(start)
    st = start
    sequence = [st]
    while st not in terminal_states:
        direction = random.randrange(0, 2)
        if direction <= 0:
            st_index -= 1  # move left
        else:
            st_index += 1  # move right
        st = states[st_index]
        sequence.append(st)
    return sequence


def generate_training_sets(num_set, num_sequence, states, start, terminal_states):
    """
    method to generate training sets
    :param num_set: number of training sets
    :param num_sequence: number of sequence per set
    :param states: all states
    :param start: starting state
    :param terminal_states: terminal states
    :return:
    """
    return [[sample(states, start, terminal_states) for i in xrange(num_sequence)] for j in xrange(num_set)]


def experiment1(training_sets, states, terminal_states, rewards, alpha, _lambda):
    states_list = sorted(list(set(states) - set(terminal_states)))
    states_dict = {}
    for i, s in enumerate(states_list):
        states_dict[s] = i
    num_states = len(states_list)
    T = [1./6, 1./3, 1./2, 2./3, 5./6]
    rmse_list = []
    w = np.zeros((num_states,))
    # w = np.array([.5, .5, .5, .5, .5])

    for training_set in training_sets:
        converged = False
        count = 0

        while not converged:
            prev_w = np.copy(w)

            dw = np.zeros((num_states,))
            for sequence in training_set:
                new_dw = calculate_eligibility(sequence, states_dict, terminal_states, rewards, num_states, w, alpha, _lambda)
                dw += new_dw

            # only update weights after each training_set
            w += dw

            error = calculate_rmse(prev_w, w)
            count += 1

            if error < 0.0005:
                # print('Converged in {count} count'.format(**{'count': count}))
                converged = True

        # calculate error between w and T
        rmse_list.append(calculate_rmse(w, T))

    # trim outliars
    rmse_list = sorted(rmse_list)[10:-10]
    # calculate avg for rmse
    rmse_avg = np.average(rmse_list)
    return rmse_avg


def calculate_eligibility(sequence, states_dict, terminal_states, rewards, num_states, w, alpha, _lambda):
    dw = np.zeros((num_states,))
    prev_del_w = np.zeros((num_states,))

    for i, st in enumerate(sequence[:-1]):
        # current state t
        xt_index = states_dict[st]
        xt = np.zeros((num_states,))
        xt[xt_index] = 1.
        Pt = np.sum(w * xt)
        Pt_1 = 0

        # next state t + 1
        st_1 = sequence[i + 1]
        if st_1 in states_dict:
            xt_1_index = states_dict[st_1]
            xt_1 = np.zeros((num_states,))
            xt_1[xt_1_index] = 1.
            Pt_1 = np.sum(w * xt_1)
        else:
            for idx, s in enumerate(terminal_states):
                if s == st_1:
                    Pt_1 = rewards[idx]
                    break

        # calculate del or nabla
        del_w = xt + prev_del_w * _lambda
        # calculate delta w
        dw += alpha * (Pt_1 - Pt) * del_w

        prev_del_w = del_w
    return dw


def experiment2(training_sets, states, terminal_states, rewards, alpha, _lambda):
    # First, each training set was presented once to each procedure.
    # Second, weight updates were performed after each sequence, as in (1), rather than after each complete training set
    # Third, each learning procedure was applied with a range of values for the learning-rate parameter alpha
    # Fourth, so that there was no bias either toward rightside or leftside terminations, all components of the weight
    #     vector were initially set to 0.5.
    states_list = sorted(list(set(states) - set(terminal_states)))
    states_dict = {}
    for i, s in enumerate(states_list):
        states_dict[s] = i
    num_states = len(states_list)
    T = [1./6, 1./3, 1./2, 2./3, 5./6]
    rmse_list = []
    # w = np.zeros((num_states,))

    for training_set in training_sets:
        w = np.array([.5, .5, .5, .5, .5])
        errors = []
        for sequence in training_set:
            dw = calculate_eligibility(sequence, states_dict, terminal_states, rewards, num_states, w, alpha, _lambda)
            # update weights right away
            w += dw
            # # calculate error between w and T
            errors.append(calculate_rmse(w, T))
        # get average of errors
        rmse_list.append(np.average(errors))

    # trim outliars
    rmse_list = sorted(rmse_list)[10:-10]
    # calculate avg for rmse
    rmse_avg = np.average(rmse_list)
    return rmse_avg


def calculate_rmse(prediction, actual):
    rmse = np.sqrt(np.sum((prediction - actual) ** 2) / len(actual))
    return rmse


def execute_experiment1(training_sets, states, terminal_states, rewards):
    alpha = 0.005
    lambdas = [0., 0.1, 0.3, 0.5, 0.7, 0.9, 1.]
    rmse_list = []
    for _lambda in lambdas:
        rmse = experiment1(training_sets, states, terminal_states, rewards, alpha, _lambda)
        rmse_list.append(rmse)

    fig, ax = plt.subplots()
    plt.xlabel(r'$\lambda$')
    plt.ylabel('ERROR')
    ax.plot(lambdas, rmse_list, '-o', label='Widrow-Hoff')
    ax.text(lambdas[-1]-0.075, rmse_list[-1]+0.0025, 'Widrow-Hoff', fontsize=10)
    ax.margins(0.1)
    plt.legend(loc='lower right')
    fig.savefig('fig3.png')
    return rmse_list


def execute_experiment2(training_sets, states, terminal_states, rewards):
    alphas = np.linspace(0, 0.6, 13)  # alpha every 0.05
    lambdas = np.linspace(0, 1, 11)  # [0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.]
    rmse_list = []
    for _lambda in lambdas:
        rmse_lambda_list = []
        for alpha in alphas:
            rmse = experiment2(training_sets, states, terminal_states, rewards, alpha, _lambda)
            rmse_lambda_list.append(rmse)
        rmse_list.append(rmse_lambda_list)

    fig, ax = plt.subplots()
    plt.xlabel(r'$\alpha$')
    plt.ylabel('ERROR')
    ax.margins(0.1)
    for i, array in enumerate(rmse_list):
        if True:
            y = []
            for rmse in array:
                if rmse <= .7:
                    y.append(rmse)
            x = alphas[:len(y)]
            ax.plot(x, y, '-o', label=r'$\lambda=$' + str(lambdas[i]))
            ax.text(x[-1] - .02, y[-1] + .02, r'$\lambda=$' + str(lambdas[i]), fontsize=10)
    plt.legend(loc='upper left')
    fig.savefig('fig4-all.png')

    fig, ax = plt.subplots()
    plt.xlabel(r'$\alpha$')
    plt.ylabel('ERROR')
    ax.margins(0.1)
    for i, array in enumerate(rmse_list):
        if i in [0, 3, 8, 10]:
            y = []
            for rmse in array:
                if rmse <= .7:
                    y.append(rmse)
            x = alphas[:len(y)]
            ax.plot(x, y, '-o', label=r'$\lambda=$' + str(lambdas[i]))
            ax.text(x[-1] - .02, y[-1] + .02, r'$\lambda=$' + str(lambdas[i]), fontsize=10)
    plt.legend(loc='upper left')
    fig.savefig('fig4.png')
    return rmse_list


def execute_figure5(training_sets, states, terminal_states, rewards, rmse_list):
    arr = np.array(rmse_list)
    min_lambda, min_alpha = np.where(arr == np.min(arr))
    alphas = np.linspace(0, 0.6, 13)
    lambdas = np.linspace(0, 1, 11)
    alpha = alphas[min_alpha][0]
    _lambda = lambdas[min_lambda][0]
    print('min lambda', _lambda)
    print('min alpha', alpha)

    lambdas = [0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.]
    rmse_list = []
    for _lambda in lambdas:
        rmse = experiment2(training_sets, states, terminal_states, rewards, alpha, _lambda)
        rmse_list.append(rmse)
    print rmse_list

    fig, ax = plt.subplots()
    plt.xlabel(r'$\lambda$')
    plt.ylabel('ERROR')
    ax.plot(lambdas, rmse_list, '-o', label='Widrow-Hoff')
    ax.text(lambdas[-1]-0.075, rmse_list[-1]+0.0025, 'Widrow-Hoff', fontsize=10)
    ax.margins(0.1)
    plt.legend(loc='lower right')
    fig.savefig('fig5.png')


def main():
    states = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    start = 'd'
    terminal_states = ['a', 'g']
    rewards = [0, 1]

    training_sets = generate_training_sets(100, 10, states, start, terminal_states)

    execute_experiment1(training_sets, states, terminal_states, rewards)
    rmse_list = execute_experiment2(training_sets, states, terminal_states, rewards)
    execute_figure5(training_sets, states, terminal_states, rewards, rmse_list)


if __name__ == '__main__':
    main()

