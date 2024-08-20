import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
from tqdm import tqdm
import time
import seaborn as sns
sns.set_style("darkgrid")

from skimage.metrics import peak_signal_noise_ratio, structural_similarity
from utils.alternating import als
from utils.compress import compressRatio


visualize = False
DPI = 150


imgRGB = imread("data/snoopy.png")
imgGrayScale = np.mean(imgRGB, axis=-1)
img_size = imgGrayScale.shape
img_dim = img_size[0]*img_size[1]

k = 200

W, H = als(imgGrayScale, k=k, num_iter=10)
imgReconstruct = W@H
imgCompressUsage = W.shape[0]*W.shape[1] + H.shape[0]*H.shape[1]
imgCompressRatio = compressRatio(img_dim, imgCompressUsage)

print("-"*10 + "{} singular values".format(k) + "-"*10)
print("compress ratio:", imgCompressRatio)
print("SSIM:", structural_similarity(imgGrayScale, imgReconstruct, data_range=1))
print("PSNR:", peak_signal_noise_ratio(imgGrayScale, imgReconstruct, data_range=1))

if visualize:

    fig, ax = plt.subplots(1, 2 ,figsize=(8, 4), dpi=DPI)
    ax[0].imshow(imgGrayScale, cmap="gray")
    ax[0].set_title("Original image memory usage: {}".format(img_dim))
    ax[0].axis("off")

    ax[1].imshow(imgReconstruct, cmap="gray")
    ax[1].set_title("Compressed image memory usage {}".format(imgCompressUsage))
    ax[1].axis("off")

    plt.tight_layout()
    plt.savefig("docs/als_example")




if visualize:

    listTime = []
    listSSIM = []
    listPSNR = []
    iter_list = range(1, 50)

    for i in tqdm(iter_list):
        tic = time.time()
        W, H = als(imgGrayScale, k=k, num_iter=i)
        toc = time.time()
        img_k = W@H
        listTime.append(toc-tic)
        listSSIM.append(structural_similarity(imgGrayScale, img_k, data_range=1))
        listPSNR.append(peak_signal_noise_ratio(imgGrayScale, img_k, data_range=1))


    fig, ax = plt.subplots(3, 1 ,figsize=(10, 9), dpi=DPI)

    ax[0].plot(iter_list, listTime)
    ax[0].set_xlabel("iteration")
    ax[0].set_ylabel("time (sec)")
    ax[0].grid("on")

    ax[1].plot(iter_list, 100*np.array(listSSIM))
    ax[1].set_xlabel("iteration")
    ax[1].set_ylabel("SSIM (%)")
    ax[1].grid("on")

    ax[2].plot(iter_list, listPSNR)
    ax[2].set_xlabel("iteration")
    ax[2].set_ylabel("PSNR")
    ax[2].grid("on")

    plt.tight_layout()
    plt.savefig("docs/als_metrics")