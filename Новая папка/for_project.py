def count_max_blocks(numbers_list):
    max_n = numbers_list[0]
    length = 0
    q_block = 0
    for num in numbers_list:
        length += 1
        max_n = max(num, max_n)
        expect_length = max_n + 1 
        if length == expect_length:
            q_block += 1 
        else:
            continue
    return q_block

if __name__ == '__main__':
    quantity_nums = int(input())
    numbers_list = list(map(int, input().split()))
    print (count_max_blocks(numbers_list))
