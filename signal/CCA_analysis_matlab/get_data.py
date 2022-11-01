import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

import math
import numpy as np
import pandas as pd
from scipy.signal import iirnotch, filtfilt
from scipy.io.matlab import savemat

# parameters
SUBJECT_ID = 'S09'
FREQ_TYPE = 'C'
VERBOSE = True  # if True, prints some output to screen

BAD_COLLECTION_IDS = [44, 80]  # runs that should not be included in the data
REF_FREQ_MAP = {
    # add 0.001 to upper bound because np.arange() doesn't include endpoint
    # round to 2 decimal places to avoid mismatches due to numerical errors
    'A': {*np.around(np.arange(8, 15.751, 0.25), decimals=2)} - {12},
    'B': {*np.around(np.arange(5.1, 12.851, 0.25), decimals=2)} - {10.85},
    'C': {*np.around(np.arange(5.85, 10.651, 0.16), decimals=2)},
}

FPATH_DOTENV = 'config.env'

FS = 250  # sampling frequency
TRIAL_DURATION = 5  # in seconds
N_CHANNELS = 8
CHANNEL_NAMES = [f'channel_{i + 1}' for i in range(N_CHANNELS)]


def infer_freq_type(freqs):
    '''Returns a frequency type based on a list of (possibly incomplete) frequencies.'''

    freqs = {*freqs}  # convert to set
    for freq_type, ref_freqs in REF_FREQ_MAP.items():
        # check if freqs is a subset of ref_freqs
        if len(freqs - ref_freqs) == 0:
            return freq_type
    raise ValueError(f'No frequency configuration matched for freqs {freqs}')


def get_subject_data(database_url, subject_id, target_freq_type, bad_collection_ids=[], verbose=True):
    '''
    Downloads a subject's runs from a database and selects those with the target frequency type.
    Returns a list of pandas dataframes (one for each data collection run).
    '''

    # connect to database server
    alchemy_engine = create_engine(database_url)
    with alchemy_engine.connect() as db_connection:

        target_freq_type = target_freq_type.upper()

        # bci_collection table has one row per data collection session
        # each session has an associated collector_name
        bci_collection = pd.read_sql("SELECT * FROM bci_collection", db_connection)
        all_ids = bci_collection['collector_name']

        # add some flexibility for the subject ID
        # ex: S09 has 3 trials called 'S09_trial1', 's09_trial2', and 's09_trial3'
        subject_ids = {id for id in all_ids if subject_id.lower() in id.lower()}
        if verbose:
            print(f'Looking for sessions with collector name in {subject_ids}')

        # find all collection IDs for the subject
        collection_ids = bci_collection.loc[bci_collection['collector_name'].isin(subject_ids), 'id'].drop_duplicates()
        collection_ids = [id for id in collection_ids if id not in bad_collection_ids]
        if verbose:
            print(f'Found {len(collection_ids)} sessions (some may not have any data)')

        # get the subject's data in a list of pandas dataframes
        # each dataframe contains data for a single session
        subject_data = []
        for collection_id in collection_ids:

            df_run = pd.read_sql(f"SELECT * FROM collected_data WHERE collection_id = {collection_id}", db_connection)

            n_rows_per_character = df_run['character'].value_counts()
            freq_type = infer_freq_type(df_run['frequency']).upper()

            # if the dataframe is not empty and if the frequency type is correct
            if n_rows_per_character.sum() > 0 and freq_type == target_freq_type:
                subject_data.append(df_run)

                if verbose:
                    print(f'Collection ID: {collection_id}')
                    print(f'\t{len(n_rows_per_character)} characters ({df_run.shape[0]} rows)')
                    print(f'\tAverage number of rows per character: {n_rows_per_character.mean():.0f}')
                    print(f'\tFrequency range: {df_run["frequency"].min()}-{df_run["frequency"].max()} Hz')

        if verbose:
            print(f'Added data from {len(subject_data)} runs with frequency type {target_freq_type}')

    return subject_data


