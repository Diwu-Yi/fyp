

if __name__ == '__main__':
    # testing of some heuristics
    # 1. crude calculation of fix appearance in commit message
    # Heuristic 1: key word with dictionary {fix} in commit msg
    count_fix_in_buggy = 0
    count_fix_in_correct = 0

    f_buggy = open('../result/buggy/benchmark_buggy.txt', 'r')
    f_correct = open('../result/correct/benchmark_correct.txt', 'r')
    for line in f_buggy.readlines():
        if "fix" in line.lower():
            count_fix_in_buggy += 1
    for line in f_correct.readlines():
        if "fix" in line.lower():
            count_fix_in_correct += 1

    print(count_fix_in_buggy/151)
    print(count_fix_in_correct/151)

    # 2. calculation of avg commit size
    # Heuristic 2: commit size of the version: larger indicates higher chance of error
    count_size_buggy = 0
    count_size_fix = 0

    f_size_buggy = open('../result/buggy/buggy_corresponding_size.txt', 'r')
    f_size_correct = open('../result/correct/correct_corresponding_size.txt', 'r')
    arr_size_buggy = []
    arr_size_correct = []
    for line in f_size_buggy.readlines():
        num = line.strip().split(",")[2]
        count_size_buggy += int(num)
        arr_size_buggy.append(int(num))
    for line in f_size_correct.readlines():
        num = line.strip().split(",")[2]
        count_size_fix += int(num)
        arr_size_correct.append(int(num))
    print("avg size of buggy commit is: " + str(count_size_buggy/46))
    print("avg size of fixing commit is: " + str(count_size_fix / 46))
    import statistics
    print("median size of buggy is: " + str(statistics.median(arr_size_buggy)))
    print("median size of correct is: " + str(statistics.median(arr_size_correct)))
    print("max of buggy commit is: " + str(max(arr_size_buggy)))
    print("max of correct commit is " + str(max(arr_size_correct)))
    print("min of buggy commit is: " + str(min(arr_size_buggy)))
    print("min of correct commit is: " + str(min(arr_size_correct)))
    import matplotlib.pyplot as plt

    plt.plot(arr_size_correct, c="blue")
    plt.plot(arr_size_buggy, c="red")
    plt.show()

    # 3. authorship of commits
    # Heuristic 3: authorship of the version: same author indicates higher chance of fixing
    base_line = 0.0
    f_base_bench = open('../result/benchmark_crude_fastjson.txt', 'r')
    book = {}
    for line in f_base_bench.readlines():
        author = line.split(",")[1].strip()
        if author in book:
            book[author] += 1
        else:
            book[author] = 1
    for entry in book.keys():
        val = book[entry]
        prob = (val/4000) * (1 - (val/4000))
        base_line += prob
    observed = 0.0
    f_observed_buggy = open('../result/buggy/buggy_corresponding_size.txt', 'r')
    f_observed_correct = open('../result/correct/correct_corresponding_size.txt', 'r')
    line1 = f_observed_buggy.readlines()
    line2 = f_observed_correct.readlines()
    counter_author_same = 0
    for i in range(len(line1)):
        bug = line1[i]
        corr = line2[i]
        au1 = bug.split(",")[1].strip()
        au2 = corr.split(",")[1].strip()
        if au1 in au2:
            counter_author_same += 1
    f_base_bench.close()
    f_observed_correct.close()
    f_observed_buggy.close()
    print(" the average chance is: " + str(base_line))
    print(" the observed chance is: " + str((counter_author_same / 151)))
    # 4. frequent edition of the modified files in repo history
    # Heuristics 4: frequency of edition of the file in history, between the two versions identified

    # Heuristics 5: exceptions and crashes encountered during testcase execution
    f_execution_buggy = open('../result/buggy/buggy_corresponding_size.txt', 'r')
    f_execution_correct = open('../result/correct/correct_corresponding_size.txt', 'r')
    line1 = f_execution_buggy.readlines()
    line2 = f_execution_correct.readlines()
    import csv
    dynamic_output = open('../result/Regs4j.csv', 'r')
    csv_reader = csv.DictReader(dynamic_output)
    score = 0
    for i in range(len(line1)):
        bug = line1[i]
        corr = line2[i]
        bugId = bug.split(",")[5].strip()
        for row in csv_reader:
            if bugId in row:
                print("hit")
                score = 1
    # offer intuition and statistics historical
    # dynamic features : runtime: an exception happens when a test case is executed,
    # junit test coverage





