import numpy as np


def rotate_mmn(mmn, umn, kpb_kidx, window=None):
    """
    Rotate the overlap matrices according to
    :math:`U^{(\mathbf{k})\dagger}M^{(\mathbf{k},\mathbf{b})}U^{(\mathbf{k}+\mathbf{b})}`

    """
    (nkpts, nntot, nbnds, nbnds) = mmn.shape
    nproj = umn[0].shape[1]

    mmn_rotated = np.empty((nkpts, nntot, nproj, nproj), dtype=complex)

    if window is not None:
        for ikpt in range(nkpts):
            for inn in range(nntot):
                ikpb = kpb_kidx[ikpt][inn]
                mmn_rotated[ikpt][inn] = (
                    np.dot(
                        np.dot(
                            umn[ikpt].conj().T, mmn[ikpt][inn][window[ikpt]][:, window[ikpb]],
                        ),
                        umn[ikpb]
                    )
                )
    else:
        for ikpt in range(nkpts):
            for inn in range(nntot):
                ikpb = kpb_kidx[ikpt][inn]
                mmn_rotated[ikpt][inn] = np.dot(np.dot(umn[ikpt].conj().T, mmn[ikpt][inn]), umn[ikpb])

    return mmn_rotated


# def change_gauge_k(m, u, setup_file):
#     (nkpts, nntot, nbnds, nbnds) = m.shape
#     nproj = u[0].shape[1]

#     m_rotated = np.zeros((nkpts, nntot, nproj, nbnds), dtype=complex)

#     for ikpt in range(nkpts):
#         for inn in range(nntot):
#             m_rotated[ikpt][inn] = np.dot(u[ikpt].conj().T, m[ikpt][inn])

#     return m_rotated


# def change_gauge_kpb(m, u, setup_file, kpb_kidx=None):
#     (nkpts, nntot, nbnds, nbnds) = m.shape
#     nproj = u[0].shape[1]

#     if kpb_kidx is None:
#         kpb_kidx = setup_file.kpb_kidx

#     m_rotated = np.zeros((nkpts, nntot, nbnds, nproj), dtype=complex)

#     for ikpt in range(nkpts):
#         for inn in range(nntot):
#             ikpb = kpb_kidx[ikpt][inn]
#             m_rotated[ikpt][inn] = np.dot(m[ikpt][inn], u[ikpb])

#     return m_rotated
