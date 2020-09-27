import github

from django.conf import settings


def get_github_instance():
    g = github.Github(settings.GITHUB_ACCESS_TOKEN)
    return g


def get_repo():
    g = get_github_instance()
    repo = g.get_repo("raphodn/know-your-planet")
    return repo


def create_branch(branch_name):
    print("in create_branch", branch_name)
    repo = get_repo()
    source = repo.get_branch("master")
    branch_ref = f"heads/{branch_name}"
    try:
        branch = repo.create_git_ref(ref=f"refs/{branch_ref}", sha=source.commit.sha)
    except github.GithubException as e:
        if e.data["message"] == "Reference already exists":
            print("branch already exists")
            branch = repo.get_git_ref(ref=branch_ref)
        else:
            raise e
    # branch already exists ? github.GithubException.GithubException: 422 {"message": "Reference already exists", "documentation_url": "https://docs.github.com/rest/reference/git#create-a-reference"} # noqa
    print(branch)
    return branch


def create_file(file_path, commit_message, file_content, branch_name):
    print("in create_file", file_path)
    repo = get_repo()
    # create_file(path, message, content, branch=NotSet, committer=NotSet, author=NotSet)
    try:
        res = repo.create_file(
            file_path, commit_message, file_content, branch=branch_name
        )
    except github.GithubException as e:
        if (
            e.data["message"] == 'Invalid request.\n\n"sha" wasn\'t supplied.'
        ):  # trying to update an existing file # noqa
            print("in create_file > update_file")
            contents = repo.get_contents(file_path, ref=branch_name)
            res = repo.update_file(
                file_path,
                commit_message,
                file_content,
                contents.sha,
                branch=branch_name,
            )
        else:
            raise e
    print(res)
    return res


def create_pull_request(
    pull_request_title, pull_request_message, branch_name, review_request=False
):
    print("in create_pull_request", pull_request_title)
    repo = get_repo()
    try:
        pull_request = repo.create_pull(
            title=pull_request_title,
            body=pull_request_message,
            base="master",
            head=branch_name,
        )
    except github.GithubException as e:
        if (
            (e.data["message"] == "Validation Failed")
            and (len(e.data["errors"]) == 1)
            and e.data["errors"][0]["message"].startswith(
                "A pull request already exists for"
            )
        ):  # for raphodn:data-update-2020-09-27-test."
            print("pull request already exists")
            open_pull_requests = repo.get_pulls(state="open")
            for open_pull_request in open_pull_requests:
                if open_pull_request.title == pull_request_title:
                    pull_request = repo.get_pull(open_pull_request.number)
        else:
            raise e
    # if review_request:
    #     pull_request.create_review_request(reviewers=["raphodn"])
    print(pull_request)
    return pull_request
