import numpy as np
import matplotlib.pyplot as plt

cblue = "#2980B9"
cred = "#E74C3C"

def plot_path(pred_path, gt_path, sequence):

    gt_path = np.array(gt_path)
    pred_path = np.array(pred_path)

    save_path = "docs/{0:0=2d}".format(sequence)

    plt.figure()
    plt.plot([x for x in pred_path[:, 0]], [z for z in pred_path[:, 1]], c=cblue) 
    plt.plot([x for x in gt_path[:, 0]], [z for z in gt_path[:, 1]], c=cred) 
    plt.grid()
    plt.title("VO - Seq {0:0=2d}".format(sequence))
    plt.xlabel("Translation in x direction [m]")
    plt.ylabel("Translation in z direction [m]")
    plt.legend(["estimated", "ground truth"])
    plt.savefig(save_path)