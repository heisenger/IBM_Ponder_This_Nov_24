import numpy as np
from multiprocessing import Pool


# Volume formula given sides
def volume(s_01, s_02, s_12, s_03, s_13, s_23):
    squared_vol = (
        (2 * s_01 * s_02 * s_03) ** 2
        + (s_01**2 + s_02**2 - s_12**2)
        * (s_01**2 + s_03**2 - s_13**2)
        * (s_02**2 + s_03**2 - s_23**2)
        - (s_01**2) * (s_02**2 + s_03**2 - s_23**2) ** 2
        - (s_02**2) * (s_01**2 + s_03**2 - s_13**2) ** 2
        - (s_03**2) * (s_01**2 + s_02**2 - s_12**2) ** 2
    )
    return squared_vol


# Function to process a single s_01 value
def process_s_01(s_01):
    results = []
    for s_02 in range(1, s_01 + 1):
        for s_12 in range(1, s_02 + 1):
            if s_12 + s_02 > s_01:  # Triangle inequality for the base triangle
                base_area_squared = (
                    (s_01 + s_02 + s_12)
                    * (-s_01 + s_02 + s_12)
                    * (s_01 - s_02 + s_12)
                    * (s_01 + s_02 - s_12)
                    / 16
                )
                min_height = max(0, int(np.sqrt(8 / base_area_squared)) - 1)
                for s_03 in range(min_height, s_02 + 1):  # Vertex 3 is the apex
                    for s_13 in range(min_height, s_02 + 1):
                        if s_01 + s_03 > s_13:
                            for s_23 in range(min_height, s_02 + 1):
                                if (s_02 + s_03 > s_23) and (s_12 + s_13 > s_23):
                                    vol = volume(s_01, s_02, s_12, s_03, s_13, s_23)
                                    if vol == 128:
                                        results.append(
                                            (s_01, s_02, s_12, s_03, s_13, s_23, vol)
                                        )
                                        print(s_01, s_02, s_12, s_03, s_13, s_23, vol)
                                    elif vol > 128:
                                        break
                                else:
                                    break
                        else:
                            break
            else:
                break
    return results


# Main execution
if __name__ == "__main__":
    from tqdm import tqdm

    # Define range of s_01 values
    s_01_values = range(1, 100)

    # Create a pool of workers
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
