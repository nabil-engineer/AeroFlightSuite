from utils.logger import logger


def handle_error(
    error,
    message="Unexpected error",
    raise_error=False,
):
    """
    Centralized error handler.

    Parameters
    ----------
    error : Exception

    message : str

    raise_error : bool
    """

    logger.exception(f"{message}: {error}")

    if raise_error:
        raise error

    return None
