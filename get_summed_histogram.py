import numpy as np
import analysis_utils as utils
import h5py
import os

sphere = 'sphere_20241221'
dataset = '20241221_3e-7mbar_16e_alignment0_long'
data_prefix = r'20241221_d_'
data_dir = f'/Users/yuhan/work/nanospheres/data/dm_data_processed/{sphere}/{dataset}'

nfile = 1331

outfile_name = f'{dataset}_summed_histograms.hdf5'

excess_thr = 1600
noise_thr = 400

hists = utils.load_data_hists(data_dir, data_prefix, nfile, excess_thr, noise_thr)

bc, hhs, hh_cut_det, hh_cut_noise, hh_cut_all = hists[0], hists[1], hists[2], hists[3], hists[4]

hh_all_sum = np.sum(np.sum(hhs, axis=0), axis=0)
hh_cut_det_sum = np.sum(hh_cut_det, axis=0)
hh_cut_noise_sum = np.sum(hh_cut_noise, axis=0)
hh_cut_all_sum = np.sum(hh_cut_all, axis=0)

n_search_per_win = (5000 - 150) / 25
time_per_search = 2e-6 * 25
scaling = n_search_per_win * time_per_search * (hists[0][1] - hists[0][0])

n_window_all = hhs.shape[0] * hhs.shape[1]
n_window_cut_det = hh_cut_det.shape[0]
n_window_cut_noise = hh_cut_noise.shape[0]
n_window_cut_all = hh_cut_all.shape[0]

with h5py.File(os.path.join(data_dir, outfile_name), 'w') as fout:
    print(f'Writing file {os.path.join(data_dir, outfile_name)}')

    g = fout.create_group('summed_histograms')
    g.attrs['bin_center_kev'] = bc
    g.attrs['scaling'] = scaling

    g0 = g.create_dataset('hh_all_sum', data=hh_all_sum, dtype=np.int64)
    g1 = g.create_dataset('hh_cut_det_sum', data=hh_cut_det_sum, dtype=np.int64)
    g2 = g.create_dataset('hh_cut_noise_sum', data=hh_cut_noise_sum, dtype=np.int64)
    g3 = g.create_dataset('hh_cut_all_sum', data=hh_cut_all_sum, dtype=np.int64)

    g0.attrs['n_window'] = n_window_all
    g1.attrs['n_window'] = n_window_cut_det
    g2.attrs['n_window'] = n_window_cut_noise
    g3.attrs['n_window'] = n_window_cut_all

    fout.close()