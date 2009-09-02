"""
Functions to read series and masks on the raw data.
"""

# Major scientific libraries import
import numpy as np

# Neuroimaging library imports
import nipy.neurospin.utils.mask as mask_utils


################################################################################
# Series and mask extraction 
################################################################################

def series_from_mask(session_files, mask):
    """ Read the time series from the given sessions filenames, using the mask.

        Parameters
        -----------
        session_files: list of list of nifti file names. 
            Files are grouped by session.
        mask: 3d ndarray
            3D mask array: true where a voxel should be used.
        
        Returns
        --------
        session_series: ndarray
            3D array of time course: (session, voxel, time)
    """
    mask = mask.astype(np.bool)
    session_series = np.zeros((len(session_files), mask.sum(), 
                                            len(session_files[0])),
                                    np.float32)
    for session_index, filenames in enumerate(session_files):
        for file_index, filename in enumerate(filenames):
            data = mask_utils.load_nifti(filename).asarray().T
                
            session_series[session_index, :, file_index] = \
                            data[mask].astype(np.float32)
            # Free memory early
            del data

    return session_series.squeeze()

