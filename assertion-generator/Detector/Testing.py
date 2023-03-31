import time
import threading
import os

# input format array, of length (n-1) , contains values of 1 to n
if __name__ == '__main__':
    def find_missing_value(arr): # Length n
        if len(arr) == 0: # O (1)
            return None
        if arr is None:
            return None

        recorder = [0 for i in range(len(arr) + 1)]  # O (n) , O (n + 1) ==> O (n)
        for j in range(len(arr)):  # O (n)
            curr_element = arr[j]  # O (1)
            recorder[curr_element - 1] = 1
        # result = -1
        for k in range(len(recorder)):  # O (n)
            if recorder[k] == 1:
                continue
            else:
                return (k + 1)

    # Overall O (n) for time complexity
    # Overall O (n) for space complexity
    # [1, 2, 3, 5]
    #print(find_missing_value([]))

    def negative_number_to_string(num):
        str_num = str(num)
        str_num = str_num[::-1]
        if str_num[-1] != "-":
            result = int(str_num)
        else:
            str_num = str_num[:len(str_num) - 1]
            result = int(str_num)
            result = result * -1
        return result

    print(negative_number_to_string(-123))
