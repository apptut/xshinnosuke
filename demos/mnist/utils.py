import gzip
from six.moves import urllib
import os
import platform
import pickle
import time


start_time = None
file_dir_path = os.path.dirname(__file__)


def format_size(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("Wrong format")
        return "Error"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.3fG" % G
        else:
            return "%.3fM" % M
    else:
        return "%.3fK" % kb


def schedule(blocknum, blocksize, totalsize):
    global start_time
    speed = (blocknum * blocksize) / (time.time() - start_time)
    speed_str = " Speed: %s" % format_size(speed)
    recv_size = blocknum * blocksize

    pervent = recv_size / totalsize
    percent_str = "%.2f%%" % (pervent * 100)
    n = round(pervent * 50)
    s = ('#' * n).ljust(50, '-')
    print('\r' + percent_str + '[' + s + ']' + speed_str, flush=True, end='')


def load_pickle(f):
    version = platform.python_version_tuple()
    if version[0] == '2':
        return pickle.load(f)
    elif version[0] == '3':
        return pickle.load(f, encoding='latin1')
    raise ValueError("invalid python version: {}".format(version))


def load_mnist(save_path=None):
    mnist_url = 'http://deeplearning.net/data/mnist/mnist.pkl.gz'
    if save_path is None:
        save_path = os.path.join(file_dir_path, 'data')
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    save_path = os.path.join(save_path, 'mnist.pkl.gz')
    if os.path.exists(save_path):
        print(f'{save_path} alread exists!')
    else:
        print('>> Downloading MNIST Dataset')
        global start_time
        start_time = time.time()
        urllib.request.urlretrieve(mnist_url, save_path, schedule)
        print('Successfully downloaded')
    with gzip.open(save_path, 'rb') as f:
        train_set, val_set, test_set = load_pickle(f)
        return train_set, val_set, test_set