def remove_dc_offset(data, fs, chunk_length=0.5):
    '''Splits the data into chunks of fixed length, substract channel-wise mean from each chunk.'''
    n_samples = data.shape[0]
    n_chunks = math.ceil(n_samples / (chunk_length * fs))
    processed_chunks = []
    for chunk in np.array_split(data, n_chunks):
        processed_chunks.append(chunk - np.mean(chunk, axis=0))
    return np.concatenate(processed_chunks, axis=0)


def notch_filter(data, fs, freq=60, Q=10):
    '''Applies notch filter to timeseries data of shape (n_samples, n_channels).'''
    b, a = iirnotch(freq, Q, fs=fs)
    return filtfilt(b, a, data, axis=0)


def preprocess_trial(data, fs, dc_chunk_length=0.5, notch_freq=60, notch_Q=10):
    '''Removes DC offset and filters data.'''
    data = remove_dc_offset(data, fs, chunk_length=dc_chunk_length)
    data = notch_filter(data, fs, freq=notch_freq, Q=notch_Q)
    return data


if __name__ == '__main__':

    # get database URL from environment variable
    load_dotenv(FPATH_DOTENV)
    database_url = os.environ.get('DATABASE_URL')

    # get data from sessions of interest (one dataframe per session)
    subject_data = get_subject_data(database_url, SUBJECT_ID, FREQ_TYPE,
                                    bad_collection_ids=BAD_COLLECTION_IDS, verbose=VERBOSE)

    freqs = sorted(list(REF_FREQ_MAP[FREQ_TYPE]))  # list of all expected frequencies
    freq_char_map = dict.fromkeys(freqs, None)
    n_samples_per_trial = FS * TRIAL_DURATION

    all_blocks = []
    for i_run, run_data in enumerate(subject_data):

        if VERBOSE:
            if i_run == 0:
                print('----------')
            print(f'Run {i_run + 1}')

        block_data = []
        run_data_grouped = run_data.groupby('frequency')
        for freq in freqs:
            try:
                trial_data = run_data_grouped.get_group(freq)

            # missing target --> add a matrix of NaNs
            except KeyError:
                if VERBOSE:
                    print(f'Missing freq: {freq} Hz')
                nan_trial = np.empty((n_samples_per_trial, N_CHANNELS))
                nan_trial[:] = np.nan
                block_data.append(nan_trial)
                continue

            # update dictionary of frequency-character pairs
            char = trial_data['character'].iloc[0]
            if freq_char_map[freq] is None:
                if char == '\b':
                    char = '\\b'  # escape this for MATLAB to be able to read it as '\b'
                freq_char_map[freq] = char

            # extract and preprocess EEG channel data
            trial_data = trial_data.sort_values('order').reset_index(drop=True)
            trial_data = trial_data.loc[:n_samples_per_trial - 1, CHANNEL_NAMES]
            trial_data_preprocessed = preprocess_trial(trial_data.to_numpy(), FS)
            block_data.append(trial_data_preprocessed)

        if VERBOSE:
            print('----------')

        all_blocks.append(block_data)

    # final shape is (n_channels, n_samples, n_characters, n_blocks)
    all_blocks = np.array(all_blocks, dtype=object).T  # want cell array in MATLAB
    if VERBOSE:
        print(f'Final matrix shape: {all_blocks.shape}')

    # get a list of characters sorted by increasing frequency
    char_freq_map = {c: f for (f, c) in freq_char_map.items()}
    chars = sorted(char_freq_map.keys(), key=(lambda x: char_freq_map[x]))
    chars = np.array(chars, dtype=object)  # want cell array in MATLAB

    # save to .mat file
    fpath_out = f'{SUBJECT_ID}_type{FREQ_TYPE}.mat'
    savemat(fpath_out, {'data': all_blocks, 'freq_type': FREQ_TYPE, 'freqs': freqs, 'chars': chars})
    if VERBOSE:
        print(f'Saved to {fpath_out}')