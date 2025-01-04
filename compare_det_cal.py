import numpy as np
import time
from scipy.linalg import det as scipy_det
from sympy import Matrix
import matplotlib.pyplot as plt


def volume_cal(s_01, s_02, s_12, s_03, s_13, s_23):
    s_01_squared = s_01**2
    s_02_squared = s_02**2
    s_12_squared = s_12**2
    s_03_squared = s_03**2
    s_13_squared = s_13**2
    s_23_squared = s_23**2

    squared_vol = (
        4 * s_01_squared * s_02_squared * s_03_squared
        + (s_01_squared + s_02_squared - s_12_squared)
        * (s_01_squared + s_03_squared - s_13_squared)
        * (s_02_squared + s_03_squared - s_23_squared)
        - s_01_squared * ((s_02_squared + s_03_squared - s_23_squared) ** 2)
        - s_02_squared * ((s_01_squared + s_03_squared - s_13_squared) ** 2)
        - s_03_squared * ((s_01_squared + s_02_squared - s_12_squared) ** 2)
    )

    return squared_vol


def cayley_menger_matrix(s_01, s_02, s_12, s_03, s_13, s_23):
    matrix = np.array(
        [
            [0, 1, 1, 1, 1],
            [1, 0, s_01**2, s_02**2, s_03**2],
            [1, s_01**2, 0, s_12**2, s_13**2],
            [1, s_02**2, s_12**2, 0, s_23**2],
            [1, s_03**2, s_13**2, s_23**2, 0],
        ]
    )
    return matrix


def calculate_volumes_and_determinants_and_test_speed(iterations=100):

    volumes = []
    np_dets = []
    sympy_dets = []
    volume_times = []
    np_det_times = []
    sympy_det_times = []

    for _ in range(iterations):
        s_01, s_02, s_12, s_03, s_13, s_23 = map(
            int, np.random.randint(200000, 500000, 6)
        )

        start_time = time.time()
        vol = volume_cal(s_01, s_02, s_12, s_03, s_13, s_23) * 2
        volume_times.append(time.time() - start_time)
        volumes.append(vol)

        matrix = cayley_menger_matrix(s_01, s_02, s_12, s_03, s_13, s_23)

        start_time = time.time()
        np_det = np.linalg.det(matrix)
        np_det_times.append(time.time() - start_time)
        np_dets.append(np_det)

        sympy_matrix = Matrix(matrix)
        start_time = time.time()
        sympy_det_val = sympy_matrix.det(method="bareiss")
        sympy_det_times.append(time.time() - start_time)
        sympy_dets.append(float(sympy_det_val))

    volume_avg = np.mean(volume_times)
    volume_std = np.std(volume_times)
    np_det_avg = np.mean(np_det_times)
    np_det_std = np.std(np_det_times)
    sympy_det_avg = np.mean(sympy_det_times)
    sympy_det_std = np.std(sympy_det_times)

    print(
        f"Volume Calculation - Avg Time: {volume_avg:.6f} seconds, Std Dev: {volume_std:.6f}"
    )
    print(
        f"Numpy Determinant Calculation - Avg Time: {np_det_avg:.6f} seconds, Std Dev: {np_det_std:.6f}"
    )
    print(
        f"Sympy Determinant Calculation - Avg Time: {sympy_det_avg:.6f} seconds, Std Dev: {sympy_det_std:.6f}"
    )

    plt.figure(figsize=(10, 6))
    plt.errorbar(
        ["Volume", "Numpy Det", "Sympy Det"],
        [volume_avg, np_det_avg, sympy_det_avg],
        yerr=[volume_std, np_det_std, sympy_det_std],
        fmt="o",
        capsize=5,
    )
    plt.ylabel("Time (seconds)")
    plt.title("Average Calculation Time with Standard Deviation")
    plt.show()

    return volumes, np_dets, sympy_dets


def plot_scatter(volumes, np_dets, sympy_dets):
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.scatter(volumes, np_dets, alpha=0.5, label="Numpy Determinant")
    plt.plot(
        [min(volumes), max(volumes)], [min(volumes), max(volumes)], "r--", label="y=x"
    )  # Line at y=x

    plt.xlabel("Volume Calculation")
    plt.ylabel("Numpy Determinant")
    plt.title("Volume Calculation vs Numpy Determinant")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.scatter(volumes, sympy_dets, alpha=0.5, label="Scipy Determinant")
    plt.plot(
        [min(volumes), max(volumes)], [min(volumes), max(volumes)], "r--", label="y=x"
    )  # Line at y=x

    plt.xlabel("Volume Calculation")
    plt.ylabel("Scipy Determinant")
    plt.title("Volume Calculation vs Scipy Determinant")
    plt.legend()

    plt.tight_layout()
    plt.show()


volumes, np_dets, sympy_dets = calculate_volumes_and_determinants_and_test_speed(100)
print(volumes[:10], np_dets[:10], sympy_dets[:10])
plot_scatter(volumes, np_dets, sympy_dets)


test = 524283
hex_tuple = (test, test, test, test - 1, test - 1, 2)
print(volume_cal(*hex_tuple) * 2)
matrix = cayley_menger_matrix(*hex_tuple)
print(np.linalg.det(matrix))

sympy_matrix = Matrix(matrix)
sympy_det_val = sympy_matrix.det(method="bareiss")

print(sympy_det_val)
# print(matrix)
