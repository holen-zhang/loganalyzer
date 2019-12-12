import git


def get_project_repository(project_path: str):
    repository = git.Repo(project_path)
    assert not repository.bare
    return repository


def get_single_commit_diff(head_commit):
    parent_commit = head_commit.parents[0]
    diff = parent_commit.diff(head_commit)
    return diff


def get_commit_sha_pair(head_commit):
    next_commit = head_commit.parents[0]
    head_commit_sha = head_commit.hexsha
    next_commit_sha = next_commit.hexsha
    return head_commit_sha, next_commit_sha
