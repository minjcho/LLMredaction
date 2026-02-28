"""Tests for app.detectors.regex_detector."""

from app.detectors.regex_detector import detect, _valid_rrn, _valid_brn


# ── RRN_KR ──────────────────────────────────────────────────────

class TestRRN:
    def test_valid_rrn_with_dash(self):
        spans = detect("주민번호 900101-1234568 입니다")
        assert len(spans) == 1
        assert spans[0].type == "RRN_KR"
        assert spans[0].text == "900101-1234568"

    def test_valid_rrn_without_dash(self):
        spans = detect("주민번호 9001011234568 입니다")
        assert len(spans) == 1
        assert spans[0].type == "RRN_KR"

    def test_invalid_rrn_checksum(self):
        # Change last digit to make checksum invalid
        spans = detect("주민번호 900101-1234569 입니다")
        assert len(spans) == 0

    def test_rrn_gender_digit_1(self):
        spans = detect("900101-1234568")
        assert len(spans) == 1

    def test_rrn_gender_digit_2(self):
        spans = detect("900101-2234567")
        # Verify checksum
        assert all(s.type == "RRN_KR" for s in spans)

    def test_rrn_gender_digit_3(self):
        spans = detect("900101-3234567")
        assert all(s.type == "RRN_KR" for s in spans)

    def test_rrn_gender_digit_4(self):
        spans = detect("900101-4234567")
        assert all(s.type == "RRN_KR" for s in spans)

    def test_rrn_invalid_gender_digit_0(self):
        """Gender digit must be 1-4."""
        spans = detect("900101-0234567")
        rrn_spans = [s for s in spans if s.type == "RRN_KR"]
        assert len(rrn_spans) == 0

    def test_rrn_position(self):
        text = "앞텍스트 900101-1234568 뒤텍스트"
        spans = detect(text)
        rrn_spans = [s for s in spans if s.type == "RRN_KR"]
        assert len(rrn_spans) == 1
        assert text[rrn_spans[0].start : rrn_spans[0].end] == "900101-1234568"

    def test_valid_rrn_helper(self):
        assert _valid_rrn("9001011234568") is True

    def test_invalid_rrn_helper(self):
        assert _valid_rrn("9001011234560") is False

    def test_rrn_helper_short(self):
        assert _valid_rrn("12345") is False

    def test_rrn_helper_nonnumeric(self):
        assert _valid_rrn("900101123456a") is False


# ── BRN_KR ──────────────────────────────────────────────────────

class TestBRN:
    def test_valid_brn_with_dashes(self):
        spans = detect("사업자번호 123-45-67891 입니다")
        brn = [s for s in spans if s.type == "BRN_KR"]
        assert len(brn) == 1
        assert brn[0].text == "123-45-67891"

    def test_valid_brn_without_dashes(self):
        spans = detect("사업자번호 1234567891 입니다")
        brn = [s for s in spans if s.type == "BRN_KR"]
        assert len(brn) == 1

    def test_invalid_brn_checksum(self):
        spans = detect("사업자번호 123-45-67890 입니다")
        brn = [s for s in spans if s.type == "BRN_KR"]
        assert len(brn) == 0

    def test_valid_brn_helper(self):
        assert _valid_brn("1234567891") is True

    def test_invalid_brn_helper(self):
        assert _valid_brn("1234567890") is False

    def test_brn_helper_short(self):
        assert _valid_brn("12345") is False

    def test_brn_helper_nonnumeric(self):
        assert _valid_brn("123456789a") is False


# ── PHONE_KR ────────────────────────────────────────────────────

class TestPhone:
    def test_mobile_010_with_dash(self):
        spans = detect("전화 010-1234-5678")
        phone = [s for s in spans if s.type == "PHONE_KR"]
        assert len(phone) == 1

    def test_mobile_010_without_dash(self):
        spans = detect("전화 01012345678")
        phone = [s for s in spans if s.type == "PHONE_KR"]
        assert len(phone) == 1

    def test_mobile_011(self):
        spans = detect("전화 011-234-5678")
        phone = [s for s in spans if s.type == "PHONE_KR"]
        assert len(phone) == 1

    def test_landline_02_not_matched(self):
        """02 is 2-digit area code; regex requires 3-digit (0[2-6][0-9])."""
        spans = detect("전화 02-1234-5678")
        phone = [s for s in spans if s.type == "PHONE_KR"]
        assert len(phone) == 0

    def test_landline_031(self):
        spans = detect("전화 031-123-4567")
        phone = [s for s in spans if s.type == "PHONE_KR"]
        assert len(phone) == 1

    def test_three_digit_middle(self):
        spans = detect("전화 010-123-4567")
        phone = [s for s in spans if s.type == "PHONE_KR"]
        assert len(phone) == 1


