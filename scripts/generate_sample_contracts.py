"""Generate multilingual sample contract PDFs for PII masking testing.

Produces realistic, investor-demo-ready contracts with PII distributed
naturally throughout the document (not concentrated in a single section).
"""

from fpdf import FPDF
from pathlib import Path

FONT_PATHS = [
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
]
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "samples"


def _find_font() -> str:
    for p in FONT_PATHS:
        if Path(p).exists():
            return p
    raise FileNotFoundError(
        "Arial Unicode.ttf not found. Searched: " + ", ".join(FONT_PATHS)
    )


def _make_pdf() -> FPDF:
    pdf = FPDF()
    font_path = _find_font()
    pdf.add_font("ArialUnicode", "", font_path)
    pdf.add_font("ArialUnicode", "B", font_path)
    pdf.set_auto_page_break(auto=True, margin=20)
    return pdf


def _title(pdf: FPDF, text: str) -> None:
    pdf.set_font("ArialUnicode", "B", 18)
    pdf.cell(0, 12, text, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(6)


def _subtitle(pdf: FPDF, text: str) -> None:
    pdf.set_font("ArialUnicode", "", 11)
    pdf.cell(0, 8, text, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(2)


def _heading(pdf: FPDF, text: str) -> None:
    pdf.set_font("ArialUnicode", "B", 13)
    pdf.cell(0, 10, text, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)


def _subheading(pdf: FPDF, text: str) -> None:
    pdf.set_font("ArialUnicode", "B", 11)
    pdf.cell(0, 8, text, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)


def _body(pdf: FPDF, text: str) -> None:
    pdf.set_font("ArialUnicode", "", 11)
    pdf.multi_cell(0, 7, text)
    pdf.ln(3)


def _small(pdf: FPDF, text: str) -> None:
    pdf.set_font("ArialUnicode", "", 9)
    pdf.multi_cell(0, 5, text)
    pdf.ln(2)


# ── Korean ──────────────────────────────────────────────────────────────────


def generate_korean_contract(output_dir: Path) -> None:
    pdf = _make_pdf()
    pdf.add_page()

    _title(pdf, "소프트웨어 개발 용역 계약서")
    _subtitle(pdf, "계약번호: KR-2024-0315-A0078")

    _body(pdf, (
        "주식회사 넥스트이노베이션(이하 \"갑\"이라 한다)과 "
        "프리랜서 개발자 박영희(이하 \"을\"이라 한다)는 "
        "아래와 같이 소프트웨어 개발 용역 계약을 체결한다."
    ))

    # ── 제1조 ──
    _heading(pdf, "제1조 (당사자)")

    _subheading(pdf, "1. 갑 (위탁자)")
    _body(pdf, (
        "회사명: 주식회사 넥스트이노베이션\n"
        "대표이사: 김철수\n"
        "사업자등록번호: 214-87-45123\n"
        "법인등록번호: 110111-5678901\n"
        "본사 소재지: 서울특별시 강남구 테헤란로 152, 강남파이낸스센터 22층\n"
        "전화번호: 02-555-0100\n"
        "팩스: 02-555-0101\n"
        "이메일: chulsoo.kim@nextinnovation.co.kr"
    ))

    _subheading(pdf, "2. 을 (수탁자)")
    _body(pdf, (
        "성명: 박영희\n"
        "주민등록번호: 850315-2987654\n"
        "전화번호: 010-9876-5432\n"
        "이메일: younghee.park@devmail.kr\n"
        "주소: 서울특별시 서초구 반포대로 58, 래미안퍼스티지 301동 1204호\n"
        "사업자등록번호: 481-26-00987 (개인사업자)"
    ))

    # ── 제2조 ──
    _heading(pdf, "제2조 (계약의 목적)")
    _body(pdf, (
        "본 계약은 갑이 운영하는 'AI 기반 문서 자동 분류 시스템'(프로젝트명: DocuMind)의 "
        "백엔드 API 서버 및 관리자 대시보드 개발을 을에게 위탁하고, "
        "을이 이를 수행함에 있어 필요한 제반 사항을 규정함을 목적으로 한다."
    ))

    # ── 제3조 ──
    _heading(pdf, "제3조 (용역의 범위)")
    _body(pdf, (
        "을이 수행할 용역의 범위는 다음과 같다.\n\n"
        "  1. RESTful API 서버 설계 및 개발 (Python/FastAPI 기반)\n"
        "  2. PostgreSQL 데이터베이스 스키마 설계 및 마이그레이션\n"
        "  3. 관리자 대시보드 프론트엔드 개발 (React/TypeScript)\n"
        "  4. AWS 클라우드 인프라 구축 및 CI/CD 파이프라인 설정\n"
        "  5. API 문서화 (OpenAPI/Swagger 규격)\n"
        "  6. 단위 테스트 및 통합 테스트 코드 작성 (코드 커버리지 80% 이상)\n\n"
        "세부 기능 명세는 별첨 '기술 요구 사항 명세서(Appendix A)'에 따른다."
    ))

    # ── 제4조 ──
    _heading(pdf, "제4조 (계약 기간)")
    _body(pdf, (
        "1. 전체 계약 기간: 2024년 4월 1일 ~ 2024년 11월 30일 (총 8개월)\n"
        "2. 각 단계별 일정은 아래와 같다.\n\n"
        "  - 1단계 (설계): 2024년 4월 1일 ~ 2024년 5월 15일\n"
        "  - 2단계 (핵심 개발): 2024년 5월 16일 ~ 2024년 8월 31일\n"
        "  - 3단계 (테스트/안정화): 2024년 9월 1일 ~ 2024년 10월 31일\n"
        "  - 4단계 (배포/인수인계): 2024년 11월 1일 ~ 2024년 11월 30일\n\n"
        "3. 갑의 사유로 인한 일정 지연 시, 해당 기간만큼 계약 기간이 자동 연장된다."
    ))

    # ── 제5조 ──
    _heading(pdf, "제5조 (계약 금액 및 지급 조건)")
    _body(pdf, (
        "1. 총 계약 금액: 금 팔천만원정 (₩80,000,000), 부가가치세 별도\n"
        "2. 지급 일정:\n\n"
        "  - 착수금 (계약 체결 시): ₩20,000,000 (25%)\n"
        "  - 1차 중도금 (2단계 착수 시): ₩20,000,000 (25%)\n"
        "  - 2차 중도금 (3단계 착수 시): ₩20,000,000 (25%)\n"
        "  - 잔금 (최종 납품 및 검수 완료 후 14일 이내): ₩20,000,000 (25%)\n\n"
        "3. 대금 지급 계좌:\n"
        "  은행: 신한은행\n"
        "  계좌번호: 110-432-789012\n"
        "  예금주: 박영희\n\n"
        "4. 갑은 을의 세금계산서 수령일로부터 14영업일 이내에 해당 금액을 지급한다."
    ))

    # ── 제6조 ──
    _heading(pdf, "제6조 (프로젝트 관리 및 보고)")
    _body(pdf, (
        "1. 을은 매주 월요일 오전 10시까지 주간 업무 보고서를 갑의 프로젝트 매니저에게 "
        "이메일로 제출한다.\n"
        "  프로젝트 매니저: 이준혁\n"
        "  이메일: junhyuk.lee@nextinnovation.co.kr\n"
        "  전화: 010-2345-6789\n\n"
        "2. 격주 수요일 오후 2시에 화상 회의를 통해 진척 현황을 점검한다.\n\n"
        "3. 을은 모든 소스 코드를 갑이 지정한 Git 저장소에 커밋하며, "
        "코드 리뷰 승인 없이 main 브랜치에 직접 병합할 수 없다."
    ))

    # ── 제7조 ──
    _heading(pdf, "제7조 (검수)")
    _body(pdf, (
        "1. 각 단계 완료 시 을은 갑에게 산출물을 제출하고, "
        "갑은 수령일로부터 10영업일 이내에 검수를 완료한다.\n\n"
        "2. 갑이 검수 기간 내에 서면으로 이의를 제기하지 않는 경우, "
        "해당 단계의 산출물은 검수에 합격한 것으로 간주한다.\n\n"
        "3. 검수에 불합격한 경우, 을은 갑의 보완 요청을 수령한 날로부터 "
        "5영업일 이내에 수정·보완하여 재제출한다."
    ))

    # ── 제8조 ──
    _heading(pdf, "제8조 (지식재산권)")
    _body(pdf, (
        "1. 본 계약에 따라 을이 개발한 소프트웨어의 저작재산권은 "
        "최종 대금 지급 완료 시 갑에게 귀속된다.\n\n"
        "2. 을이 계약 이전에 보유하고 있던 범용 라이브러리 및 도구는 "
        "을의 소유로 유지되며, 갑에게 비독점적 사용 라이선스가 부여된다.\n\n"
        "3. 을은 본 계약의 산출물과 실질적으로 동일한 소프트웨어를 "
        "갑의 경쟁사에 제공하여서는 아니 된다."
    ))

    # ── 제9조 ──
    _heading(pdf, "제9조 (비밀유지)")
    _body(pdf, (
        "1. 양 당사자는 본 계약의 이행 과정에서 알게 된 상대방의 영업비밀, "
        "기술 정보, 고객 정보, 그리고 개인정보(주민등록번호, 연락처, 주소 등)를 "
        "계약 기간 및 종료 후 3년간 제3자에게 누설하거나 본 계약 이외의 목적으로 "
        "사용하여서는 아니 된다.\n\n"
        "2. 비밀유지 의무를 위반할 경우, 위반 당사자는 상대방에게 "
        "금 오천만원정 (₩50,000,000)의 위약금을 지급한다."
    ))

    # ── 제10조 ──
    _heading(pdf, "제10조 (손해배상)")
    _body(pdf, (
        "1. 갑 또는 을이 본 계약상의 의무를 위반하여 상대방에게 손해를 입힌 경우, "
        "귀책사유 있는 당사자는 상대방에게 발생한 직접적인 손해를 배상한다.\n\n"
        "2. 손해배상의 총액은 본 계약 총 금액을 초과하지 아니한다.\n\n"
        "3. 천재지변, 전쟁, 감염병 확산 등 불가항력적 사유로 인한 계약 불이행에 대해서는 "
        "어느 당사자도 책임을 지지 아니한다."
    ))

    # ── 제11조 ──
    _heading(pdf, "제11조 (계약 해지)")
    _body(pdf, (
        "1. 일방 당사자가 본 계약의 중요한 조항을 위반하고, 상대방의 서면 시정 요구를 "
        "수령한 날로부터 15영업일 이내에 시정하지 아니한 경우, "
        "상대방은 본 계약을 해지할 수 있다.\n\n"
        "2. 갑의 사유로 중도 해지하는 경우, 갑은 을에게 기 수행분에 대한 대가와 "
        "함께 잔여 계약 금액의 20%를 위약금으로 지급한다.\n\n"
        "3. 을의 사유로 중도 해지하는 경우, 을은 기 수령한 대금 중 "
        "미수행분에 해당하는 금액을 갑에게 반환한다."
    ))

    # ── 제12조 ──
    _heading(pdf, "제12조 (분쟁 해결)")
    _body(pdf, (
        "본 계약에 관한 분쟁이 발생한 경우, 양 당사자는 우선 성실히 협의하여 "
        "해결하기로 하며, 협의가 이루어지지 않을 경우 서울중앙지방법원을 "
        "관할 법원으로 하여 소송으로 해결한다."
    ))

    # ── 제13조 ──
    _heading(pdf, "제13조 (일반 조항)")
    _body(pdf, (
        "1. 본 계약은 양 당사자의 서면 합의 없이 제3자에게 양도할 수 없다.\n"
        "2. 본 계약에 명시되지 않은 사항은 민법 및 관계 법령에 따른다.\n"
        "3. 본 계약은 2부를 작성하여 갑과 을이 각각 1부씩 보관한다."
    ))

    # ── 서명란 ──
    _body(pdf, "\n")
    _body(pdf, (
        "위 계약 내용을 충분히 이해하고 이에 동의하여, "
        "갑과 을은 아래에 서명 날인한다.\n\n"
        "2024년 3월 15일\n\n\n"
        "갑 (위탁자)\n"
        "주식회사 넥스트이노베이션\n"
        "대표이사: 김철수 (인)\n\n\n"
        "을 (수탁자)\n"
        "박영희 (인)\n"
        "주민등록번호: 850315-2987654"
    ))

    # ── 별첨 ──
    pdf.add_page()
    _heading(pdf, "[별첨] 비상 연락처 및 프로젝트 관계자 정보")
    _body(pdf, (
        "1. 갑측 관계자\n\n"
        "  - 프로젝트 총괄: 김철수 (대표이사)\n"
        "    전화: 010-1234-5678 / 이메일: chulsoo.kim@nextinnovation.co.kr\n\n"
        "  - 프로젝트 매니저: 이준혁 (개발팀장)\n"
        "    전화: 010-2345-6789 / 이메일: junhyuk.lee@nextinnovation.co.kr\n\n"
        "  - 기술 검토: 최민지 (수석 엔지니어)\n"
        "    전화: 010-3456-7890 / 이메일: minji.choi@nextinnovation.co.kr\n\n"
        "  - 법무 담당: 정서연 (법무팀)\n"
        "    전화: 02-555-0105 / 이메일: seoyeon.jung@nextinnovation.co.kr\n\n"
        "2. 을측\n\n"
        "  - 개발자: 박영희\n"
        "    전화: 010-9876-5432 / 이메일: younghee.park@devmail.kr\n"
        "    비상 연락처: 010-5555-9999 (배우자 박준서)\n\n"
        "3. 갑측 대금 지급 담당\n\n"
        "  - 재무팀: 한소라\n"
        "    전화: 02-555-0110 / 이메일: sora.han@nextinnovation.co.kr\n"
        "    갑 대금 지급 계좌: 국민은행 467901-04-123456 (주식회사 넥스트이노베이션)"
    ))

    out = output_dir / "contract_ko.pdf"
    pdf.output(str(out))
    print(f"  Created {out}")


# ── English (Series A Investment Agreement) ─────────────────────────────────


def generate_english_contract(output_dir: Path) -> None:
    pdf = _make_pdf()
    pdf.add_page()

    _title(pdf, "Series A Preferred Stock Purchase Agreement")
    _subtitle(pdf, "Vertex Analytics, Inc.")
    _subtitle(pdf, "Dated as of March 15, 2024")

    _body(pdf, (
        "This Series A Preferred Stock Purchase Agreement (this \"Agreement\") is "
        "entered into as of March 15, 2024, by and among Vertex Analytics, Inc., "
        "a Delaware corporation (the \"Company\"), and the investors listed on "
        "Exhibit A attached hereto (each, an \"Investor\" and collectively, "
        "the \"Investors\")."
    ))

    # ── 1. Purchase and Sale ──
    _heading(pdf, "1. Purchase and Sale of Series A Preferred Stock")

    _subheading(pdf, "1.1 Sale and Issuance")
    _body(pdf, (
        "Subject to the terms and conditions of this Agreement, each Investor "
        "agrees to purchase at the Closing, and the Company agrees to sell and "
        "issue to each Investor, that number of shares of Series A Preferred Stock "
        "set forth opposite such Investor's name on Exhibit A, at a purchase price "
        "of $4.25 per share (the \"Purchase Price\")."
    ))

    _subheading(pdf, "1.2 Closing")
    _body(pdf, (
        "The initial closing (the \"Closing\") of the purchase and sale of "
        "the Series A Preferred Stock shall take place at the offices of "
        "Morrison & Blake LLP, 1290 Avenue of the Americas, 35th Floor, "
        "New York, NY 10104, at 10:00 a.m. Eastern Time on April 1, 2024, "
        "or at such other time and place as the Company and the Lead Investor "
        "mutually agree (the \"Closing Date\")."
    ))

    _subheading(pdf, "1.3 Aggregate Investment")
    _body(pdf, (
        "The aggregate purchase price for all shares of Series A Preferred Stock "
        "to be sold at the Closing is $8,500,000.00 (Eight Million Five Hundred "
        "Thousand Dollars), representing 2,000,000 shares at $4.25 per share."
    ))

    # ── 2. Parties ──
    _heading(pdf, "2. Company and Investor Information")

    _subheading(pdf, "2.1 The Company")
    _body(pdf, (
        "Legal Name: Vertex Analytics, Inc.\n"
        "State of Incorporation: Delaware\n"
        "EIN: 82-4591037\n"
        "Principal Office: 350 Fifth Avenue, Suite 4800, New York, NY 10118\n\n"
        "CEO and Co-Founder: Robert Chen\n"
        "  Phone: +1-212-555-0190\n"
        "  Email: robert.chen@vertexanalytics.com\n"
        "  Home Address: 88 Greenwich Street, Apt 3901, New York, NY 10006\n"
        "  SSN (last four on file): 4521\n\n"
        "CTO and Co-Founder: John Smith\n"
        "  Phone: +1-212-555-0147\n"
        "  Email: john.smith@vertexanalytics.com\n"
        "  Home Address: 415 East 54th Street, Apt 12F, New York, NY 10022\n"
        "  SSN (last four on file): 7890"
    ))

    _subheading(pdf, "2.2 Lead Investor")
    _body(pdf, (
        "Fund Name: Horizon Ventures Fund III, L.P.\n"
        "Managing Partner: Katherine Liu\n"
        "EIN: 47-3829156\n"
        "Address: 2000 Sand Hill Road, Suite 220, Menlo Park, CA 94025\n"
        "Phone: +1-650-555-0312\n"
        "Email: katherine.liu@horizonvc.com\n\n"
        "Investment Amount: $5,000,000.00 (1,176,471 shares)\n\n"
        "Wire Instructions for Capital Calls:\n"
        "  Bank: Silicon Valley Bank (a division of First Citizens Bank)\n"
        "  Routing: 121140399\n"
        "  Account: 3301-8847-2210\n"
        "  Account Name: Horizon Ventures Fund III, L.P.\n"
        "  SWIFT: SVBKUS6S"
    ))

    _subheading(pdf, "2.3 Co-Investor")
    _body(pdf, (
        "Fund Name: Eastbridge Capital Partners, LLC\n"
        "Managing Director: James O'Brien\n"
        "EIN: 61-7724830\n"
        "Address: 100 Federal Street, 29th Floor, Boston, MA 02110\n"
        "Phone: +1-617-555-0278\n"
        "Email: jobrien@eastbridgecap.com\n\n"
        "Investment Amount: $2,500,000.00 (588,235 shares)"
    ))

    _subheading(pdf, "2.4 Angel Investor")
    _body(pdf, (
        "Name: Sarah Williams\n"
        "SSN (last four on file): 3344\n"
        "Address: 742 Evergreen Terrace, Apt 5C, San Francisco, CA 94102\n"
        "Phone: +1-415-555-0199\n"
        "Email: sarah.williams.angel@gmail.com\n\n"
        "Investment Amount: $1,000,000.00 (235,294 shares)"
    ))

    # ── 3. Representations — Company ──
    _heading(pdf, "3. Representations and Warranties of the Company")
    _body(pdf, (
        "The Company hereby represents and warrants to each Investor as follows:\n\n"
        "3.1 Organization. The Company is a corporation duly organized, validly "
        "existing, and in good standing under the laws of the State of Delaware, "
        "and has all requisite corporate power and authority to own and operate "
        "its properties and assets, to execute and deliver this Agreement, and "
        "to carry on its business as presently conducted.\n\n"
        "3.2 Capitalization. The authorized capital stock of the Company, "
        "immediately prior to the Closing, consists of:\n"
        "  (a) 20,000,000 shares of Common Stock, of which 8,000,000 are "
        "issued and outstanding; and\n"
        "  (b) 5,000,000 shares of Preferred Stock, of which 2,000,000 shares "
        "have been designated Series A Preferred Stock, none of which are "
        "issued and outstanding.\n\n"
        "3.3 Financial Statements. The Company has delivered to the Investors "
        "unaudited financial statements (balance sheet, income statement, and "
        "cash flow statement) for the fiscal year ended December 31, 2023. "
        "Such financial statements have been prepared in accordance with GAAP "
        "and fairly present the financial condition of the Company.\n\n"
        "3.4 No Litigation. There is no action, suit, proceeding, or investigation "
        "pending or, to the Company's knowledge, currently threatened against the Company."
    ))

    # ── 4. Representations — Investors ──
    _heading(pdf, "4. Representations and Warranties of the Investors")
    _body(pdf, (
        "Each Investor hereby represents and warrants that:\n\n"
        "4.1 Such Investor is an \"accredited investor\" as defined in "
        "Rule 501(a) of Regulation D.\n\n"
        "4.2 Such Investor is acquiring the shares for investment for its own "
        "account and not with a view to, or for resale in connection with, "
        "any distribution thereof.\n\n"
        "4.3 Such Investor has sufficient knowledge and experience in financial "
        "and business matters to evaluate the merits and risks of an investment "
        "in the Company.\n\n"
        "4.4 Such Investor has had the opportunity to ask questions and receive "
        "answers from the Company regarding the Company, its business, and the "
        "terms of this investment."
    ))

    # ── 5. Rights of Series A ──
    _heading(pdf, "5. Rights, Preferences, and Privileges of Series A Preferred Stock")
    _body(pdf, (
        "5.1 Dividends. Holders of Series A Preferred Stock shall be entitled to "
        "receive non-cumulative dividends at a rate of 8% per annum on the "
        "Purchase Price, when and if declared by the Board of Directors.\n\n"
        "5.2 Liquidation Preference. In the event of any liquidation, dissolution, "
        "or winding up of the Company, the holders of Series A Preferred Stock "
        "shall be entitled to receive, prior to any distribution to holders of "
        "Common Stock, an amount equal to 1.0x the Purchase Price per share, "
        "plus any declared but unpaid dividends (the \"Liquidation Preference\"). "
        "After payment of the Liquidation Preference, the remaining assets shall "
        "be distributed to the holders of Common Stock.\n\n"
        "5.3 Conversion. Each share of Series A Preferred Stock shall be "
        "convertible, at the option of the holder, into one share of Common Stock, "
        "subject to adjustment for stock splits, dividends, and similar events.\n\n"
        "5.4 Anti-Dilution. The conversion price shall be subject to broad-based "
        "weighted average anti-dilution protection in the event of a down round.\n\n"
        "5.5 Voting Rights. Each holder of Series A Preferred Stock shall have "
        "the right to vote on all matters submitted to a vote of stockholders, "
        "on an as-converted-to-Common-Stock basis."
    ))

    # ── 6. Board and Governance ──
    _heading(pdf, "6. Board of Directors and Governance")
    _body(pdf, (
        "6.1 Board Composition. Immediately following the Closing, the Board "
        "of Directors shall consist of five (5) members:\n"
        "  (a) Two seats designated by the holders of Common Stock "
        "(initially Robert Chen and John Smith);\n"
        "  (b) Two seats designated by the Lead Investor "
        "(initially Katherine Liu and one additional designee); and\n"
        "  (c) One independent seat mutually agreed upon by the Common holders "
        "and the Lead Investor.\n\n"
        "6.2 Board Observer. Eastbridge Capital Partners shall be entitled to "
        "designate one non-voting board observer (initially James O'Brien).\n\n"
        "6.3 Protective Provisions. For so long as any shares of Series A "
        "Preferred Stock remain outstanding, the Company shall not, without "
        "the affirmative vote of the holders of at least a majority of the "
        "Series A Preferred Stock:\n"
        "  (a) alter the rights or preferences of the Series A Preferred Stock;\n"
        "  (b) increase or decrease the authorized number of shares;\n"
        "  (c) create any new class of stock senior to the Series A;\n"
        "  (d) declare or pay any dividend on Common Stock;\n"
        "  (e) sell, lease, or transfer all or substantially all assets; or\n"
        "  (f) incur indebtedness in excess of $500,000."
    ))

    # ── 7. Information Rights ──
    _heading(pdf, "7. Information Rights")
    _body(pdf, (
        "7.1 The Company shall deliver to each Major Investor "
        "(holding at least 500,000 shares of Series A Preferred Stock):\n"
        "  (a) Unaudited quarterly financial statements within 30 days of "
        "each fiscal quarter end;\n"
        "  (b) Audited annual financial statements within 90 days of each "
        "fiscal year end;\n"
        "  (c) An annual budget and operating plan at least 30 days prior to "
        "the beginning of each fiscal year.\n\n"
        "7.2 Financial reports shall be sent to:\n\n"
        "  Horizon Ventures Fund III, L.P.\n"
        "  Attn: Katherine Liu\n"
        "  2000 Sand Hill Road, Suite 220\n"
        "  Menlo Park, CA 94025\n"
        "  Email: portfolio-reports@horizonvc.com\n\n"
        "  Eastbridge Capital Partners, LLC\n"
        "  Attn: James O'Brien\n"
        "  100 Federal Street, 29th Floor\n"
        "  Boston, MA 02110\n"
        "  Email: portfolio@eastbridgecap.com"
    ))

    # ── 8. Right of First Refusal and Co-Sale ──
    _heading(pdf, "8. Right of First Refusal and Co-Sale")
    _body(pdf, (
        "8.1 Right of First Refusal. Before any Key Holder (as defined in "
        "Exhibit B) may sell, transfer, or otherwise dispose of any shares of "
        "Common Stock, such Key Holder shall first offer such shares to the "
        "Investors on a pro rata basis at the same price and on the same terms.\n\n"
        "8.2 Co-Sale Right. If a Key Holder proposes to transfer shares and "
        "the Investors do not exercise their Right of First Refusal in full, "
        "each Investor shall have the right to participate in such transfer "
        "on a pro rata basis.\n\n"
        "8.3 Key Holders. The Key Holders are:\n"
        "  - Robert Chen (4,800,000 shares of Common Stock)\n"
        "  - John Smith (3,200,000 shares of Common Stock)"
    ))

    # ── 9. Drag-Along ──
    _heading(pdf, "9. Drag-Along Rights")
    _body(pdf, (
        "If the holders of at least a majority of the Series A Preferred Stock "
        "and a majority of the Common Stock approve a Deemed Liquidation Event "
        "(including a merger, acquisition, or sale of all or substantially all "
        "assets), all other stockholders shall be required to vote in favor of "
        "and not oppose such transaction, and shall take all actions necessary "
        "to consummate such transaction."
    ))

    # ── 10. Confidentiality ──
    _heading(pdf, "10. Confidentiality")
    _body(pdf, (
        "10.1 Each Investor agrees that all information provided by the Company "
        "in connection with this Agreement, including but not limited to financial "
        "statements, customer data, employee records (names, Social Security Numbers, "
        "compensation details, home addresses), technical specifications, and "
        "business plans, constitutes Confidential Information.\n\n"
        "10.2 Each Investor shall hold Confidential Information in strict "
        "confidence and shall not disclose it to any person other than its "
        "partners, employees, advisors, and legal counsel who need to know "
        "such information.\n\n"
        "10.3 This confidentiality obligation shall survive for 3 years "
        "following termination of this Agreement."
    ))

    # ── 11. Conditions to Closing ──
    _heading(pdf, "11. Conditions to Closing")
    _body(pdf, (
        "11.1 Conditions to Investors' Obligations:\n"
        "  (a) The Company shall have filed an Amended and Restated Certificate "
        "of Incorporation with the Delaware Secretary of State;\n"
        "  (b) The Company shall have delivered an opinion of counsel;\n"
        "  (c) The Investors' Rights Agreement, Right of First Refusal and "
        "Co-Sale Agreement, and Voting Agreement shall have been executed;\n"
        "  (d) The Company shall have complied with all applicable securities laws.\n\n"
        "11.2 Conditions to Company's Obligations:\n"
        "  (a) Each Investor shall have delivered the Purchase Price by wire transfer "
        "to the Company's account:\n"
        "    Bank: JPMorgan Chase\n"
        "    Routing: 021000021\n"
        "    Account: 7729-4410-3356\n"
        "    Account Name: Vertex Analytics, Inc.\n"
        "    SWIFT: CHASUS33\n"
        "  (b) Each Investor shall have executed this Agreement and all ancillary documents."
    ))

    # ── 12. Governing Law ──
    _heading(pdf, "12. Governing Law and Dispute Resolution")
    _body(pdf, (
        "12.1 This Agreement shall be governed by and construed in accordance "
        "with the laws of the State of Delaware, without regard to its "
        "conflict-of-laws principles.\n\n"
        "12.2 Any dispute arising under this Agreement shall be resolved "
        "by binding arbitration administered by JAMS in New York, New York, "
        "in accordance with JAMS Comprehensive Arbitration Rules."
    ))

    # ── 13. General ──
    _heading(pdf, "13. Miscellaneous")
    _body(pdf, (
        "13.1 Entire Agreement. This Agreement, together with the Exhibits, "
        "constitutes the entire agreement among the parties.\n\n"
        "13.2 Amendments. This Agreement may be amended only by a written "
        "instrument signed by the Company and the Lead Investor.\n\n"
        "13.3 Notices. All notices shall be in writing and delivered to the "
        "addresses set forth in this Agreement or as updated by written notice.\n\n"
        "13.4 Expenses. Each party shall bear its own costs and expenses in "
        "connection with this Agreement, except that the Company shall reimburse "
        "the Lead Investor for legal fees up to $25,000.\n\n"
        "13.5 Counterparts. This Agreement may be executed in two or more "
        "counterparts, each of which shall be an original."
    ))

    # ── Signatures ──
    _body(pdf, "\n")
    _body(pdf, (
        "IN WITNESS WHEREOF, the parties have executed this Series A Preferred "
        "Stock Purchase Agreement as of the date first written above.\n\n\n"
        "THE COMPANY:\n"
        "Vertex Analytics, Inc.\n\n"
        "By: _________________________\n"
        "Name: Robert Chen\n"
        "Title: Chief Executive Officer\n"
        "Date: March 15, 2024\n\n\n"
        "LEAD INVESTOR:\n"
        "Horizon Ventures Fund III, L.P.\n"
        "By: Horizon Ventures GP III, LLC, its General Partner\n\n"
        "By: _________________________\n"
        "Name: Katherine Liu\n"
        "Title: Managing Partner\n"
        "Date: March 15, 2024\n\n\n"
        "CO-INVESTOR:\n"
        "Eastbridge Capital Partners, LLC\n\n"
        "By: _________________________\n"
        "Name: James O'Brien\n"
        "Title: Managing Director\n"
        "Date: March 15, 2024\n\n\n"
        "ANGEL INVESTOR:\n\n"
        "By: _________________________\n"
        "Name: Sarah Williams\n"
        "Date: March 15, 2024"
    ))

    # ── Exhibit A ──
    pdf.add_page()
    _heading(pdf, "Exhibit A - Schedule of Investors")
    _body(pdf, (
        "Investor Name                     | Shares     | Purchase Price\n"
        "---------------------------------------------------------------\n"
        "Horizon Ventures Fund III, L.P.   | 1,176,471  | $5,000,000.00\n"
        "Eastbridge Capital Partners, LLC  |   588,235  | $2,500,000.00\n"
        "Sarah Williams                    |   235,294  | $1,000,000.00\n"
        "---------------------------------------------------------------\n"
        "TOTAL                             | 2,000,000  | $8,500,000.00"
    ))

    _heading(pdf, "Exhibit B - Key Holder and Contact Information")
    _body(pdf, (
        "Company Officers:\n\n"
        "  Robert Chen, CEO\n"
        "  88 Greenwich Street, Apt 3901, New York, NY 10006\n"
        "  Phone: +1-212-555-0190 / Email: robert.chen@vertexanalytics.com\n\n"
        "  John Smith, CTO\n"
        "  415 East 54th Street, Apt 12F, New York, NY 10022\n"
        "  Phone: +1-212-555-0147 / Email: john.smith@vertexanalytics.com\n\n"
        "  Lisa Park, CFO\n"
        "  230 West 79th Street, Apt 8A, New York, NY 10024\n"
        "  Phone: +1-212-555-0155 / Email: lisa.park@vertexanalytics.com\n\n"
        "Legal Counsel to the Company:\n\n"
        "  Morrison & Blake LLP\n"
        "  Attn: Michael Torres, Esq.\n"
        "  1290 Avenue of the Americas, 35th Floor, New York, NY 10104\n"
        "  Phone: +1-212-555-0288 / Email: mtorres@morrisonblake.com\n\n"
        "Legal Counsel to the Lead Investor:\n\n"
        "  Fenwick & West LLP\n"
        "  Attn: David Park, Esq.\n"
        "  801 California Street, Mountain View, CA 94041\n"
        "  Phone: +1-650-555-0345 / Email: dpark@fenwick.com"
    ))

    out = output_dir / "contract_en.pdf"
    pdf.output(str(out))
    print(f"  Created {out}")


# ── Russian (Commercial Lease Agreement) ──────────────────────────────────


def generate_russian_contract(output_dir: Path) -> None:
    pdf = _make_pdf()
    pdf.add_page()

    _title(pdf, "Договор аренды нежилого помещения")
    _subtitle(pdf, "№ АР-2024/03-0892")

    _body(pdf, (
        "г. Москва                                                      "
        "15 марта 2024 года"
    ))
    _body(pdf, (
        "Общество с ограниченной ответственностью «Цифровые Горизонты» "
        "(далее — «Арендодатель»), в лице генерального директора "
        "Иванова Ивана Ивановича, действующего на основании Устава, с одной стороны, и "
        "индивидуальный предприниматель Петрова Мария Сергеевна "
        "(далее — «Арендатор»), с другой стороны, "
        "совместно именуемые «Стороны», заключили настоящий Договор о нижеследующем:"
    ))

    # ── 1. Стороны ──
    _heading(pdf, "1. Реквизиты Сторон")

    _subheading(pdf, "1.1 Арендодатель")
    _body(pdf, (
        "Полное наименование: ООО «Цифровые Горизонты»\n"
        "ИНН: 7707123456\n"
        "КПП: 770701001\n"
        "ОГРН: 1027700123456\n"
        "Юридический адрес: 125009, г. Москва, ул. Тверская, д. 15, стр. 2, офис 401\n"
        "Фактический адрес: 125009, г. Москва, ул. Тверская, д. 15, стр. 2, офис 401\n"
        "Генеральный директор: Иванов Иван Иванович\n"
        "Паспорт: серия 4510 номер 123456, выдан ОВД «Тверской» г. Москвы 15.06.2010\n"
        "Телефон: +7 (495) 123-45-67\n"
        "Электронная почта: ivanov@dighoriz.ru\n\n"
        "Банковские реквизиты:\n"
        "  Банк: ПАО «Сбербанк»\n"
        "  Р/с: 40702810938000012345\n"
        "  К/с: 30101810400000000225\n"
        "  БИК: 044525225"
    ))

    _subheading(pdf, "1.2 Арендатор")
    _body(pdf, (
        "ФИО: Петрова Мария Сергеевна\n"
        "Статус: Индивидуальный предприниматель\n"
        "ИНН: 771234567890\n"
        "ОГРНИП: 318774600123456\n"
        "Паспорт: серия 4512 номер 654321, выдан УФМС России по г. Москве "
        "по району Хамовники 22.09.2015\n"
        "Дата рождения: 14.08.1988\n"
        "Адрес регистрации: 119435, г. Москва, Ленинский проспект, д. 28, кв. 105\n"
        "Телефон: +7 (495) 987-65-43\n"
        "Мобильный: +7 (916) 555-12-34\n"
        "Электронная почта: petrova@freelance-dev.ru\n\n"
        "Банковские реквизиты:\n"
        "  Банк: АО «Тинькофф Банк»\n"
        "  Р/с: 40802810500000567890\n"
        "  К/с: 30101810145250000974\n"
        "  БИК: 044525974"
    ))

    # ── 2. Предмет ──
    _heading(pdf, "2. Предмет Договора")
    _body(pdf, (
        "2.1 Арендодатель передаёт, а Арендатор принимает во временное "
        "владение и пользование (аренду) нежилое помещение (далее — «Помещение»), "
        "расположенное по адресу: 125009, г. Москва, ул. Тверская, д. 15, стр. 2, "
        "этаж 3, помещения №№ 301–305.\n\n"
        "2.2 Характеристики Помещения:\n"
        "  - Общая площадь: 186,4 кв. м\n"
        "  - Назначение: офисное\n"
        "  - Кадастровый номер: 77:01:0001076:2345\n"
        "  - Свидетельство о праве собственности: серия 77-АО № 567890, "
        "выдано 12.03.2018 Управлением Росреестра по г. Москве\n\n"
        "2.3 Помещение передаётся Арендатору для использования в качестве "
        "офиса (ведение предпринимательской деятельности в сфере "
        "информационных технологий). Изменение целевого назначения "
        "допускается только с письменного согласия Арендодателя."
    ))

    # ── 3. Срок аренды ──
    _heading(pdf, "3. Срок аренды")
    _body(pdf, (
        "3.1 Настоящий Договор заключён на срок 3 (три) года: "
        "с 1 апреля 2024 года по 31 марта 2027 года.\n\n"
        "3.2 Договор подлежит государственной регистрации в Управлении "
        "Росреестра по г. Москве в течение 30 (тридцати) календарных дней "
        "с момента подписания.\n\n"
        "3.3 Арендатор имеет преимущественное право на заключение договора "
        "аренды на новый срок при условии надлежащего исполнения обязательств "
        "по настоящему Договору. О намерении продлить аренду Арендатор обязан "
        "уведомить Арендодателя не позднее чем за 90 (девяносто) календарных "
        "дней до истечения срока Договора."
    ))

    # ── 4. Арендная плата ──
    _heading(pdf, "4. Арендная плата и порядок расчётов")
    _body(pdf, (
        "4.1 Ежемесячная арендная плата составляет 420 000 (четыреста двадцать "
        "тысяч) рублей 00 копеек, НДС не облагается (Арендодатель применяет "
        "упрощённую систему налогообложения).\n\n"
        "4.2 Арендная плата включает:\n"
        "  - пользование Помещением;\n"
        "  - эксплуатационные расходы (уборка мест общего пользования, "
        "охрана здания, обслуживание лифтов).\n\n"
        "4.3 Коммунальные платежи (электроэнергия, водоснабжение, отопление, "
        "интернет) оплачиваются Арендатором отдельно по показаниям приборов "
        "учёта на основании выставленных счетов.\n\n"
        "4.4 Арендная плата вносится ежемесячно не позднее 5 (пятого) числа "
        "оплачиваемого месяца путём безналичного перевода на расчётный счёт "
        "Арендодателя.\n\n"
        "4.5 Обеспечительный платёж: при подписании настоящего Договора "
        "Арендатор вносит обеспечительный платёж в размере двухмесячной "
        "арендной платы — 840 000 (восемьсот сорок тысяч) рублей. "
        "Обеспечительный платёж возвращается Арендатору в течение 10 (десяти) "
        "рабочих дней после прекращения Договора и подписания акта "
        "возврата Помещения при условии отсутствия задолженности.\n\n"
        "4.6 Арендодатель вправе пересматривать размер арендной платы "
        "не чаще одного раза в 12 (двенадцать) месяцев. Увеличение не может "
        "превышать 7% от текущей ставки. Арендодатель обязан уведомить "
        "Арендатора о повышении не позднее чем за 60 (шестьдесят) "
        "календарных дней.\n\n"
        "4.7 В случае просрочки арендной платы Арендатор уплачивает "
        "неустойку в размере 0,1% от суммы задолженности за каждый "
        "день просрочки."
    ))

    # ── 5. Передача и возврат ──
    _heading(pdf, "5. Передача и возврат Помещения")
    _body(pdf, (
        "5.1 Помещение передаётся Арендатору по акту приёма-передачи "
        "(Приложение №1) не позднее 1 апреля 2024 года. В акте фиксируется "
        "техническое состояние Помещения, показания приборов учёта, "
        "перечень переданных ключей и пропусков.\n\n"
        "5.2 При прекращении Договора Арендатор обязан возвратить Помещение "
        "Арендодателю по акту возврата в состоянии не хуже, чем на момент "
        "приёма, с учётом нормального износа.\n\n"
        "5.3 Арендатор обязан освободить Помещение и передать его "
        "в течение 5 (пяти) рабочих дней с даты прекращения Договора."
    ))

    # ── 6. Права и обязанности ──
    _heading(pdf, "6. Права и обязанности Сторон")
    _body(pdf, (
        "6.1 Арендодатель обязан:\n"
        "  а) передать Помещение в состоянии, пригодном для офисного "
        "использования;\n"
        "  б) обеспечить беспрепятственный доступ Арендатора и его "
        "сотрудников в Помещение в рабочие дни с 07:00 до 23:00, "
        "в выходные и праздничные дни — по пропускам;\n"
        "  в) производить капитальный ремонт здания за свой счёт;\n"
        "  г) не позднее чем за 30 дней уведомлять Арендатора "
        "о проведении плановых работ, затрагивающих Помещение.\n\n"
        "6.2 Арендатор обязан:\n"
        "  а) использовать Помещение исключительно по назначению, "
        "указанному в п. 2.3;\n"
        "  б) своевременно и в полном объёме вносить арендную плату "
        "и оплачивать коммунальные услуги;\n"
        "  в) производить текущий ремонт Помещения за свой счёт;\n"
        "  г) не производить перепланировку и реконструкцию Помещения "
        "без письменного согласия Арендодателя;\n"
        "  д) соблюдать правила пожарной безопасности и санитарные нормы;\n"
        "  е) не передавать Помещение в субаренду без письменного "
        "согласия Арендодателя;\n"
        "  ж) обеспечить допуск представителей Арендодателя для осмотра "
        "Помещения при условии предварительного уведомления "
        "не менее чем за 24 часа."
    ))

    # ── 7. Улучшения ──
    _heading(pdf, "7. Улучшения арендованного Помещения")
    _body(pdf, (
        "7.1 Отделимые улучшения, произведённые Арендатором, являются "
        "его собственностью.\n\n"
        "7.2 Неотделимые улучшения, произведённые Арендатором с письменного "
        "согласия Арендодателя, подлежат возмещению Арендодателем при "
        "прекращении Договора в размере их остаточной стоимости.\n\n"
        "7.3 Стоимость неотделимых улучшений, произведённых без письменного "
        "согласия Арендодателя, возмещению не подлежит."
    ))

    # ── 8. Конфиденциальность ──
    _heading(pdf, "8. Конфиденциальность")
    _body(pdf, (
        "8.1 Стороны обязуются не разглашать конфиденциальную информацию, "
        "ставшую известной в ходе исполнения Договора, в том числе: "
        "условия аренды, персональные данные сторон "
        "(ФИО, паспортные данные, адреса, ИНН), финансовую информацию "
        "и банковские реквизиты.\n\n"
        "8.2 Обязательства по конфиденциальности действуют в течение "
        "3 (трёх) лет после прекращения Договора.\n\n"
        "8.3 За нарушение обязательств по конфиденциальности виновная "
        "Сторона уплачивает штраф в размере 3 000 000 (три миллиона) рублей."
    ))

    # ── 9. Ответственность ──
    _heading(pdf, "9. Ответственность Сторон")
    _body(pdf, (
        "9.1 За неисполнение или ненадлежащее исполнение обязательств по "
        "настоящему Договору Стороны несут ответственность в соответствии "
        "с действующим законодательством Российской Федерации.\n\n"
        "9.2 Арендодатель не несёт ответственности за сохранность имущества "
        "Арендатора, находящегося в Помещении, за исключением случаев, "
        "когда утрата или повреждение произошли по вине Арендодателя.\n\n"
        "9.3 Стороны освобождаются от ответственности за неисполнение "
        "обязательств, вызванное обстоятельствами непреодолимой силы "
        "(форс-мажор), при условии незамедлительного уведомления "
        "другой Стороны и предоставления подтверждающих документов."
    ))

    # ── 10. Расторжение ──
    _heading(pdf, "10. Порядок расторжения Договора")
    _body(pdf, (
        "10.1 Каждая Сторона вправе расторгнуть Договор в одностороннем порядке, "
        "направив письменное уведомление другой Стороне не менее чем за "
        "90 (девяносто) календарных дней.\n\n"
        "10.2 Арендодатель вправе потребовать досрочного расторжения "
        "Договора в случае:\n"
        "  а) просрочки арендной платы более чем на 30 (тридцать) "
        "календарных дней;\n"
        "  б) использования Помещения не по назначению;\n"
        "  в) существенного ухудшения состояния Помещения.\n\n"
        "10.3 При досрочном расторжении по инициативе Арендатора без "
        "нарушений со стороны Арендодателя обеспечительный платёж "
        "удерживается Арендодателем в качестве компенсации."
    ))

    # ── 11. Разрешение споров ──
    _heading(pdf, "11. Разрешение споров")
    _body(pdf, (
        "11.1 Все споры и разногласия, возникающие в связи с настоящим Договором, "
        "Стороны будут стремиться урегулировать путём переговоров.\n\n"
        "11.2 При невозможности достижения согласия спор передаётся "
        "на рассмотрение в Арбитражный суд города Москвы."
    ))

    # ── 12. Заключительные ──
    _heading(pdf, "12. Заключительные положения")
    _body(pdf, (
        "12.1 Настоящий Договор вступает в силу с момента государственной "
        "регистрации и действует до 31 марта 2027 года.\n\n"
        "12.2 Все изменения и дополнения к Договору оформляются "
        "дополнительными соглашениями, подписанными обеими Сторонами "
        "и подлежащими государственной регистрации.\n\n"
        "12.3 Настоящий Договор составлен в трёх экземплярах, "
        "имеющих одинаковую юридическую силу: по одному для каждой "
        "из Сторон и один для органа регистрации.\n\n"
        "12.4 Приложения, являющиеся неотъемлемой частью Договора:\n"
        "  - Приложение №1: Акт приёма-передачи Помещения\n"
        "  - Приложение №2: Поэтажный план с указанием Помещения\n"
        "  - Приложение №3: Копия свидетельства о праве собственности"
    ))

    # ── Подписи ──
    _body(pdf, "\n")
    _heading(pdf, "Подписи Сторон")
    _body(pdf, (
        "АРЕНДОДАТЕЛЬ:\n"
        "ООО «Цифровые Горизонты»\n\n"
        "Генеральный директор\n\n"
        "__________________ / Иванов И.И. /\n"
        "                          М.П.\n\n"
        "Паспорт: 4510 123456\n"
        "ИНН: 7707123456\n"
        "Дата: 15 марта 2024 г.\n\n\n"
        "АРЕНДАТОР:\n"
        "ИП Петрова Мария Сергеевна\n\n"
        "__________________ / Петрова М.С. /\n\n"
        "Паспорт: 4512 654321\n"
        "ИНН: 771234567890\n"
        "Дата: 15 марта 2024 г."
    ))

    # ── Приложение ──
    pdf.add_page()
    _heading(pdf, "Приложение: Контактные лица и экстренные контакты")
    _body(pdf, (
        "Со стороны Арендодателя:\n\n"
        "  1. Генеральный директор: Иванов Иван Иванович\n"
        "     Телефон: +7 (495) 123-45-67\n"
        "     Мобильный: +7 (903) 111-22-33\n"
        "     Email: ivanov@dighoriz.ru\n\n"
        "  2. Управляющий зданием: Сидоров Алексей Петрович\n"
        "     Телефон: +7 (495) 123-45-89\n"
        "     Мобильный: +7 (903) 222-33-44\n"
        "     Email: sidorov@dighoriz.ru\n\n"
        "  3. Инженер по эксплуатации: Козлов Дмитрий Андреевич\n"
        "     Мобильный: +7 (916) 333-44-55\n"
        "     Email: kozlov@dighoriz.ru\n\n"
        "  4. Юридический отдел: Волкова Елена Николаевна\n"
        "     Телефон: +7 (495) 123-45-90\n"
        "     Email: volkova@dighoriz.ru\n\n"
        "  5. Бухгалтерия: Новикова Татьяна Владимировна\n"
        "     Телефон: +7 (495) 123-45-92\n"
        "     Email: novikova@dighoriz.ru\n\n"
        "Со стороны Арендатора:\n\n"
        "  1. Петрова Мария Сергеевна\n"
        "     Мобильный: +7 (916) 555-12-34\n"
        "     Email: petrova@freelance-dev.ru\n"
        "     Экстренный контакт: Петров Сергей Анатольевич (супруг)\n"
        "     Телефон: +7 (916) 666-78-90"
    ))

    out = output_dir / "contract_ru.pdf"
    pdf.output(str(out))
    print(f"  Created {out}")


# ── Main ────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(exist_ok=True)
    print("Generating sample contracts...")
    generate_korean_contract(OUTPUT_DIR)
    generate_english_contract(OUTPUT_DIR)
    generate_russian_contract(OUTPUT_DIR)
    print("Done.")
