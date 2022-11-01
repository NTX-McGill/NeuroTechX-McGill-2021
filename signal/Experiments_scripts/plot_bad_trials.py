#!/usr/bin/env python

import sys, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.io.matlab import loadmat, savemat

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
    rejection_rms_threshold = 15.0

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
    print(df_data[df_data['mean_rms'] > rejection_rms_threshold][['i_freq', 'i_block']])
    for index in df_data[df_data['mean_rms'] > rejection_rms_threshold][['i_freq', 'i_block']].to_numpy(dtype=int):
        print(index)
        data[:, :, index[0], index[1]] = None
    fpath_out = f'cleaned_{fpath_mat}'
    savemat(fpath_out, {'data': data.tolist()})
    cleaned_d = loadmat(fpath_out, simplify_cells=True)
    print(np.shape(cleaned_d['data']))
    exit(0)

    fig_hist, ax_hist = plt.subplots()
    sns.histplot(df_data[get_mean_noisiness_label()], ax=ax_hist, bins=60)
    fig_hist.savefig(generate_fig_name(fpath_mat, f'hist'), dpi=300, bbox_inches='tight')

    # plot raw signals for top/bottom noisy trials
    n_trials = n_rows * n_cols
    fig_top_trials = plot_trials(df_data.sort_values(get_mean_noisiness_label(), ascending=False).iloc[:n_trials])
    fig_top_trials.savefig(generate_fig_name(fpath_mat, f'top{n_trials}'), dpi=300, bbox_inches='tight')

    fig_bottom_trials = plot_trials(df_data.sort_values(get_mean_noisiness_label(), ascending=True).iloc[:n_trials])
    fig_bottom_trials.savefig(generate_fig_name(fpath_mat, f'bottom{n_trials}'), dpi=300, bbox_inches='tight')
