def memoryUsage(U, d, V):
    return U.shape[0]*U.shape[1] + d.shape[0] + V.shape[0]*V.shape[1]

def compressRatio(original_usage, compressed_usage):
    return 100*(compressed_usage/original_usage)