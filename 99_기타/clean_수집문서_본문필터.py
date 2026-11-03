"""수집 문서에서 본문이 아닌 문단(메뉴·구독 안내·저작권·사진 캡션 등)을 걸러낸다.

입력: collected_live.json (all_documents[].paragraphs[])
출력: {"documents": [{doc_id, country, language, title, source_name, credibility_weight, tier,
                      paragraphs: [{paragraph_id, text}]}], "dropped": {...}}

    python clean.py collected_live.json -o cleaned.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter

# 어느 언어든 이 패턴이 들어가면 본문이 아님
DROP_PATTERNS = [
    # 공통: 링크·메뉴·SNS·저작권
    r"^\[.*\]\(.*\)\s*$", r"_?메뉴 열기/닫기_?", r"열기/닫기", r"^#+\s*\[", r"https?://\S+\)?\s*$",
    r"©|ⓒ|copyright", r"[\w.]+@[\w.]+\.\w+", r"^\*\s{2,}第",
    # 한국어 기사 부속
    r"^송고", r"송고\s*\d{4}", r"재판매 및 DB\s*금지", r"제보는 카카오톡", r"후원링크", r"함께 (볼만한|보면 좋은|읽기 좋은)",
    r"연합뉴스를 만나보세요", r"세 줄 요약", r"기사 본문과 함께 읽어야", r"구글 검색에서", r"글자 크기", r"좋아요\s+슬퍼요",
    r"^폰트 \d단계", r"카카오톡\s+페이스북", r"에디터스 픽", r"Family site", r"마이뉴스", r"원스톱 콘텐츠",
    r"통합 검색", r"^\*\*\[.*\]\(.*\)\s*기자\*\*$", r"전체메뉴", r"\]\(", r"防衛白書トップ", r"\{\{.*\}\}",
    # 중국어 기사 부속
    r"^来源[：:]", r"责任编辑", r"摄\s*$", r"扫一扫", r"点击底部", r"未经本网", r"【纠错】", r"^\[新华网\]",
    r"^\*?\d{4}\*?\s*\*?\d{2}\*?/", r"^\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}",
    # 일본어 백서 목차·사진 설명
    r"^\*\s+第[IVX\d]+部", r"^\*\s+第\d+(章|節)", r"防衛省・自衛隊のホーム", r"^\]\(", r"^参照\s*図表", r"^資料[：:]",
    # 영어 사이트 부속
    r"subscri", r"log ?in\b", r"logout", r"sign up", r"premium (article|stories)", r"e-books library", r"webinar",
    r"support our reporting", r"read unlimited", r"last free article", r"news app", r"related topics", r"photo credit",
    r"^(updated|published)\s*-", r"published in dawn", r"allow notifications", r"recipient email", r"account settings",
    r"keyboard shortcuts?", r"volume\s*\d+%", r"^(play/pause|increase|decrease|captions|fullscreen|shortcuts)",
    r"^#####\s", r"offer (is )?only for", r"discounted access", r"unlock them all", r"products you've access",
]
DROP_RE = re.compile("|".join(DROP_PATTERNS), re.IGNORECASE)

# 언어별 최소 길이 (한·중·일은 글자당 정보량이 많아 기준을 낮춤)
MIN_LEN = {"zh": 12, "ja": 15, "ko": 20, "en": 40}

MD_RE = re.compile(r"[*_#>`]+|\[([^\]]*)\]\([^)]*\)")


def strip_markdown(text: str) -> str:
    text = MD_RE.sub(lambda m: m.group(1) or "", text)
    return re.sub(r"\s+", " ", text).strip()


def is_body(text: str, lang: str) -> tuple[bool, str]:
    """(본문인지, 버린 이유)"""
    if DROP_RE.search(text):
        return False, "pattern"
    plain = strip_markdown(text)
    if len(plain) < MIN_LEN.get(lang, 20):
        return False, "short"
    # 영어: 문장부호로 끝나지 않는 짧은 줄은 대부분 추천 기사 제목·사이드바
    if lang == "en" and len(plain) < 100 and not re.search(r"[.!?\"”’)]$", plain):
        return False, "headline"
    return True, ""


def clean(data: dict) -> dict:
    out_docs, dropped = [], Counter()
    for doc in data["all_documents"]:
        lang = doc.get("language", "en")
        seen, paras = set(), []
        for p in doc.get("paragraphs", []):
            raw = p.get("text") or p.get("raw_text") or ""
            ok, why = is_body(raw, lang)
            text = strip_markdown(raw)
            if ok and text in seen:
                ok, why = False, "duplicate"
            if not ok:
                dropped[why] += 1
                continue
            seen.add(text)
            paras.append({"paragraph_id": p.get("paragraph_id") or p.get("id"), "text": text})
        out_docs.append({
            "doc_id": doc["doc_id"],
            "country": doc.get("country"),
            "language": lang,
            "title": strip_markdown(doc.get("title", "")),
            "url": doc.get("url"),
            "source_name": doc.get("source_name"),
            "credibility_weight": doc.get("credibility_weight"),
            "tier": doc.get("tier"),
            "paragraphs": paras,
        })
    return {"question": data.get("korean_question"), "documents": out_docs, "dropped": dict(dropped)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="본문 아닌 문단 제거")
    ap.add_argument("input")
    ap.add_argument("-o", "--output", default="cleaned.json")
    args = ap.parse_args(argv)
    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)
    result = clean(data)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    kept = sum(len(d["paragraphs"]) for d in result["documents"])
    print(f"문서 {len(result['documents'])}건, 남은 문단 {kept}개, 버린 문단 {result['dropped']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())