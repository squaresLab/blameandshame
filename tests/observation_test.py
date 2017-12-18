import unittest
from typing import List, Dict
from blameandshame.observation import Observation
from blameandshame.base import Line


class ObservationTestCase(unittest.TestCase):
    @staticmethod
    def __build_simple(repo_url: str, fix_sha: str) -> Observation:
        bug_sha = "{}~1".format(fix_sha)
        return Observation.build(repo_url, bug_sha, fix_sha)

    def test_modified_files(self):
        def test_one(repo_url: str, fix_sha: str, expected: List[str]) -> None:
            obs = ObservationTestCase.__build_simple(repo_url, fix_sha)
            self.assertEqual(obs.modified_files, frozenset(expected))

        test_one("https://github.com/php/php-src", "fe4c789",
                 ["main/php_variables.c"])
        # should not include added file: 'ext/gmp/tests/gmp_kronecker.phpt'
        test_one("https://github.com/php/php-src", "fc80114",
                 ["ext/gmp/php_gmp.h",
                  "ext/gmp/gmp.c",
                  "UPGRADING",
                  "NEWS"])
        # merge
        test_one("https://github.com/php/php-src", "16eb387", [])

        # deletes files
        test_one("https://github.com/php/php-src", "2783b1c", [])

        # adds one file
        test_one('https://github.com/ruby/ruby', 'ec2f913', [])

    def test_modified_lines(self):
        def test_one(repo_url: str, fix_sha: str, expected: Dict[str, List[int]]) -> None:
            obs = ObservationTestCase.__build_simple(repo_url, fix_sha)

            lines = []
            for (filename, lines_in_file) in expected.items():
                lines += [Line(filename, line) for line in lines_in_file]
            lines = frozenset(lines)

            self.assertEqual(obs.modified_lines, frozenset(lines))

        test_one('https://github.com/squaresLab/blameandshame-test-repo', 'a351329',
                 {'testfile.c': [8, 25]})
