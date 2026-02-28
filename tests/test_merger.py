"""Tests for app.merger."""

from app.merger import merge_spans
from app.schemas import Span


def _span(start, end, type_="EMAIL", source="regex", confidence=1.0):
    return Span(
        start=start,
        end=end,
        type=type_,
        text=f"x" * (end - start),
        source=source,
        confidence=confidence,
    )


class TestMergeSpans:
    def test_empty_list(self):
        assert merge_spans([]) == []

    def test_single_span(self):
        s = _span(0, 5)
        result = merge_spans([s])
        assert len(result) == 1
        assert result[0].start == 0

    def test_non_overlapping(self):
        result = merge_spans([_span(0, 5), _span(10, 15)])
        assert len(result) == 2

    def test_non_overlapping_order(self):
        """Result should be sorted by start position."""
        result = merge_spans([_span(10, 15), _span(0, 5)])
        assert result[0].start == 0
        assert result[1].start == 10

    def test_overlap_source_priority(self):
        """regex (priority 0) beats llm (priority 2) on overlap."""
        regex = _span(0, 10, source="regex")
        llm = _span(5, 15, source="llm")
        result = merge_spans([llm, regex])
        assert len(result) == 1
        assert result[0].source == "regex"

    def test_overlap_type_sensitivity(self):
        """RRN_KR (sensitivity 0) beats EMAIL (sensitivity 3)."""
        rrn = _span(0, 10, type_="RRN_KR", source="regex")
        email = _span(5, 15, type_="EMAIL", source="regex")
        result = merge_spans([email, rrn])
        assert len(result) == 1
        assert result[0].type == "RRN_KR"

    def test_overlap_longer_span_wins(self):
        """Given same source+type, longer span wins."""
        short = _span(0, 5, type_="EMAIL", source="regex")
        long = _span(0, 10, type_="EMAIL", source="regex")
        result = merge_spans([short, long])
        assert len(result) == 1
        assert result[0].end == 10

    def test_overlap_higher_confidence_wins(self):
        """Given same source+type+length, higher confidence wins."""
        low = _span(0, 10, confidence=0.5)
        high = _span(0, 10, confidence=0.9)
        result = merge_spans([low, high])
        assert len(result) == 1
        assert result[0].confidence == 0.9

    def test_partial_overlap(self):
        a = _span(0, 10, source="regex")
        b = _span(8, 20, source="llm")
        result = merge_spans([a, b])
        assert len(result) == 1
        assert result[0].source == "regex"

    def test_full_containment(self):
        outer = _span(0, 20, type_="RRN_KR", source="regex")
        inner = _span(5, 15, type_="EMAIL", source="regex")
        result = merge_spans([inner, outer])
        assert len(result) == 1
        assert result[0].type == "RRN_KR"

    def test_three_way_overlap(self):
        a = _span(0, 10, source="regex", type_="RRN_KR")
        b = _span(5, 15, source="ner", type_="PERSON")
        c = _span(8, 20, source="llm", type_="EMAIL")
        result = merge_spans([c, b, a])
        # regex+RRN_KR has highest priority
        assert len(result) == 1
        assert result[0].source == "regex"

    def test_unknown_source_gets_low_priority(self):
        known = _span(0, 10, source="regex")
        unknown = _span(5, 15, source="unknown_source")
        result = merge_spans([unknown, known])
        assert len(result) == 1
        assert result[0].source == "regex"

    def test_unknown_type_gets_low_priority(self):
        known = _span(0, 10, type_="RRN_KR", source="regex")
        unknown = _span(5, 15, type_="UNKNOWN_TYPE", source="regex")
        result = merge_spans([unknown, known])
        assert len(result) == 1
        assert result[0].type == "RRN_KR"
