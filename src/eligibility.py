from __future__ import annotations
from dataclasses import dataclass

@dataclass
class EligibilityResult:
    status: str
    reasons: list[str]
    checks: list[tuple[str, str]]


def check_pm_kisan_demo(answers: dict) -> EligibilityResult:
    """Demo rules based on PM-KISAN guideline exclusions.
    This is an educational classifier, not an official eligibility decision.
    """
    reasons = []
    checks = []
    ok = True

    landholder = answers.get("landholder", False)
    institutional_land = answers.get("institutional_land", False)
    constitutional = answers.get("constitutional_or_elected", False)
    govt_employee = answers.get("govt_employee", False)
    income_tax = answers.get("income_tax", False)
    professional = answers.get("professional_body", False)

    checks.append(("Landholding farmer family", "PASS" if landholder else "FAIL"))
    if not landholder:
        ok = False
        reasons.append("The demo requires the applicant to be a landholding farmer family under the scheme description.")

    checks.append(("Institutional land holder", "FAIL" if institutional_land else "PASS"))
    if institutional_land:
        ok = False
        reasons.append("Institutional land holders are listed among exclusions.")

    checks.append(("Constitutional/elected office category", "FAIL" if constitutional else "PASS"))
    if constitutional:
        ok = False
        reasons.append("Certain constitutional/elected office holders and related categories are excluded.")

    checks.append(("Serving/retired government employee category", "FAIL" if govt_employee else "PASS"))
    if govt_employee:
        ok = False
        reasons.append("Certain serving or retired government employee categories are excluded.")

    checks.append(("Income tax payer", "FAIL" if income_tax else "PASS"))
    if income_tax:
        ok = False
        reasons.append("Certain income-tax payer categories are excluded.")

    checks.append(("Registered practicing professional", "FAIL" if professional else "PASS"))
    if professional:
        ok = False
        reasons.append("Certain practicing professionals registered with professional bodies are excluded.")

    if ok:
        return EligibilityResult("Likely eligible based on demo rules", reasons, checks)
    return EligibilityResult("Potentially ineligible based on demo rules", reasons, checks)
