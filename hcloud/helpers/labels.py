from __future__ import annotations

import re


class LabelValidator:
    KEY_REGEX = re.compile(
        r"^([a-z0-9A-Z]((?:[\-_.]|[a-z0-9A-Z]){0,253}[a-z0-9A-Z])?/)?[a-z0-9A-Z]((?:[\-_.]|[a-z0-9A-Z]|){0,61}[a-z0-9A-Z])?$"
    )
    VALUE_REGEX = re.compile(
        r"^(([a-z0-9A-Z](?:[\-_.]|[a-z0-9A-Z]){0,61})?[a-z0-9A-Z]$|$)"
    )

    @staticmethod
    def validate(labels: dict[str, str]) -> bool:
        """Validates Labels. If you want to know which key/value pair of the dict is not correctly formatted
        use :func:`~hcloud.helpers.labels.validate_verbose`.

        :return:  bool
        """
        for key, value in labels.items():
            if LabelValidator.KEY_REGEX.match(key) is None:
                return False
            if LabelValidator.VALUE_REGEX.match(value) is None:
                return False
        return True

    @staticmethod
    def validate_verbose(labels: dict[str, str]) -> tuple[bool, str]:
        """Validates Labels and returns the corresponding error message if something is wrong. Returns True, <empty string>
        if everything is fine.

        :return:  bool, str
        """
        for key, value in labels.items():
            if LabelValidator.KEY_REGEX.match(key) is None:
                return (
                    False,
                    f"label key {key} is not correctly formatted",
                )
            if LabelValidator.VALUE_REGEX.match(value) is None:
                return (
                    False,
                    f"label value {value} (key: {key}) is not correctly formatted",
                )
        return True, ""
