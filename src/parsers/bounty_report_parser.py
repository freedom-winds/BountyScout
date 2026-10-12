import re
from typing import List, Dict
from datetime import datetime

class BountyReportParser:
    """
    Parser especializado para converter relatórios de scan de bounties 
    em objetos estruturados para o BountyScout.
    """

    def __init__(self):
        self.pattern_issue = re.compile(
            r"#### \d\. \[(?P<title>.*?)\]\((?P<url>.*?)\)\n"
            r"- \*\*Repository:\*\* \[(?P<repo_name>.*?)\]\(? (?P<repo_url>.*?)\)?\n"
            r"- \*\*Comments:\*\* (?P<comments>\d+)\n"
            r"- \*\*Last Updated:\*\* (?P<last_updated>.*)",
            re.MULTILINE
        )

    def parse(self, raw_text: str) -> List[Dict]:
        opportunities = []
        matches = self.pattern_issue.finditer(raw_text)

        for match in matches:
            data = match.groupdict()
            opportunities.append({
                "title": data["title"],
                "issue_url": data["url"],
                "repository_name": data["repo_name"],
                "repository_url": data["repo_url"].strip(),
                "comments_count": int(data["comments"]),
                "last_updated": self._parse_date(data["last_updated"]),
                "scanned_at": datetime.utcnow().isoformat() + "Z"
            })
        
        return opportunities

    def _parse_date(self, date_str: str) -> str:
        try:
            # Formato esperado: 2026-10-12T07:11:40Z
            return date_str.strip()
        except Exception:
            return datetime.utcnow().isoformat() + "Z"

if __name__ == "__main__":
    # Teste rápido com o conteúdo da issue
    sample_text = """
    #### 1. [📋 2026-10-12 本週補助／競賽機會更新](https://github.com/fishtvlvoe/ai-apply-skill/issues/22)
    - **Repository:** [fishtvlvoe/ai-apply-skill](https://github.com/fishtvlvoe/ai-apply-skill)
    - **Comments:** 0
    - **Last Updated:** 2026-10-12T07:11:40Z
    """
    parser = BountyReportParser()
    print(parser.parse(sample_text))