# ── PLATE_KR ────────────────────────────────────────────────────

class TestPlate:
    def test_two_digit_plate(self):
        spans = detect("차량 12가1234")
        plate = [s for s in spans if s.type == "PLATE_KR"]
        assert len(plate) == 1

    def test_three_digit_plate(self):
        spans = detect("차량 123가1234")
        plate = [s for s in spans if s.type == "PLATE_KR"]
        assert len(plate) == 1

    def test_no_hangul_no_match(self):
        spans = detect("차량 12A1234")
        plate = [s for s in spans if s.type == "PLATE_KR"]
        assert len(plate) == 0


# ── EMAIL ───────────────────────────────────────────────────────

class TestEmail:
    def test_standard_email(self):
        spans = detect("이메일 user@example.com 입니다")
        email = [s for s in spans if s.type == "EMAIL"]
        assert len(email) == 1
        assert email[0].text == "user@example.com"

    def test_plus_tag_email(self):
        spans = detect("이메일 user+tag@example.com 입니다")
        email = [s for s in spans if s.type == "EMAIL"]
        assert len(email) == 1

    def test_invalid_email_no_at(self):
        spans = detect("이메일 userexample.com 입니다")
        email = [s for s in spans if s.type == "EMAIL"]
        assert len(email) == 0

    def test_invalid_email_no_domain(self):
        spans = detect("이메일 user@ 입니다")
        email = [s for s in spans if s.type == "EMAIL"]
        assert len(email) == 0


# ── BANK_ACCOUNT ────────────────────────────────────────────────

class TestBankAccount:
    def test_standard_format(self):
        spans = detect("계좌번호 110-123-456789 입니다")
        bank = [s for s in spans if s.type == "BANK_ACCOUNT"]
        assert len(bank) == 1

    def test_different_format(self):
        spans = detect("계좌번호 1234-56-789012 입니다")
        bank = [s for s in spans if s.type == "BANK_ACCOUNT"]
        assert len(bank) == 1


# ── API_KEY ─────────────────────────────────────────────────────

class TestAPIKey:
    def test_api_key_equals(self):
        spans = detect('api_key = "abcdefghij1234567890XY"')
        api = [s for s in spans if s.type == "API_KEY"]
        assert len(api) == 1
        assert api[0].text == "abcdefghij1234567890XY"

    def test_api_key_colon(self):
        spans = detect('api_key: "abcdefghij1234567890XY"')
        api = [s for s in spans if s.type == "API_KEY"]
        assert len(api) == 1

    def test_api_key_case_insensitive(self):
        spans = detect("API_KEY=abcdefghij1234567890XY")
        api = [s for s in spans if s.type == "API_KEY"]
        assert len(api) == 1

    def test_token_keyword(self):
        spans = detect('token = "abcdefghij1234567890XY"')
        api = [s for s in spans if s.type == "API_KEY"]
        assert len(api) == 1

    def test_secret_keyword(self):
        spans = detect('secret = "abcdefghij1234567890XY"')
        api = [s for s in spans if s.type == "API_KEY"]
        assert len(api) == 1

    def test_short_value_no_match(self):
        spans = detect('api_key = "short"')
        api = [s for s in spans if s.type == "API_KEY"]
        assert len(api) == 0


# ── Common ──────────────────────────────────────────────────────

class TestCommon:
    def test_empty_string(self):
        assert detect("") == []

    def test_no_pii(self):
        assert detect("오늘 날씨가 좋습니다.") == []

    def test_multiple_types(self):
        text = "번호 010-1234-5678, 이메일 a@b.com, 차량 12가1234"
        spans = detect(text)
        types = {s.type for s in spans}
        assert "PHONE_KR" in types
        assert "EMAIL" in types
        assert "PLATE_KR" in types

    def test_source_is_regex(self):
        spans = detect("user@example.com")
        assert all(s.source == "regex" for s in spans)

    def test_confidence_is_one(self):
        spans = detect("user@example.com")
        assert all(s.confidence == 1.0 for s in spans)
