import numpy as np

# normalizes the data with the maximum intensity
def normalize_volume(a_data):
    """
    Simple method to normalize a volume

    Args:
        a_data (N, M, K): array_like
                Volume to normalize
    
    Returns:
        A volume that has values in [0, 1] having the same shape as the input
    """
    if np.max(a_data) != 1.0:
        max_detect_count = np.max(a_data)

        for i in range(0, a_data.shape[0]):
            a_data[i] /= max_detect_count
            
    return a_data

def normalize_frames(a_data):
    """
    Simple method to normlize frames contained in a 3-rank tensor

    Args:
        a_data (N, M, K): array_like
                Frames of data index by i in N
    
    Returns:
        The normalized frames having the same shape as the input
    """
    if np.max(a_data) != 1.0:        

        for i in range(0, a_data.shape[0]):
            max_detect_count = np.max(a_data[i])
            a_data[i, :, :] /= max_detect_count
            
    return a_data