import sys, os
import numpy as np
import pandas as pd
from scipy.io.matlab import loadmat, savemat
from scipy.signal import filtfilt, cheby1, savgol_filter
import matplotlib.pyplot as plt
from FBCCA_IT import filter_bank_cca_it
# import seaborn as sns



def rms(data, axis=None):
    data = np.array(data)
    return np.sqrt(np.mean(data**2, axis=axis))

def sum_abs(data, axis=None):
    data = np.array(data)
    return np.sum(np.abs(data), axis=axis)

def get_noisiness_label(label):
    return f'{label}_{noisiness_metric_name}'

def get_mean_noisiness_label():
    return get_noisiness_label('mean')

def plot_trials(df_data):
    fig_trials, axes = plt.subplots(
        nrows=n_rows, ncols=n_cols,
        figsize=(ax_width*n_cols, ax_height*n_rows),
        sharey='all',
    )
    for i_ax, ax in enumerate(axes.ravel()):
        df_trial = df_data.iloc[i_ax]
        for channel_name in channel_names:
            ax.plot(df_trial[channel_name], alpha=alpha)
        ax.set_ylim(y_lims)
        ax.set_xlim(0, n_samples)
        ax.set_title(f'Block {df_trial["i_block"]}, Freq {df_trial["i_freq"]} ({df_trial["freq"]}Hz/"{df_trial["char"]}") ({get_mean_noisiness_label()}={df_trial[get_mean_noisiness_label()]:.2f})')
    fig_trials.tight_layout()
    return fig_trials

def generate_fig_name(fpath, suffix=None, prefix=None, sep='_', ext='png', append_metric_name=True):
    dirname = os.path.dirname(fpath)
    basename, _ = os.path.splitext(os.path.basename(fpath_mat))
    if append_metric_name:
        basename = f'{basename}{sep}{noisiness_metric_name}'
    if prefix is not None:
        basename = f'{prefix}{sep}{basename}'
    if suffix is not None:
        basename = f'{basename}{sep}{suffix}'
    return os.path.join(dirname, f'{basename}.{ext}')

