def find_average(list:list):
    sum = 0
    for i in list:
        sum += i
    a,b,c = sum, len(list), sum / len(list)
    return a,b,c

origin_list = [3, 1, 4, 1, 5, 9, 2, 6, 5]
sum_of_elements, count_of_elements, average_value = find_average(origin_list)
print(f"Cумма всех элементов равна {sum_of_elements}, а количество элементов равно {count_of_elements}, поэтому среднее значение равно {average_value}")