#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from scripts.funding_record import FundingRecordError, load_funding_records


FUNDING_LIST_PLACEHOLDER = "__FUNDING_LIST__"


class FundingIndexError(ValueError):
    pass


def _render_sponsor_label(sponsor: str, award_id: str | None) -> str:
    if not award_id:
        return sponsor
    return f"{sponsor} {award_id}"


def _render_year_range(start_year: int, end_year: int) -> str:
    if start_year == end_year:
        return str(start_year)
    return f"{start_year} - {end_year}"


def _render_public_funding_entry_djot(record) -> str:
    amount_label = f"${record.amount_usd:,}"
    sponsor_label = _render_sponsor_label(record.sponsor, record.award_id)
    return (
        f"- {record.title} \\\n"
        f"  {record.role}; {sponsor_label}; {amount_label}; "
        f"{_render_year_range(record.start_year, record.end_year)}"
    )


def render_public_funding_list_djot(
    root: Path,
    *,
    funding_path: Path | None = None,
) -> str:
    try:
        records = load_funding_records(root, funding_path=funding_path)
    except FundingRecordError as err:
        raise FundingIndexError(str(err)) from err

    rendered = "\n\n".join(_render_public_funding_entry_djot(record) for record in records)
    return rendered + ("\n" if rendered else "")
