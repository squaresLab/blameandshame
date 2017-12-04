#!/usr/bin/env python3
import os
import unittest
from blameandshame.base import  Project
from blameandshame.util import  Change, \
                                files_in_commit, \
                                lines_modified_by_commit, \
                                authors_of_file, \
                                commits_to_file, \
                                commits_to_line, \
                                last_commit_to_line


class ProjectTestCase(unittest.TestCase):
    def test_repo_path(self):
        repos_dir = os.path.join(os.getcwd(), '.repos')

        self.assertEqual(Project._url_to_path('https://github.com/uber/pyro'),
                         os.path.join(repos_dir, 'pyro'))
        self.assertEqual(Project._url_to_path('https://github.com/google/protobuf'),
                         os.path.join(repos_dir, 'protobuf'))
        self.assertEqual(Project._url_to_path('https://github.com/cilium/cilium'),
                         os.path.join(repos_dir, 'cilium'))
        self.assertEqual(Project._url_to_path('https://github.com/golang/dep'),
                         os.path.join(repos_dir, 'dep'))
        self.assertEqual(Project._url_to_path('https://github.com/opencv/opencv.git'),
                         os.path.join(repos_dir, 'opencv'))


class UtilTestCase(unittest.TestCase):
    def test_commits_to_line(self):
        def check_one(repo, filename, lineno, expected):
            expected = [repo.commit(sha) for sha in expected]
            self.assertEqual(commits_to_line(repo, filename, lineno, until=expected[0]),
                             expected)

        repo = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(repo, 'file.txt', 1, ['922e13d', '422cab3'])


    def test_commits_to_file(self):
        def check_one(repo, filename, expected):
            expected = [repo.commit(sha) for sha in expected]
            self.assertEqual(commits_to_file(repo, filename, until=expected[0]),
                             expected)

        repo = Project.from_url('https://github.com/php/php-src')
        check_one(repo, 'ext/ext_skel.php', ['216d711', 'f35f459', 'b079cc2', '941dc72'])

        repo = Project.from_url('https://github.com/google/protobuf')
        check_one(repo, 'php/composer.json', ['21b0e55', 'b9b34e9', '6b27c1f', '46ae90d'])

        # corner case: file is renamed once
        repo = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(repo, 'file-one.txt', ['474ea04', '922e13d', '422cab3'])


    def test_authors_of_file(self):
        def check_one(repo, filename, until, expected):
            until = repo.commit(until)
            actors = authors_of_file(repo, filename, until=until)
            authors = frozenset(a.name for a in actors)
            self.assertEqual(authors, frozenset(expected))

        repo = Project.from_url('https://github.com/google/protobuf')
        check_one(repo, 'php/composer.json', '21b0e55',
                  ['Paul Yang', 'michaelbausor', 'Brent Shaffer'])
        check_one(repo, 'php/composer.json', '6b27c1f',
                  ['Paul Yang'])


    def test_files_in_commit(self):
        repo = Project.from_url('https://github.com/google/protobuf')
        self.assertEqual(files_in_commit(repo, 'baed06e'),
                         frozenset(['objectivec/GPBCodedOutputStream.m']))
        self.assertEqual(files_in_commit(repo, '949596e'),
                         frozenset(['objectivec/GPBMessage.m']))
        self.assertEqual(files_in_commit(repo, 'cd5f49d', {Change.MODIFIED}),
                         frozenset(['ruby/travis-test.sh',
                                    'ruby/ext/google/protobuf_c/protobuf.c',
                                    'ruby/ext/google/protobuf_c/defs.c',
                                    'ruby/Rakefile',
                                    'Makefile.am',
                                    '.gitignore',
                                    'ruby/ext/google/protobuf_c/protobuf.h']))
        self.assertEqual(files_in_commit(repo, 'cd5f49d', {Change.ADDED}),
                         frozenset(['ruby/tests/gc_test.rb']))
        self.assertEqual(files_in_commit(repo, 'cd5f49d'),
                         frozenset(['ruby/travis-test.sh',
                                    'ruby/ext/google/protobuf_c/protobuf.c',
                                    'ruby/ext/google/protobuf_c/defs.c',
                                    'ruby/Rakefile',
                                    'Makefile.am',
                                    '.gitignore',
                                    'ruby/ext/google/protobuf_c/protobuf.h',
                                    'ruby/tests/gc_test.rb']))
        # note: `ruby/tests/gc_test.rb` is added and thus should not be
        #       considered as 'modified'.


    def test_lines_modified_by_commit(self):
        repo = Project.from_url('https://github.com/google/protobuf')
        self.assertEqual(
            lines_modified_by_commit(repo, 'baed06e'),
            (frozenset({('objectivec/GPBCodedOutputStream.m', 177)}),
             frozenset({('objectivec/GPBCodedOutputStream.m', 180)}))
        )
        # Only add
        self.assertEqual(
            lines_modified_by_commit(repo, 'ac5371d'),
            (frozenset(), frozenset({('BUILD', 27), ('BUILD', 28)}))
        )
        # Only delete
        self.assertEqual(
            lines_modified_by_commit(repo, 'd680159'),
            (frozenset({('src/google/protobuf/stubs/time.cc', 24)}),
             frozenset())
        )


    def test_last_commit_to_line(self):
        repo = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        self.assertEqual(last_commit_to_line(repo, 'file-one.txt', 1,
                                             repo.commit('9ca70f7')),
                         repo.commit('922e13d'))
        self.assertEqual(last_commit_to_line(repo, 'file-one.txt', 5,
                                             repo.commit('e1d2532')),
                         repo.commit('0d841d1'))
        self.assertEqual(last_commit_to_line(repo, 'file-one.txt', 1,
                                             repo.commit('422cab3')),
                         None)
        self.assertEqual(last_commit_to_line(repo, 'file-one.txt', 1,
                                             repo.commit('e1d2532')),
                         repo.commit('e1d2532'))


if __name__ == '__main__':
    unittest.main()
