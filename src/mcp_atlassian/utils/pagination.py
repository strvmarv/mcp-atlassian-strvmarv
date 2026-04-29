"""Pagination caps to protect both the upstream server and the LLM context.

A single tool call that asks for thousands of results forces N backend
round-trips and dumps a huge response into the model. This module clamps
user-supplied `limit` values to a configurable ceiling, applied at the
mixin entry point so every caller (FastMCP tool, programmatic, etc.)
benefits.
"""

import logging
import os

logger = logging.getLogger("mcp-atlassian.pagination")

DEFAULT_MAX_PAGINATION_LIMIT = 100


def clamp_limit(requested: int, *, context: str = "pagination") -> int:
    """Clamp `requested` to ATLASSIAN_MAX_PAGINATION_LIMIT (default 100).

    A non-positive cap disables clamping. Negative or zero `requested` is
    passed through unchanged so callers' own validation still applies.
    """
    if requested <= 0:
        return requested

    raw = os.getenv("ATLASSIAN_MAX_PAGINATION_LIMIT")
    cap = DEFAULT_MAX_PAGINATION_LIMIT
    if raw:
        try:
            cap = int(raw)
        except ValueError:
            logger.warning(
                "Invalid ATLASSIAN_MAX_PAGINATION_LIMIT=%r; using default %d",
                raw,
                DEFAULT_MAX_PAGINATION_LIMIT,
            )

    if cap <= 0:
        return requested
    if requested > cap:
        logger.info(
            "%s: limit %d clamped to %d (ATLASSIAN_MAX_PAGINATION_LIMIT)",
            context,
            requested,
            cap,
        )
        return cap
    return requested
