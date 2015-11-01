import nose
import angr
import subprocess

import logging
l = logging.getLogger('angr.tests.strtol')

import os
test_location = str(os.path.dirname(os.path.realpath(__file__)))


def test_strtol():
    b = angr.Project(os.path.join(test_location, "../../binaries/tests/x86_64/strtol_test"))

    pg = b.factory.path_group(immutable=False)

    # find the end of main
    expected_outputs = {"base 8 worked\n", "base +8 worked\n", "0x worked\n", "+0x worked\n", "base +10 worked\n",
                        "base 10 worked\n", "base -8 worked\n", "-0x worked\n", "base -10 worked\n", "Nope\n"}
    pg.explore(find=0x400804, num_find=len(expected_outputs))

    # check the outputs
    pipe = subprocess.PIPE
    for f in pg.found:
        test_input = f.state.posix.dumps(0)
        test_output = f.state.posix.dumps(1)
        expected_outputs.remove(test_output)

        # check the output works as expected
        p = subprocess.Popen("./test2", stdout=pipe, stderr=pipe, stdin=pipe)
        ret = p.communicate(test_input)[0]
        nose.tools.assert_equal(ret, test_output)

    # check that all of the outputs were seen
    nose.tools.assert_equal(len(expected_outputs), 0)


if __name__ == "__main__":
    test_strtol()
