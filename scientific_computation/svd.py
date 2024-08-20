import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
from tqdm import tqdm
import seaborn as sns
sns.set_style("darkgrid")

from skimage.metrics import peak_signal_noise_ratio, structural_similarity
from utils.compress import memoryUsage, compressRatio


visualize = False
DPI = 150


imgRGB = imread("data/snoopy.png")
imgGrayScale = np.mean(imgRGB, axis=-1)
img_size = imgGrayScale.shape
img_dim = img_size[0]*img_size[1]

k = 200

U, d, V = np.linalg.svd(imgGrayScale, full_matrices=False)

d_k = d[:k]
U_k = U[:, :k]
V_k = V[:k, :]
D_k = np.diag(d_k)

imgCompress = U_k@D_k@V_k
imgCompressUsage = memoryUsage(U_k, d_k, V_k)
imgCompressRatio = compressRatio(img_dim, imgCompressUsage)

print("-"*10 + "{} singular values".format(k) + "-"*10)
print("compress ratio:", imgCompressRatio)
print("SSIM:", structural_similarity(imgGrayScale, imgCompress, data_range=1))
print("PSNR:", peak_signal_noise_ratio(imgGrayScale, imgCompress, data_range=1))

if visualize:

    fig, ax = plt.subplots(1, 2 ,figsize=(8, 4), dpi=DPI)
    ax[0].imshow(imgGrayScale, cmap="gray")
    ax[0].set_title("Original image memory usage: {}".format(img_dim))
    ax[0].axis("off")

    ax[1].imshow(imgCompress, cmap="gray")
    ax[1].set_title("Compressed image memory usage {}".format(imgCompressUsage))
    ax[1].axis("off")

    plt.tight_layout()
    plt.savefig("docs/svd_example")




if visualize:

    listRatio = []
    listSSIM = []
    listPSNR = []
    k_list = range(10, 610)

    for k in tqdm(k_list):
        d_k = d[:k]
        U_k = U[:, :k]
        V_k = V[:k, :]
        D_k = np.diag(d_k)

        img_k = U_k@D_k@V_k
        listRatio.append(compressRatio(img_dim, memoryUsage(U_k, d_k, V_k)))
        listSSIM.append(structural_similarity(imgGrayScale, img_k, data_range=1))
        listPSNR.append(peak_signal_noise_ratio(imgGrayScale, img_k, data_range=1))


    fig, ax = plt.subplots(3, 1 ,figsize=(10, 9), dpi=DPI)

    ax[0].plot(k_list, listRatio)
    ax[0].set_xlabel("$k$")
    ax[0].set_ylabel("compress ratio (%)")
    ax[0].grid("on")

    ax[1].plot(k_list, 100*np.array(listSSIM))
    ax[1].set_xlabel("$k$")
    ax[1].set_ylabel("SSIM (%)")
    ax[1].grid("on")

    ax[2].plot(k_list, listPSNR)
    ax[2].set_xlabel("$k$")
    ax[2].set_ylabel("PSNR")
    ax[2].grid("on")

    plt.tight_layout()
    plt.savefig("docs/svd_metrics")