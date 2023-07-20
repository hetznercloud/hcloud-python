from __future__ import annotations

import pytest

from hcloud.helpers.labels import LabelValidator


@pytest.mark.parametrize(
    "labels,expected",
    [
        # valid combinations
        ({"label1": "correct.de"}, True),
        ({"empty/label": ""}, True),
        ({"label3-test.de/hallo.welt": "233344444443"}, True),
        ({"label2.de/hallo": "1correct2.de"}, True),
        # invalid value
        ({"valid_key": "incorrect .com"}, False),
        ({"valid_key": "-incorrect.com"}, False),
        ({"valid_key": "incorrect.com-"}, False),
        ({"valid_key": "incorr,ect.com-"}, False),
        (
            {
                "valid_key": "incorrect-111111111111111111111111111111111111111111111111111111111111.com"
            },
            False,
        ),
        (
            {
                "valid_key": "63-characters-are-allowed-in-a-label__this-is-one-character-more",
            },
            False,
        ),
        # invalid keys
        ({"incorrect.de/": "correct.de"}, False),
        ({"incor rect.de/": "correct.de"}, False),
        ({"incorrect.de/+": "correct.de"}, False),
        ({"-incorrect.de": "correct.de"}, False),
        ({"incorrect.de-": "correct.de"}, False),
        ({"incorrect.de/tes t": "correct.de"}, False),
        ({"incorrect.de/test-": "correct.de"}, False),
        (
            {
                "incorrect.de/test-dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd": "correct.de"
            },
            False,
        ),
        (
            {
                "incorrect-11111111111111111111111111111111111111111111111111111111111111111111111111111111"
                + "11111111111111111111111111111111111111111111111111111111111111111111111111111111"
                + "11111111111111111111111111111111111111111111111111111111111111111111111111111111"
                + "11111111111111111111111111111111111111111111111111111111111111111111111111111111"
                + "11111111111111111111111111111111111111111111111111111111111111111111111111111111"
                + "11111111111111111111111111111111111111111111111111111111111111111111111111111111"
                + "11111111111111111111111111111111111111111111111111111111111111111111111111111111"
                + ".de/test": "correct.de"
            },
            False,
        ),
    ],
)
def test_validate(labels, expected):
    assert LabelValidator.validate(labels=labels) == expected


@pytest.mark.parametrize(
    "labels,expected,type",
    [
        # valid combinations
        ({"label1": "correct.de"}, True, ""),
        ({"empty/label": ""}, True, ""),
        ({"label3-test.de/hallo.welt": "233344444443"}, True, ""),
        ({"label2.de/hallo": "1correct2.de"}, True, ""),
        # invalid value
        ({"valid_key": "incorrect .com"}, False, "value"),
        ({"valid_key": "-incorrect.com"}, False, "value"),
        ({"valid_key": "incorrect.com-"}, False, "value"),
        ({"valid_key": "incorr,ect.com-"}, False, "value"),
        (
            {
                "valid_key": "incorrect-111111111111111111111111111111111111111111111111111111111111.com"
            },
            False,
            "value",
        ),
        (
            {
                "valid_key": "63-characters-are-allowed-in-a-label__this-is-one-character-more",
            },
            False,
            "value",
        ),
        # invalid keys
        ({"incorrect.de/": "correct.de"}, False, "key"),
        ({"incor rect.de/": "correct.de"}, False, "key"),
        ({"incorrect.de/+": "correct.de"}, False, "key"),
        ({"-incorrect.de": "correct.de"}, False, "key"),
        ({"incorrect.de-": "correct.de"}, False, "key"),
        ({"incorrect.de/tes t": "correct.de"}, False, "key"),
        ({"incorrect.de/test-": "correct.de"}, False, "key"),
        (
            {
                "incorrect.de/test-dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd": "correct.de"
            },
            False,
            "key",
        ),
        (
            {
                "incorrect-11111111111111111111111111111111111111111111111111111111111111111111111111111111"
                + "11111111111111111111111111111111111111111111111111111111111111111111111111111111"
                + "11111111111111111111111111111111111111111111111111111111111111111111111111111111"
                + "11111111111111111111111111111111111111111111111111111111111111111111111111111111"
                + "11111111111111111111111111111111111111111111111111111111111111111111111111111111"
                + "11111111111111111111111111111111111111111111111111111111111111111111111111111111"
                + "11111111111111111111111111111111111111111111111111111111111111111111111111111111"
                + ".de/test": "correct.de"
            },
            False,
            "key",
        ),
    ],
)
def test_validate_verbose(labels, expected, type):
    result, error = LabelValidator.validate_verbose(labels=labels)
    if type == "key" and expected is False:
        assert error == f"label key {list(labels.keys())[0]} is not correctly formatted"
    elif type == "value" and expected is False:
        assert (
            error
            == f"label value {list(labels.values())[0]} (key: {list(labels.keys())[0]}) is not correctly formatted"
        )

    assert result == expected
