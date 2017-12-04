import git
import os
import urllib.parse


class Project(object):


    # Path to the directory used to hold downloaded Git repositories.
    REPOS_DIR = os.path.join(os.getcwd(), '.repos')


    @staticmethod
    def _url_to_path(url: str) -> str:
        """
        Computes the intended path to the local copy of a given project,
        specified by the URL of its repository.
        """
        # get the name of the repo
        path = urllib.parse.urlparse(url).path
        path, ext = os.path.splitext(path)
        _, name = os.path.split(path)

        return os.path.join(Project.REPOS_DIR, name)


    @staticmethod
    def from_url(url: str) -> 'Project':
        """
        Retrieves a project by the URL of its Git repository.

        Internally, this function uses GitPython to clone the entire history for
        Git repositories to disk. Each repository is cloned to its own
        subdirectory within `${PWD}/.repos`.

        Warning: This can potentially consume quite a bit of disk space.
        """
        # Determine the (intended) location of the given repo on disk
        path = Project._url_to_path(url)

        # Don't clone the repo if it already exists.
        if not os.path.exists(path):
            try:
                # ensure that the `${PWD}/.repos` directory exists
                if not os.path.exists(REPOS_DIR):
                    os.mkdir(REPOS_DIR)

                repo = git.Repo.clone_from(repo_url, path)
                return Project(repo)

            # ensure that we don't end up with corrupted clones
            except:
                shutil.rmtree(path, ignore_errors=True)
                raise

        return Project.from_disk(path)


    @staticmethod
    def from_disk(path: str) -> 'Project':
        """
        Retrieves a project whose repository is stored at a given local path.
        """
        return Project(git.Repo(path))


    def __init__(self, repo: git.Repo):
        self.__repo = repo
