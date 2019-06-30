from __future__ import absolute_import, print_function, unicode_literals
import os
import os.path as osp
import glob
import numpy as np
import imageio
import six
import pandas as pd
from collections import OrderedDict



class MOBIFACE(object):
    def __init__(self, root_dir, subset='all'):
        assert subset in ['all', 'train', 'test']

        self.root_dir = root_dir
        self.subset = subset

        self.train_meta_fn = osp.join(root_dir, 'train.meta.csv')
        self.test_meta_fn = osp.join(root_dir, 'test.meta.csv')

        self.train_meta = pd.read_csv(self.train_meta_fn,index_col=0).transpose().to_dict()
        self.test_meta = pd.read_csv(self.test_meta_fn,index_col=0).transpose().to_dict()


        # self.train_anno_files = [osp.abspath(osp.join(self.root_dir,'train', s+'.annot.csv')) for s in self.train_seq_names]
        # self.test_anno_files = [osp.abspath(osp.join(self.root_dir,'test', s+'.annot.csv')) for s in self.test_seq_names]



        if subset == 'all':
            self.meta = {**self.train_meta, **self.test_meta} # In Python 3.5 or greater
        elif subset == 'train':
            self.meta = self.train_meta
        else:
            self.meta = self.test_meta

        self.meta = OrderedDict(sorted(self.meta.items(), key=lambda t: t[0]))
        self.anno_files = []
        for k,v in self.meta.items():
            if k in self.train_meta.keys():
                self.anno_files.append(osp.abspath(osp.join(self.root_dir,'train', k+'.annot.csv')))
            else:
                self.anno_files.append(osp.abspath(osp.join(self.root_dir,'test', k+'.annot.csv')))
        self.seq_dirs = [fn[:-len('.annot.csv')] for fn in self.anno_files]
        self.seq_names = sorted(list(self.meta.keys()))
        self._check_dataset()

    def __len__(self):
        return len(self.seq_names)

    def __getitem__(self, index):
        r"""        
        Args:
            index (integer or string): Index or name of a sequence.
        
        Returns:
            tuple: (img_files, anno), where ``img_files`` is a list of
                file names and ``anno`` is a N x 4 (rectangles) numpy array.
        """
        if isinstance(index, six.string_types):
            if not index in self.seq_names:
                raise Exception('Sequence {} not found.'.format(index))
            index = self.seq_names.index(index)

        img_files = sorted(glob.glob(self.seq_dirs[index]+'/*.jpg'))
        if len(img_files) == 0:
            img_files = sorted(glob.glob(self.seq_dirs[index]+'.png'))


        # to deal with different delimeters
        with open(self.anno_files[index], 'r') as f:
            anno = np.loadtxt(f, delimiter=',', skiprows=1, dtype=int)
        anno = anno[:,1:]
        assert anno.shape[1] == 4

        return img_files, anno

    def _check_dataset(self):
        for vid_dir in self.seq_dirs:
            assert osp.isdir(vid_dir)
            assert len(os.listdir(vid_dir)) > 0

    def _vid_to_img(self):
        from tqdm import tqdm
        for vid_dir in self.seq_dirs:
            if not osp.isdir(vid_dir):
                os.makedirs(vid_dir)
            vid = vid_dir + '.mp4'
            assert osp.isfile(vid)
            reader = imageio.get_reader(vid)
            for i, im in tqdm(enumerate(reader),desc='decoding ' + vid, total=reader.get_length()):
                img_fn = osp.join(vid_dir, '{:08d}.jpg'.format(i))
                imageio.imwrite(img_fn, im)
            reader.close()





            

        
