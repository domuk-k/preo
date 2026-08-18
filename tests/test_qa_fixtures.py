"""셀프 QA 픽스처와 A칸 계약을 잠근다. 점수는 만들지 않는다."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = ROOT / "skills" / "preo" / "SKILL.md"
RULES_YAML = ROOT / "standard" / "rules" / "candidates.yaml"
K8S_EXCERPT = ROOT / "docs" / "pilot" / "fixtures" / "k8s-kubeadm-install.excerpt.md"
K8S_INSPECT = ROOT / "docs" / "pilot" / "2026-08-preo-k8s-kubeadm-inspect.md"
FASTAPI_EXCERPT = (
    ROOT / "docs" / "pilot" / "fixtures" / "fastapi-first-steps.excerpt.md"
)
FASTAPI_INSPECT = (
    ROOT / "docs" / "pilot" / "2026-08-preo-fastapi-first-steps-inspect.md"
)

BYTE_LOCK_TOKENS = (
    "sudo swapoff -a",
    "sudo apt-get install -y kubelet kubeadm kubectl",
    "https://pkgs.k8s.io/core:/stable:/v1.36/deb/Release.key",
    "2GB",
    "2개",
)


def test_k8s_excerpt_is_attributed_and_covers_procedure_warning() -> None:
    text = K8S_EXCERPT.read_text(encoding="utf-8")
    assert "kubernetes.io/ko/docs/setup/production-environment/tools/kubeadm/install-kubeadm" in text
    assert "CC BY 4.0" in text
    assert "#### 경고" in text
    assert "```shell" in text
    for token in BYTE_LOCK_TOKENS:
        assert token in text, token


def test_fastapi_excerpt_is_attributed_and_locks_urls() -> None:
    text = FASTAPI_EXCERPT.read_text(encoding="utf-8")
    assert "fastapi.tiangolo.com/ko/tutorial/first-steps" in text
    assert "AI와 사람이 함께한 번역" in text
    for token in (
        "fastapi dev",
        "http://127.0.0.1:8000",
        "main.py",
        '{"message": "Hello World"}',
    ):
        assert token in text, token


def test_fastapi_inspect_report_is_inspect_only() -> None:
    text = FASTAPI_INSPECT.read_text(encoding="utf-8")
    assert "fastapi.tiangolo.com/ko/tutorial/first-steps" in text
    assert "검사만" in text
    assert "품질 점수 없음" in text
    assert "| A1 | 예 |" in text
    assert "KSTL-SYN-002" in text
    assert not any(token in text for token in ("82점", "Flesch", "COMET"))


def test_skill_inspect_contract_locks_a_cells() -> None:
    skill = SKILL_MD.read_text(encoding="utf-8")
    inspect = skill.split("## 검사만", 1)[1].split("## 쓰기", 1)[0]
    assert "고치지 않는다" in inspect
    assert "통과 또는 실패" in inspect
    assert "Accuracy" in inspect
    assert "뜻 유지" in skill
    assert "이미 읽힘" in skill
    assert "출력 형식에 그 칸이 없다" in skill
    assert "BLEU" in skill
    assert "byte 단위로 둔다" in skill


def test_k8s_inspect_report_is_inspect_only() -> None:
    text = K8S_INSPECT.read_text(encoding="utf-8")
    assert "kubernetes.io/ko/docs/setup/production-environment/tools/kubeadm/install-kubeadm" in text
    assert "검사만" in text
    assert "품질 점수 없음" in text
    assert "가독성" not in text.replace("가독성 점수", "")
    assert not any(token in text for token in ("82점", "Flesch", "COMET"))
    assert "| A1 | 예 |" in text
    assert "KSTL-SAF-001" in text
    assert "KSTL-DOC-001" in text


def test_k8s_inspect_does_not_autofail_synonym_or_nonsafety_admonition() -> None:
    text = K8S_INSPECT.read_text(encoding="utf-8")
    assert "KSTL-DOC-001, KSTL-TER-001" not in text
    assert "KSTL-SAF-001, KSTL-SYN-002" not in text
    assert "- KSTL-SAF-001 ×" not in text
    assert "불명" in text and "TER-001" in text
    assert "패키지" in text
    assert "비적용" in text or "안전 위험" in text


def test_every_rule_has_example_pair_and_invariant() -> None:
    rules = yaml.safe_load(RULES_YAML.read_text(encoding="utf-8"))
    assert len(rules) == 16
    for rule in rules:
        assert rule["unapproved_examples"], rule["id"]
        assert rule["approved_examples"], rule["id"]
        assert rule["example_invariants"], rule["id"]
