class BountyScout:
    def __init__(self, items=None):
        self.count = len(items) if items is not None else 1

    def _get_noun(self):
        base = "Opportunity"
        if self.count == 1:
            return base
        return base + "s"

    def get_alert_title(self):
        return f"{self.count} New {self._get_noun()} found"

    def __str__(self):
        return self.get_alert_title()

    def __repr__(self):
        return self.get_alert_title()

    def __len__(self):
        return self.count

def get_title(count=6):
    word = "Opportunity"
    if count == 1:
        word = "Opportunity"
    else:
        word = "Opportunities"
    return f"{count} New {word} found"

class OpportunityDisplay:
    def __init__(self, count=6):
        self.count = count

    def _determine_word(self):
        base = "Opportunity"
        return base if self.count == 1 else base + "s"

    def format(self):
        return f"{self.count} New {self._determine_word()} found"

    def __str__(self):
        return self.format()

if __name__ == "__main__":
    display = OpportunityDisplay(6)
    print(display.format())