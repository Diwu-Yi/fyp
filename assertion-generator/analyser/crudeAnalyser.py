

if __name__ == '__main__':
    buggy = []
    correct = []
    pair = set()
    unique = set()
    file_bench = open('../util/benchmark_crude_expand.txt', 'r')
    lines = file_bench.readlines()
    i = 0
    for line in lines:
        hashes = line.strip().split(" | ")
        fixing = ''
        inducing = ''
        for some_hash in hashes:
            # fixing = ''
            # inducing = ''
            if "rfc:" in some_hash:
                sha_hash = some_hash.split(":")[1].strip()
                correct.append(sha_hash)
                unique.add(sha_hash)
                fixing = sha_hash
            elif "ric:" in some_hash:
                sha_hash = some_hash.split(":")[1].strip()
                buggy.append(sha_hash)
                unique.add(sha_hash)
                inducing = sha_hash
            pair.add((fixing, inducing))
        # print(i)
        # print(fixing)
        # print(inducing)
        i += 1
    file_bench.close()
    print(len(buggy))
    print(len(correct))
    print(len(unique))
    print(len(pair))

    # # f = open('../result/benchmark_crude.txt', 'r')
    # f_target = open('../result/benchmark_relevant_commits.txt', 'a+')
    # f_correct = open('../result/correct/benchmark_correct.txt', 'a+')
    # f_buggy = open('../result/buggy/benchmark_buggy.txt', 'a+')
    # for i in range(len(buggy)):
    #     entry = buggy[i]
    #     corresponding_fix = correct[i]
    #     buggy_found_flag = False
    #     target_line_buggy = ""
    #     correct_found_flag = False
    #     target_line_correct = ""
    #     for line in open('../result/benchmark_crude_fastjson.txt', 'r').readlines():
    #         if entry in line:
    #             #f_target.write(line)
    #             #f_buggy.write(line)
    #             buggy_found_flag = True
    #             target_line_buggy = line
    #         elif corresponding_fix in line:
    #             #f_target.write(line)
    #             #f_correct.write(line)
    #             correct_found_flag = True
    #             target_line_correct = line
    #         else:
    #             continue
    #         # else:
    #         #     line = line.strip().replace('\n', ' ')
    #         #     curr_string += line
    #     # if not buggy_found_flag:
    #     #     print(i)
    #     #     print("this buggy commit is not found: ")
    #     #     print(entry)
    #     # if not correct_found_flag:
    #     #     print(i)
    #     #     print("this correct commit is not found: ")
    #     #     print(corresponding_fix)
    #     if buggy_found_flag and correct_found_flag:
    #         f_buggy.write(target_line_buggy)
    #         f_correct.write(target_line_correct)
    # f_target.close()
    # f_buggy.close()
    # f_correct.close()
    # f.close()

    # # once off process script, fill in sha for each line
    # f_correct = open('../result/correct/benchmark_correct.txt', 'r')
    # f_correct_temp = open('../result/correct/tempFile.txt', 'a+')
    # f_buggy = open('../result/buggy/benchmark_buggy.txt', 'r')
    # f_buggy_temp = open('../result/buggy/tempFile.txt', 'a+')
    # i = 0
    # for line in f_correct.readlines():
    #     while i < 47:
    #         i += 1
    #         continue
    #     info = line.strip().split(",")
    #     for j in range(len(info)):
    #         entry = info[j]
    #         print(entry)
    #         if "https://github.com/alibaba/fastjson/commit/" in entry:
    #             commit_sha = entry.split("commit/")[1].strip()
    #             if commit_sha in info[1]:
    #                 continue
    #             info.insert(1, commit_sha)
    #     f_correct_temp.write(', '.join(info) + '\n')
    #
    # for line in f_buggy.readlines():
    #     while i < 47:
    #         i += 1
    #         continue
    #     info = line.strip().split(",")
    #     for j in range(len(info)):
    #         entry = info[j]
    #         if "https://github.com/alibaba/fastjson/commit/" in entry:
    #             commit_sha = entry.split("commit/")[1].strip()
    #             if commit_sha in info[1]:
    #                 continue
    #             info.insert(1, commit_sha)
    #     f_buggy_temp.write(', '.join(info) + '\n')
    # f_buggy.close()
    # f_correct.close()
    # f_buggy_temp.close()
    # f_correct_temp.close()

    f_size_buggy = open('../result/buggy/buggy_corresponding_size.txt', 'a+')
    f_size_correct = open('../result/correct/correct_corresponding_size.txt', 'a+')
    for j in range(len(buggy)):
        entry = buggy[j]
        fixing = correct[j]
        is_buggy_found = False
        is_fixing_found = False
        line_buggy = ""
        line_fixing = ""
        for line in open('../result/benchmark_crude_fastjson_size_crude.txt', 'r').readlines():
            if entry in line:
                # f_size_buggy.write(line)
                is_buggy_found = True
                line_buggy = line
            elif fixing in line:
                #f_size_correct.write(line)
                is_fixing_found = True
                line_fixing = line
        if is_fixing_found and is_buggy_found:
            f_size_buggy.write(line_buggy)
            f_size_correct.write(line_fixing)
