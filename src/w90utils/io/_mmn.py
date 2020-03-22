import numpy as np


__all__ = ['read_mmn', 'write_mmn']


def _process_mmn_file(fname):
    with open(fname, 'r') as f:
        contents = f.readlines()

    header = contents[0]

    [nbnds, nkpts, nntot] = np.fromstring(contents[1], sep=' ', dtype=int)

    nblks = nkpts * nntot
    # a block consists of the header line and the following nbnds**2 lines
    blk_len = nbnds**2 + 1
    # indices of the starting line of each block
    blk_start_idx = list(range(2, len(contents), blk_len))

    kpb_kidx = np.zeros((nkpts, nntot), dtype=int)
    kpb_g = np.zeros((nkpts, nntot, 3), dtype=int)
    mmn = np.zeros((nkpts, nntot, nbnds, nbnds), dtype=complex)
    for (iblk, istart) in enumerate(blk_start_idx):
        # determine kpoint-index and nearest-neighbor index
        # based on the index of the block
        # --------------------------------------------------
        ikpt = iblk // nntot
        if iblk % nntot == 0:
            inn = 0
        else:
            inn += 1
        # --------------------------------------------------
        block = contents[istart:(istart+blk_len)]
        block_header = block[0]
        kpb_kidx[ikpt][inn] = int(block_header.split()[1]) - 1
        kpb_g[ikpt][inn] = list(map(int, block_header.split()[2:]))
        s = ''.join(block[1:])
        a = np.fromstring(s, sep='\n').view(complex)
        mmn[ikpt, inn, :, :] = a.reshape((nbnds, nbnds), order='F')

    return mmn, kpb_kidx, kpb_g


def read_mmn(fname):
    """
    Read MMN file

    Parameters
    ----------
    fname : str

    Returns
    -------
    mmn : ndarray, shape (nkpts, nntot, nbnds, nbnds)

    """
    return _process_mmn_file(fname)[0]


def write_mmn(fname, mmn, kpb_kidx, kpb_g):
    """
    Write :math:`M^{(\mathbf{k},\mathbf{b})}_{mn}` to MMN file

    Parameters
    ----------
    fname : str
    mmn : ndarray, shape (nkpts, nntot, nbnds, nbnds)

    """
    nkpts = mmn.shape[0]
    nntot = mmn.shape[1]
    nbnds = mmn.shape[2]
    with open(fname, 'w') as f:
        print('DUMMY HEADER', file=f)
        print('%12d%12d%12d' % (nbnds, nkpts, nntot), file=f)
        for ikpt in range(nkpts):
            for inn in range(nntot):
                print('%5d%5d%5d%5d%5d' % ((ikpt+1, kpb_kidx[ikpt][inn]+1) + tuple(kpb_g[ikpt][inn])), file=f)
                np.savetxt(f, mmn[ikpt][inn].flatten(order='F').view(float).reshape(-1, 2), fmt='%18.12f%18.12f')
