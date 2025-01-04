import numpy as np
from multiprocessing import Pool

from scipy.optimize import fsolve
import numpy as np


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


def find_s23(s_01, s_02, s_12, s_03, s_13, target_volume):
    def func(s_23):
        # volume_sq = volume(s_01, s_02, s_12, s_03, s_13, s_23)
        volume_sq = (
            (2 * s_01 * s_02 * s_03) ** 2
            + (s_01**2 + s_02**2 - s_12**2)
            * (s_01**2 + s_03**2 - s_13**2)
            * (s_02**2 + s_03**2 - s_23**2)
            - (s_01**2) * (s_02**2 + s_03**2 - s_23**2) ** 2
            - (s_02**2) * (s_01**2 + s_03**2 - s_13**2) ** 2
            - (s_03**2) * (s_01**2 + s_02**2 - s_12**2) ** 2
        )
        # print(type(volume_sq))
        return volume_sq - target_volume

    # Initial guess for s_23 (can be adjusted based on the problem)
    initial_guess = np.mean([s_01, s_02, s_12, s_03, s_13])

    # Find the root using fsolve
    s_23_solution = fsolve(func, initial_guess)
    return s_23_solution[0]


def process_s_01(s_01):
    results = []
    print(f"Processing s_01 = {s_01}")
    for s_02 in range(s_01 // 2, s_01 + 1):
        for s_12 in range(max(s_01 - s_02, 1), s_02 + 1):
            min_height = 1
            for s_03 in range(min_height, s_02 + 1):  # Vertex 3 is the apex
                for s_13 in range(max(min_height, s_01 - s_03 + 1), s_02 + 1):
                    for s_23 in range(
                        max(
                            min_height,
                            s_13 - s_12 + 1,
                            s_12 - s_13 + 1,
                            s_02 - s_03 + 1,
                        ),
                        s_01 + 1,
                    ):

                        vol = volume_cal(s_01, s_02, s_12, s_03, s_13, s_23)
                        if vol == 128:
                            results.append((s_01, s_02, s_12, s_03, s_13, s_23, vol))
                            print(s_01, s_02, s_12, s_03, s_13, s_23, vol)
                        elif vol > 128:
                            # print(vol, s_13, s_12, s_02, s_03, s_23)
                            break
    return results


# Main execution
if __name__ == "__main__":
    from tqdm import tqdm

    # Define range of s_01 values
    s_01_values = range(1000)

    # # Create a pool of workers
    with Pool() as pool:
        # Use tqdm for progress bar
        results = list(
            tqdm(pool.imap(process_s_01, s_01_values), total=len(s_01_values))
        )

    # Flatten the results list
    all_results = [item for sublist in results for item in sublist]

    # Print the results
    for result in all_results:
        print(result)