if __name__ == '__main__':

    # data file, specified here or as command line argument
    fpath_mat = 'S02_typeC.mat'

    # number of trials to plot
    n_rows = 18
    n_cols = 5
    ax_width = 5
    ax_height = 1.5
    y_lims = [-200, 200]
    alpha = 0.7
    rejection_rms_threshold = [20]

    noisiness_metric_fn = rms
    noisiness_metric_name = 'rms'
    # noisiness_metric_fn = sum_abs
    # noisiness_metric_name = 'sum_abs'

    if fpath_mat is None:
        if len(sys.argv) != 2:
            print(f'Usage: {sys.argv[0]} path_to_mat_file')
            sys.exit(1)
        else:
            fpath_mat = sys.argv[1]

    # load data
    mat = loadmat(fpath_mat, simplify_cells=True)
    data = np.array(mat['data'], dtype=np.float64)
    freqs = mat['freqs']
    chars = mat['chars']

    n_channels, n_samples, n_freqs, n_blocks = data.shape
    channel_names = [f'channel{i_channel+1}' for i_channel in range(n_channels)]

    # build df with one row per trial
    # one column per channel + extra columns for other info
    dfs_data = []
    for i_freq in range(n_freqs):
        for i_block in range(n_blocks):

            data_trial = data[:, 80:-80, i_freq, i_block]

            # skip NA trials
            if np.sum(np.isnan(data_trial)) != 0:
                continue

            # 'raw' data
            data_for_df = {
                channel_name: [data_trial[i_channel, :]]
                for i_channel, channel_name in enumerate(channel_names)
            }

            # noisiness metric
            data_for_df.update({
                get_noisiness_label(channel_name): noisiness_metric_fn(data_for_df[channel_name])
                for channel_name in channel_names
            })

            # additional info
            data_for_df.update({
                'i_freq': i_freq,
                'i_block': i_block,
                'char': chars[i_freq],
                'freq': freqs[i_freq],
                get_mean_noisiness_label(): np.mean([data_for_df[get_noisiness_label(channel_name)] for channel_name in channel_names])
            })

            dfs_data.append(pd.DataFrame(data_for_df))
    df_data = pd.concat(dfs_data).reset_index()

    # plot histogram of noisiness metric averaged across all channels
    # print(df_data.sort_values(get_mean_noisiness_label(), ascending=False))
    # df_data.sort_values(get_mean_noisiness_label(), ascending=False).to_csv('noisy_data.csv')
    # print(df_data[df_data['mean_rms'] > rejection_rms_threshold][['i_freq', 'i_block']])
    # for index in df_data[(df_data['mean_rms'] > rejection_rms_threshold[ind][1]) | (df_data['mean_rms'] < rejection_rms_threshold[ind][0])][['i_freq', 'i_block']].to_numpy(dtype=int):

    accuracy_list_vs_rms = {'mean': [], 'std': []}
    for ind in range(len(rejection_rms_threshold)):
        for i_freq in range(n_freqs):
            for i_block in range(n_blocks):
                for i_channel in range(n_channels):
                    selected = df_data.loc[(df_data["i_freq"] == i_freq) & (df_data["i_block"] == i_block)][f'channel{i_channel+1}_rms']
                    if not selected.empty and selected.iloc[0] > rejection_rms_threshold[ind]:
                        print("removed (freq, block, channel):", i_freq, i_block, i_channel)
                        data[i_channel, :, i_freq, i_block] = 0     # interpoate here instead

        fpath_out = f'channel_cleaned_{fpath_mat}'
        savemat(fpath_out, {'data': data.tolist()})
        # cleaned_d = loadmat(fpath_out, simplify_cells=True)
        # print(np.shape(cleaned_d['data']))
        exit(0)

        data = loadmat(fpath_out, simplify_cells=True)['data']  # (8, 1250, 31, x)
        # data = loadmat('Sub02.mat')['data']
        # data = data.astype(float)
        if fpath_mat == 'S02_typeC.mat': data = np.delete(data, 4, axis=3)  # for S02
        freq_list = [5.85 + k * 0.16 for k in range(31)]
        acc = []
        pred = []
        num_blocks = 12 # S02=12, S08=15
        for test_i in range(num_blocks - 1):
            test_index = test_i
            data_test = data[:, :, :, test_index]  # 10 blocks, 4 is from 3 weeks ago, 6 from 3 week: S02, 5
            template_index = [k for k in range(num_blocks - 1)]
            template_index.remove(test_index)
            data_template = data[:, :, :, template_index]
            print(np.shape(data_template))
            data_template = np.nanmean(data_template, axis=3)  # mean-non
            results = []
            predictions = []
            onset = 40
            latency = 35
            d_len = 4.3
            for tar in range(len(freq_list)):
                beta, alpha = cheby1(N=2, rp=0.3, Wn=[5.5 / 125.0, 54.0 / 125.0], btype='band', output='ba')
                signal = data_test[:, :, tar]
                # print(signal)
                # print(np.array(signal))
                if np.isnan(signal[0, 0]):
                    print("signal is nan, so skipped.")
                    predictions.append(None)
                    continue
                signal = filtfilt(beta, alpha, signal)
                signal = savgol_filter(signal, 5, 2, mode='nearest')
                signal = signal.T
                # beta, alpha = cheby1(N=2, rp=0.3, Wn=[7/125.0, 90/125.0], btype='band', output='ba')
                rho_array = []
                for i in range(len(freq_list)):
                    template = filtfilt(beta, alpha, data_template[:, :, i])
                    template = savgol_filter(template, 5, 2, mode='nearest')
                    template = template.T

                    rho = filter_bank_cca_it(signal,
                                             freq_list[i],
                                             5.5, 54.0, 5,
                                             template,
                                             250.0)
                    rho_array.append(rho)
                print(np.argmax(rho_array))
                predictions.append(np.argmax(rho_array))
                results.append(int(np.argmax(rho_array) == tar))
            print(np.sum(results) / len(results))
            acc.append(np.sum(results) / len(results))
            print(predictions)
            pred.append(predictions)
        print(acc)
        print(np.mean(acc), np.std(acc))
        accuracy_list_vs_rms['mean'].append(np.mean(acc))
        accuracy_list_vs_rms['std'].append(np.std(acc))
        print(pred)
    np.save('results_py.npy', accuracy_list_vs_rms)

    plt.errorbar(rejection_rms_threshold, accuracy_list_vs_rms['mean'], yerr=accuracy_list_vs_rms['std'])
    plt.ylabel('Accuracy')
    plt.xlabel('Rejection_rms_threshold')
    plt.title('Python Version, 4.3s')
    plt.savefig('acc_vs_thr.png')
    plt.show()