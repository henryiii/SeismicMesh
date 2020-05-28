import os

import numpy as np
from mpi4py import MPI

import SeismicMesh

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()


def test_3dpar_mesher():

    fname = os.path.join(os.path.dirname(__file__), "test3D.bin")
    wl = 10
    hmin = 50
    freq = 4
    grade = 0.15
    nz, nx, ny = 20, 10, 10
    ef = SeismicMesh.MeshSizeFunction(
        bbox=(-2e3, 0, 0, 1e3, 0, 1e3),
        nx=nx,
        ny=ny,
        nz=nz,
        endianness="big",
        grade=grade,
        freq=freq,
        wl=wl,
        model=fname,
        hmin=hmin,
    )
    # Build mesh size function (in parallel)
    ef = ef.build(comm=comm)
    # Build lambda functions
    ef = ef.construct_lambdas(comm)

    mshgen = SeismicMesh.MeshGenerator(
        ef, method="qhull"
    )  # parallel currently only works in qhull

    points, cells = mshgen.build(max_iter=50, nscreen=1, seed=0, COMM=comm, axis=0,)
    # remove slivers
    points, cells = mshgen.build(
        points=points,
        max_iter=15,
        nscreen=1,
        seed=0,
        COMM=comm,
        axis=0,
        mesh_improvement=True,
    )

    if rank == 0:
        # import meshio

        # meshio.write_points_cells(
        #    "foo3D_V3.vtk", points, [("tetra", cells)],
        # )

        vol = SeismicMesh.geometry.simpvol(points / 1000, cells)
        assert np.abs(2 - np.sum(vol)) < 0.10  # km2
        # 5865 vertices and 33063 cells
        # 9220 49263
        print(len(points), len(cells))
        assert np.abs(9220 - len(points)) < 100
        assert np.abs(49263 - len(cells)) < 100


if __name__ == "__main__":
    test_3dpar_mesher()
