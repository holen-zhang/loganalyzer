import os
import subprocess
from os.path import dirname, abspath

from CharacterizingTestLogV2 import RepoHandler
from CharacterizingTestLogV2 import FileHandler
from CharacterizingTestLogV2.GumTreeApi import Gumtree


def write_temp_file(a_temp_file, b_temp_file, head_file_content, next_file_content):
    with open(a_temp_file, "w") as f:
        f.write(head_file_content)
    with open(b_temp_file, "w") as f:
        f.write(next_file_content)


def generate_temp_file_content_modify(repo, head_commit_sha, next_commit_sha, b_path, a_path, a_temp_file, b_temp_file):
    head_file_content = repo.git.show('{}:{}'.format(head_commit_sha, b_path))
    next_file_content = repo.git.show('{}:{}'.format(next_commit_sha, a_path))
    write_temp_file(a_temp_file, b_temp_file, next_file_content, head_file_content)


def generate_temp_file_content_add(repo, head_commit_sha, b_path, a_temp_file, b_temp_file):
    head_file_content = repo.git.show('{}:{}'.format(head_commit_sha, b_path))
    next_file_content = ""
    write_temp_file(a_temp_file, b_temp_file, next_file_content, head_file_content)


def generate_temp_file_content_delete(repo, head_commit_sha, a_path, a_temp_file, b_temp_file):
    head_file_content = ""
    next_file_content = repo.git.show('{}:{}'.format(head_commit_sha, a_path))
    write_temp_file(a_temp_file, b_temp_file, head_file_content, next_file_content)


def generate_test_or_production_diff_json(path, commit_sha, test_file_index_per_commit,
                                          production_file_index_per_commit, abs_path):
    gumtree = Gumtree()
    temp_diff_list = gumtree.get_gumtree_json_diff_actions()
    if FileHandler.is_test_file(path):
        data_file_path = abs_path + "/JsonData/Test/" + str(commit_sha) + "_" + str(test_file_index_per_commit) + ".txt"
        with open(data_file_path, 'w+') as f:
            f.write(str(temp_diff_list))
        test_file_index_per_commit += 1
    else:
        data_file_path = abs_path + "/JsonData/Production/" + str(commit_sha) + "_" + \
                         str(production_file_index_per_commit) + ".txt"
        # print(data_file_path)
        with open(data_file_path, 'w+') as f:
            f.write(str(temp_diff_list))
        production_file_index_per_commit += 1

    return test_file_index_per_commit, production_file_index_per_commit


def fetch_commit_diff_json(a_temp_file, b_temp_file, stop_commit_sha, repo_path):
    repo = RepoHandler.get_project_repository(repo_path)
    head_commit = repo.head.commit
    abs_path = dirname(dirname(abspath(__file__)))
    # print(abs_path)
    while head_commit.parents[0].hexsha != stop_commit_sha:
        parent_commit = head_commit.parents[0]
        commit_diff = RepoHandler.get_single_commit_diff(head_commit)
        head_commit_sha, parent_commit_sha = RepoHandler.get_commit_sha_pair(head_commit)
        test_file_index_per_commit = 1
        production_file_index_per_commit = 1
        print(head_commit_sha)
        for file_diff in commit_diff:
            if file_diff.change_type == 'A':
                if FileHandler.is_java_file(file_diff.b_blob.path):
                    generate_temp_file_content_add(repo, head_commit_sha, file_diff.b_blob.path,
                                                   a_temp_file, b_temp_file)
                    test_file_index_per_commit, production_file_index_per_commit = \
                        generate_test_or_production_diff_json(file_diff.b_blob.path, head_commit_sha,
                                                              test_file_index_per_commit,
                                                              production_file_index_per_commit, abs_path)
            elif file_diff.change_type == 'D':
                if FileHandler.is_java_file(file_diff.a_blob.path):
                    generate_temp_file_content_delete(repo, parent_commit_sha, file_diff.a_blob.path,
                                                      a_temp_file, b_temp_file)
                    test_file_index_per_commit, production_file_index_per_commit = \
                        generate_test_or_production_diff_json(file_diff.a_blob.path, head_commit_sha,
                                                              test_file_index_per_commit,
                                                              production_file_index_per_commit, abs_path)
            elif file_diff.change_type == 'M':
                if FileHandler.is_java_file(file_diff.a_blob.path):
                    generate_temp_file_content_modify(repo, head_commit_sha, parent_commit_sha, file_diff.b_blob.path,
                                                      file_diff.a_blob.path, a_temp_file, b_temp_file)
                    test_file_index_per_commit, production_file_index_per_commit = \
                        generate_test_or_production_diff_json(file_diff.a_blob.path, head_commit_sha,
                                                              test_file_index_per_commit,
                                                              production_file_index_per_commit, abs_path)
                    # os.system('gumtree jsondiff' + " " + a_temp_file + " " + b_temp_file + " " + "> tmp.json")
                    # command = "gumtree jsondiff" + " " + a_temp_file + " " + b_temp_file
                    # temp_con = BashHandler.run(command)
                    # print(temp_con)
                    # print("Modify File: ")
                    # print(file_diff.a_blob.path)
                    # print(file_diff.b_blob.path + "\n")
        head_commit = parent_commit


def get_subprocess_output(index, a_file, b_file):
    with open("diff_" + str(index) + ".json", "w") as f:
        subprocess.call(['gumtree', 'jsondiff', a_file, b_file], stdout=f)
    return


def main():
    path = '/Users/sense/Degree/VCS/hadoop'
    stop_commit = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'
    a_file = "../TempFile/a_temp.java"
    b_file = "../TempFile/b_temp.java"
    fetch_commit_diff_json(a_file, b_file, stop_commit, path)
    # repo = get_project_repository(path)
    # get_all_commits_diff(a_file, b_file, repo)


if __name__ == "__main__":
    main()
