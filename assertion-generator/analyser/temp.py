if __name__ == '__main__':
    arr = [12, 11, 13, 5, 6]


    def insertion_sort(arr):
        for i in range(1, len(arr)):
            for j in range(i, 0, -1):
                print(arr[i])
                print(arr[j])
                if arr[i] < arr[j]:
                    arr[i], arr[j] = arr[j], arr[i]
            print(arr)
        return arr

    def quick_sort(arr, low, high):
        if low >= high:
            return arr
        pivot = arr[low]
        pos = low
        for j in range(low + 1, len(arr)):
            if arr[j] < pivot:
                arr[pos], arr[j] = arr[j], arr[pos]
                pos = j
        quick_sort(arr, 0, pos)
        quick_sort(arr, pos + 1, high)
        return arr

    print(quick_sort(arr, 0, 4))

    def bubble_sort(arr):
        for i in range(len(arr)):
            for j in range(0, len(arr) - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr


    #print(bubble_sort(arr))
