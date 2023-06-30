from dateutil.parser import isoparse

from ..core.domain import BaseDomain


class DeprecationInfo(BaseDomain):
    """Describes if, when & how the resources was deprecated. If this field is set to ``None`` the resource is not
    deprecated. If it has a value, it is considered deprecated.

    :param announced: datetime
           Date of when the deprecation was announced.
    :param unavailable_after: datetime
           After the time in this field, the resource will not be available from the general listing endpoint of the
           resource type, and it can not be used in new resources. For example, if this is an image, you can not create
           new servers with this image after the mentioned date.
    """

    __slots__ = (
        "announced",
        "unavailable_after",
    )

    def __init__(
        self,
        announced=None,
        unavailable_after=None,
    ):
        self.announced = isoparse(announced) if announced else None
        self.unavailable_after = (
            isoparse(unavailable_after) if unavailable_after else None
        )
