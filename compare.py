from timeit import timeit
import matplotlib.pyplot as plt

if __name__ == "__main__":
    folders_size = [10, 20, 100, 200, 500, 1000, 2000]
    folders = [
        "./10f/",
        "./20f/",
        "./100f/",
        "./200f/",
        "./500f/",
        "./1000f/",
        "./2000f/",
    ]
    output_folder = "./dump/"

    regular_combinepics = []
    pool_combinepics = []
    regular_light_trace = []
    pool_light_trace = []
    times = 3

    for input_folder in folders:
        regular_combinepics.append(timeit(
            stmt=f'main("{input_folder}", "{output_folder}")',
            setup="from combinepics_reguler import main",
            number=times,
        ))
        pool_combinepics.append(timeit(
            stmt=f'main("{input_folder}", "{output_folder}")',
            setup="from combinepics import main",
            number=times,
        ))

        regular_light_trace.append(timeit(
            stmt=f'main("{input_folder}", "{output_folder}", False)',
            setup="from light_trace_reguler import main",
            number=times,
        ))
        pool_light_trace.append(timeit(
            stmt=f'main("{input_folder}", "{output_folder}", False)',
            setup="from light_trace import main",
            number=times,
        ))

    color = "tab:red"
    plt.plot(folders_size, regular_combinepics, color, label="regular combinepics")
    plt.plot(folders_size, pool_combinepics, label="pool combinepics")
    plt.legend()
    plt.show()

    color = "tab:red"
    plt.plot(folders_size, regular_light_trace, color, label="regular light_trace")
    plt.plot(folders_size, pool_light_trace, label="pool light_trace")
    plt.legend()
    plt.show()

    # print()
    # print("*******results**********")
    # print(f"regular combinepics: \t{regular_combinepics:.4f}")
    # print(f"pool combinepics: \t{pool_combinepics:.4f} (multiprocessing.Pool)")
    # print(f"faster percents: \t{regular_combinepics / pool_combinepics * 100:.4f}%")
    # print("***********************")
    # print(f"regular light trace: \t{regular_light_trace:.4f}")
    # print(f"pool light trace: \t{pool_light_trace:.4f} (concurrent.futures)")
    # print(f"faster percents: \t{regular_light_trace / pool_light_trace * 100:.4f}%")
    # print("***********************")

"""
with small dataset(20 pics):
*******results**********
regular combinepics:    3.7252
pool combinepics:       4.7141 (multiprocessing.Pool)
faster percents:        79.0225%
***********************
regular light trace:    3.9107
pool light trace:       3.1036 (concurrent.futures)
faster percents:        126.0053%
***********************
"""