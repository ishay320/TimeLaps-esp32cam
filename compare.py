from timeit import timeit

if __name__ == "__main__":
    input_folder = ".\\\\test\\\\"
    output_folder = "."
    times = 5
    regular_combinepics = timeit(
        stmt=f'main("{input_folder}", "{output_folder}")',
        setup="from combinepics_reguler import main",
        number=times,
    )
    pool_combinepics = timeit(
        stmt=f'main("{input_folder}", "{output_folder}")',
        setup="from combinepics import main",
        number=times,
    )

    regular_light_trace = timeit(
        stmt=f'main("{input_folder}", "{output_folder}", False)',
        setup="from light_trace_reguler import main",
        number=times,
    )
    pool_light_trace = timeit(
        stmt=f'main("{input_folder}", "{output_folder}", False)',
        setup="from light_trace import main",
        number=times,
    )

    print()
    print("*******results**********")
    print(f"regular combinepics: \t{regular_combinepics:.4f}")
    print(f"pool combinepics: \t{pool_combinepics:.4f} (multiprocessing.Pool)")
    print(f"faster percents: \t{regular_combinepics / pool_combinepics * 100:.4f}%")
    print("***********************")
    print(f"regular light trace: \t{regular_light_trace:.4f}")
    print(f"pool light trace: \t{pool_light_trace:.4f} (concurrent.futures)")
    print(f"faster percents: \t{regular_light_trace / pool_light_trace * 100:.4f}%")
    print("***********************")

'''
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
'''