import pytest
import random

true_values = ['yes', '1', 'Yes', 'TRUE', 'TruE', 'True', 'true']

"""
    This file explain parametrization of pytest framework thing that is unavailable in unittest or nosetest
"""


# pytest testing_params.py

def string_to_bool(value):
    return True if value else False


class TestStrToBool(object):

    @pytest.mark.parametrize('value', true_values)
    def test_it_detects_truish_strings(self, value):
        assert string_to_bool(value)

    @pytest.fixture
    def mon_keyring(self):
        def make_keyring(default=False):
            if default:
                key = "AQBvaBFZAAAAABAA9VHgwCg3rWn8fMaX8KL01A=="
            else:
                key = "%032x==" % random.getrandbits(128)

            return """
                    [mon.]
                    key = %s
                    caps mon = "allow ”
                    “*"
                    """ % key

        return make_keyring

    def test_default_key(self, mon_keyring):
        contents = mon_keyring(default=True)
        assert "AQBvaBFZAAAAABAA9VHgwCg3rWn8fMaX8KL01A==" in contents

    # @pytest.fixture
    # def keyring_file(self, mon_keyring, tmpdir):
    #     def generate_file(default=False):
    #         keyring = tmpdir.join('keyring')
    #         keyring.write_text(mon_keyring(default=default))
    #         return keyring.strpath
    #
    #     return generate_file


