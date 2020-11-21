import stats.time_slice

def main():
    collector = stats.time_slice.TimeSlice()
    while True:
        collector.collect_time_slices()

if __name__ == "__main__":
    main()

