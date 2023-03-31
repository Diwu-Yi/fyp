

if __name__ == '__main__':
    buggy = []
    correct = []
    pair = set()
    unique = set()
    file_bench_buggy = open('../result/buggy/tempFile.txt', 'r')
    file_bench_correct = open('../result/correct/tempFile.txt', 'r')
    lines = file_bench_buggy.readlines()
    for line in lines:
        hashes = line.strip().split(",")
        buggy.append(hashes[3])
    lines2 = file_bench_correct.readlines()
    for line in lines:
        hashes = line.strip().split(",")
        correct.append(hashes[3])
    file_bench_buggy.close()
    file_bench_correct.close()

    for i in range(len(buggy)):
        print(i)
        entry = buggy[i]
        corresponding_fix = correct[i]
        print(entry)
        print(corresponding_fix)
        f_buggy = open('../result/buggy/buggy_relevant_pr_issue.txt', 'a+')
        flag_is_buggy_found = False
        f_correct = open('../result/correct/correct_relevant_pr_issue.txt', 'a+')
        for line in open('../result/benchmark_pr_issue_crude.txt', 'r').readlines():
            if entry.strip() in line:
                f_buggy.write(line)
                flag_is_buggy_found = True
        if not flag_is_buggy_found:
            f_buggy.write("\n")
            # else:
            #     f_buggy.write('\n')
        flag_is_fixing_found = False
        for line in open('../result/benchmark_pr_issue_crude.txt', 'r').readlines():
            if corresponding_fix.strip() in line:
                f_correct.write(line)
                flag_is_fixing_found = True
        if not flag_is_fixing_found:
            f_correct.write("\n")
        #     else:
        #         f_correct.write('\n')

        f_buggy.close()
        f_correct.close()
