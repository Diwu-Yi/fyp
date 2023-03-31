import sys
#print(sys.path)
import os
#print(os.getcwd())
import pathlib
path = pathlib.Path.cwd()
sys.path.append("..")
print(path.parent.absolute())
from BaseRequester import BaseRequester
from Parser.Parser import Parser
from util.util import Util
from threadpool.ThreadPool import ThreadPool
from Entity.RepoEntity import RepoEntity
from Requester.UserRequester import UserRequester
import requests
import json
import os
import parsel
import time
from lxml import etree
util = Util()
thread = ThreadPool(util.get_thread_num())
repo_entity = RepoEntity()
user_requester = UserRequester()


class ReposRequester(BaseRequester):
    def __init__(self):
        BaseRequester.__init__(self)
        self.result_path = os.path.dirname(os.getcwd()) + os.sep + "result" + os.sep

    # 获取README
    '''
    def get_readme(self, username: str, repo_name: str):
        url = f"https://raw.githubusercontent.com/{username}/{repo_name}/master/README.md"
        response_text = requests.get(url, headers=self._random_header()).text
        path = self.result_path + username + os.sep + repo_name + os.sep
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + "README.md", "w", encoding="utf-8") as f:
            f.write(response_text)
         f.close()
    

    def get_repo_detail(self, username: str, repo_name: str):
        url = f"https://api.github.com/repos/{username}/{repo_name}/"
        self._test()
        json_result = requests.get(url, headers=self._random_header()).json()
        repos_dict = Parser.parser_repos(json_result)
        return repos_dict
    '''

    def __get_commit_num(self, username: str, repo_name: str):
        url = f"https://github.com/{username}/{repo_name}/"
        response_text = requests.get(url, headers=self._random_header()).text
        commit_num_str = parsel.Selector(response_text).xpath("//a/span['d-none d-sm-inline']/strong/text()").get()
        if commit_num_str == None:
            # 此时库为空库
            commit_num = 0
        else:
            commit_num = int(commit_num_str.replace(",", ""))
        return commit_num


    def get_repo_commit(self, username: str, repo_name: str, is_save=True):
        # 如果break_count大于20，证明一个问题的获取以超出了20秒，那么此时放弃这个问题用户的获取
        break_count = 0
        count_list = []
        commit_num = self.__get_commit_num(username, repo_name)
        print(commit_num)
        if commit_num == 0:
            page = 0
        elif commit_num < 100:
            page = 1
        else:
            page = commit_num // 100 + 1
        # 用来存放所有的commit的相关信息，其中包括每次commit的sha，changed files，additions，deletions
        commit_list = []
        # 用来存放一个库所欲commit数据变化的总值，但无法精确到每次commit的sha
        repo_commit_dict = {}
        # save the commits sha hashes of interest into 2 sets, one for buggy aka ric, the other for correct aka rfc
        # buggy = set()
        # correct = set()
        # file_bench = open('../util/benchmark_crude.txt', 'r')
        # lines = file_bench.readlines()
        # for line in lines:
        #     hashes = line.strip().split("|")
        #     for some_hash in hashes:
        #         if "rfc" in some_hash:
        #             correct.add(some_hash)
        #         elif "ric" in some_hash:
        #             buggy.add(some_hash)
        #         else:
        #             continue

        for i in range(page):
            url = f"https://api.github.com/repos/{username}/{repo_name}/commits?page={i}&per_page=100"
            self._test()
            print(url)
            json_result = requests.get(url, headers=self._random_header()).json()
            print(json_result)
            commit_sha_list = Parser.parser_commit(json_result, is_json=True)
            #print(commit_sha_list)
            for j in range(len(commit_sha_list)):
                #if commit_sha_list[j] in correct or commit_sha_list[j] in buggy:
                    #if commit_sha_list[j] in correct:
                        #is_correct = True
                    #else:
                        #is_correct = False
                thread.run(func=self.__get_single_commit,
                               args=(username, repo_name, commit_sha_list[j], commit_list, count_list),
                               callback=self.callback)
                #else:
                    #print("ignoring irrelevant commits")
                    #continue

            while True:
                util.process_bar(percent=len(commit_list) / commit_num,
                                 start_str=f"对库{username}/{repo_name}的commit的爬取进度：", end_str="100%",
                                 total_length=50)
                if len(commit_list) < commit_num:
                    if len(count_list) == len(commit_sha_list):
                        count_list = []
                        break
                    else:
                        # time.sleep(1)
                        last_count = len(commit_list)
                        time.sleep(1)
                        if last_count == len(commit_list):
                            break_count += 1
                        else:
                            break_count = 0
                        if break_count >= 60 and self._get_limit_count() < 4999:
                            print("\n该repo的commit的获取时间卡了超过60秒，已放弃该repo")
                            break
                else:
                    break
        if len(commit_list) == 0:
            return None
        for i in commit_list:
            if i is None or i == {}:
                pass
            else:
                if not repo_commit_dict.__contains__("total"):
                    repo_commit_dict["total"] = i["total"]
                repo_commit_dict["total"] += i["total"]
                if not repo_commit_dict.__contains__("additions"):
                    repo_commit_dict["additions"] = i["total"]
                repo_commit_dict["additions"] += i["additions"]
                if not repo_commit_dict.__contains__("deletions"):
                    repo_commit_dict["deletions"] = i["total"]
                repo_commit_dict["deletions"] += i["deletions"]
        repo_commit_dict["commit_num"] = commit_num
        repo_commit_dict["repo_name"] = username + "/" + repo_name
        thread.close()
        if is_save:
            repo_entity.add_repo((repo_commit_dict, commit_list))
        return repo_commit_dict, commit_list

    def __get_single_commit(self, username, repo_name, commit_sha: str, commit_list: list, count_list: list):
        try:
            commit_dict = {}
            commit_url = f"https://github.com/{username}/{repo_name}/commit/{commit_sha}"
            api_commit_url = f"https://api.github.com/repos/{username}/{repo_name}/commits/{commit_sha}"
            print(commit_url)
            simple_headers = {
                'Accept': 'application/vnd.github+json',
                'Authorization': 'Bearer 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',
                'Content-Type': 'application/json'}
            #
            commit_response = requests.get(api_commit_url, headers=simple_headers)
            commit_json = commit_response.json()
            # print("is here")
            # print(commit_json)
            # print(commit_json["commit"]["author"]["name"] + "there is the author name")
            issue_id = "#3976"
            issue_name = commit_json["commit"]["author"]["name"]
            # print(issue_name + " there is the read name")
            issue_description = commit_json["commit"]["message"]
            issue_description = issue_description.replace('\n', ' ')
            # print(issue_description + " here is the description")
            issue_size = commit_json["stats"]["total"]
            commit_sha = commit_json["sha"]
            # f = open('../result/benchmark_crude.txt', 'a+')
            # print("file opened")
            # f.write(f'{issue_id},{issue_sha}, {issue_name},{issue_description}, {commit_url},{repo_name}\n')
            # print("file written")
            response = requests.get(commit_url, headers=simple_headers)
            # print(response.json())
            # print(response.text)
            # change_num_list = Parser.parser_commit(response_text)
            # commit_dict["sha"] = commit_sha
            # 这里的total指的是修改的文件的数量，因为总代吗修改行数本身是没有的，
            # 如果想要硬算的话，其实就是把additions和deletions做了个减法，感觉没必要，还不如总修改文件数量
            # commit_dict["total"] = change_num_list[0]
            # commit_dict["additions"] = change_num_list[1]
            # commit_dict["deletions"] = change_num_list[2]

            # issue_id issue_name url
            tree = etree.HTML(response.text)
            issue_url = tree.xpath('//*[@id="repo-content-pjax-container"]/div/div[2]/div[1]/a/@href')[0]
            print(issue_url)
            if issue_url:
                commit_dict = None
                string_list = [str(s) for s in issue_url]
                print("".join(string_list))
                # print(type("".join(string_list)))
                string_issue_url = "".join(string_list)
                # print("issues" in string_issue_url)
                if "issues" in string_issue_url:
                    # crawl the relevant jira issue
                    # issue_url = string_issue_url.replace("browse", "rest/api/2/issue")
                    # differentiated_headers = {
                    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                    #                   'Chrome/51.0.2704.63 Safari/537.36',
                    #     'Authorization': 'Bearer ' + 'ODgzNDg2Njk4MDE5OhGX12X+jiCgBmtSJVoYJVhCQrmB',
                    #     'Content-Type': 'application/json'}
                    # issue_response = requests.get(issue_url, headers=differentiated_headers)
                    # issue_json = issue_response.json()
                    # issue_id = issue_json["id"]
                    # issue_name = issue_json["fields"]["summary"]
                    # issue_description = issue_json["fields"]["description"]
                    differentiated_headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/51.0.2704.63 Safari/537.36'}
                    issue_response = requests.get(issue_url, headers=differentiated_headers)
                    issue_tree = etree.HTML(issue_response.text)
                    issue_name = issue_tree.xpath('//*[@id="partial-discussion-header"]/div[1]/div/h1/span[1]/text()')[0]
                    issue_id = tree.xpath('//*[@id="repo-content-pjax-container"]/div/div[2]/div[1]/a/text()')[0]
                    issue_description = "issue_description place holder, not applicable for this type of issue"
                else:
                    differentiated_headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/51.0.2704.63 Safari/537.36'}
                    issue_response = requests.get(issue_url, headers=differentiated_headers)
                    issue_tree = etree.HTML(issue_response.text)
                    issue_name = issue_tree.xpath('//*[@id="partial-discussion-header"]/div[1]/div/h1/span[1]/text()')[0]
                    issue_id = tree.xpath('//*[@id="repo-content-pjax-container"]/div/div[2]/div[1]/a/text()')[0]
                    issue_description = "issue_description place holder, not applicable for this type of issue"
                    '''
                    if 'issue' in issue_url:
                        with open('../result/ApacheResult.txt', 'a+') as f:
                            f.write(f'{issue_id}, {issue_name}, {issue_url}, {commit_url},{repo_name}\n')
                    '''
            # else:
            # issue_id = "#1710"
            # issue_name = commit_json["commit"]["author"]["name"]
            # issue_description = commit_json["message"]
            # print(issue_description + " here is the description")
            # issue_url = commit_json["sha"]
            f = open('../result/benchmark_pr_issue_fastjson_crude.txt', 'a+')
            #print("file opened")
            f.write(f'{issue_id}, {issue_name}, {issue_description}, {issue_url},{commit_url}, {repo_name}\n')
            print("file written")

        except Exception as e:
            commit_dict = None
        commit_list.append(commit_dict)
        count_list.append(commit_dict)

    def callback(self, status, result):
        # print(status)
        # print(result)
        pass

    def get_repos(self, user, is_save=True):
        # 在这里获取repo
        user_repo_list = []
        # 如果传入的user是一个字符串，此时模式会切换为根据用户名，爬取该用户所有的库
        if type(user) == str:
            user_dict = user_requester.get_single_user_info(username=user)
            if user_dict == None:
                pass
            for i in range(len(user_dict["repos"])):
                repo_name = str(user_dict["repos"][i].split("/")[-1])
                result = self.get_repo_commit(user, repo_name, is_save=is_save)
                user_repo_list.append(result)
            return user_repo_list
        # 如果传入的一个list，那么证明需要大量爬取用户库了，那么此时会将传入的list进行解析，然后批量爬取
        elif type(user) == list:
            for i in range(len(user)):
                if user[i] == None:
                    pass
                else:
                    print(user)
                    username = user[i]["login"]
                    repos = user[i]["repos"]
                    for j in range(len(repos)):
                        repo_name = str(repos[j].split("/")[-1])
                        result = self.get_repo_commit(username, repo_name, is_save=is_save)
                        user_repo_list.append(result)
            return user_repo_list
        else:
            print("请输入正确的user：1.用户名（str）\t2.用户列表(list[dict])【如没有，请使用user_requester.get_users()方法获取】")

        # def get_linked_jira(self, username, repo_name, commit_sha):


if __name__ == '__main__':
    r = ReposRequester()
    # u = UserRequester()
    # print(r.get_repos("srx-2000", is_save=True))
    # user_list = u.get_users(100)
    user_list = [{'login': 'alibaba', 'id': None, 'email': None, 'location': None, 'hireable': None, 'public_repos': 31, 'followers': 4, 'following': 1, 'repos': ['https://github.com/alibaba/fastjson']}]
    print(r.get_repos(user_list, is_save=True))
