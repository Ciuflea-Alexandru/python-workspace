volume = {0: 10, 1: 7, 2: 6, 3: 7, 4: 8, 5: 9, 6: 15,
          7: 6, 8: 8, 9: 4, 10: 5, 11: 14, 12: 20, 13: 25}


def analyze_volume(data):
    total_count = 0
    total_value = 0
    signal = True

    # We calculate the count of values and their total
    for key, value in data.items():
        total_value += value
        total_count += 1

    if total_count == 0:
        return 'Not enough data'

    # Find the median and the acceptance limit
    med = total_value / total_count
    break_point = med * 2

    # Get the last three numbers
    big_three = list(data.values())[-3:]

    # Find out if the last numbers are above limit
    for value in big_three:
        if value < break_point:
            signal = False
            break

    # Print the responses
    print(f'Median: {med}')
    print(f'Break point: {break_point}')
    print(f'Big three: {big_three}')

    if signal:
        return 'GREEN SIGNAL'
    else:
        return 'RED SIGNAL'


result = analyze_volume(volume)
print(result)
