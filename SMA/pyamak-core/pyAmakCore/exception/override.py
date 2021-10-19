"""
Warning for the methods which must be override
"""


class ToOverrideWarning:
    """
    Warning raised a method that should be override is called
    """
    __enable_warning = True

    def __init__(
            self,
            name: str
    ) -> None:
        if ToOverrideWarning.__enable_warning:
            print("[WARNING] : Method " + name + " was called without being override.")

    @classmethod
    def enable_warning(cls, condition: bool) -> None:
        """
        enable or disable custom warning for method that should be override
        """
        cls.__enable_warning = condition
