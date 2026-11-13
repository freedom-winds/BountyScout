# Bug Bounty Program Documentation

## Overview

The Comeback Bug Bounty Program rewards security researchers and developers who help us identify and fix security vulnerabilities and critical bugs in our codebase.

## Program Types

### 1. Security Bounty Program

Focused on identifying security vulnerabilities that could compromise:
- User data and privacy
- System integrity
- Authentication and authorization
- Data confidentiality

See [SECURITY.md](../SECURITY.md) for full details.

### 2. Developer Bounty Program

Rewards for:
- Critical bug fixes
- Performance improvements
- Feature implementations
- Documentation improvements
- Test coverage enhancements

## Eligibility

### Who Can Participate?

- Security researchers
- Independent developers
- Open source contributors
- Anyone who finds a valid issue

### Exclusions

- Current team members and contractors
- Family members of team members
- Issues found during paid security audits

## Submission Process

### For Security Issues

1. **Report privately** via GitHub Security Advisories or security@comeback.dev
2. **Wait for confirmation** (48 hours)
3. **Collaborate on fix** if requested
4. **Receive reward** after fix is deployed

### For Development Bounties

1. **Check existing issues** labeled `bounty` or `good-first-issue`
2. **Comment on the issue** to claim it
3. **Submit a PR** following our contribution guidelines
4. **Pass code review** and CI checks
5. **Receive reward** after merge

## Reward Structure

### Security Bounties

| Severity | Reward Range | Examples |
|----------|--------------|----------|
| Critical | $500 - $2,000 | RCE, Auth bypass, Data breach |
| High | $200 - $500 | XSS, CSRF, Injection attacks |
| Medium | $50 - $200 | Info disclosure, DoS |
| Low | $10 - $50 | Security misconfigurations |

### Development Bounties

| Type | Reward Range | Examples |
|------|--------------|----------|
| Critical Bug | $100 - $500 | Data loss, System crash |
| Feature | $50 - $300 | New functionality |
| Enhancement | $20 - $100 | Performance, UX improvements |
| Documentation | $10 - $50 | Guides, API docs |
| Tests | $10 - $50 | Unit, integration tests |

### Bonus Multipliers

- **First reporter**: 1.5x
- **Includes fix**: 1.3x
- **Includes tests**: 1.2x
- **Excellent documentation**: 1.2x

Multipliers stack (max 2.5x total).

## Payment Methods

- PayPal
- Bank transfer (for amounts > $100)
- Cryptocurrency (BTC, ETH, USDC)
- GitHub Sponsors
- Open Collective

## Evaluation Criteria

### Security Issues

1. **Severity**: Impact and exploitability
2. **Quality**: Clarity of report and reproduction steps
3. **Novelty**: Previously unknown vs. duplicate
4. **Scope**: Within program boundaries

### Development Contributions

1. **Code quality**: Follows style guide, best practices
2. **Testing**: Includes appropriate tests
3. **Documentation**: Clear commit messages and docs
4. **Impact**: Value to the project
5. **Compatibility**: Follows interface compatibility rules

## Timeline

### Security Issues

- **Acknowledgment**: 48 hours
- **Initial assessment**: 7 days
- **Fix deployment**: 30-90 days (severity dependent)
- **Payment**: Within 14 days of fix deployment

### Development Bounties

- **Claim acknowledgment**: 24 hours
- **PR review**: 3-7 days
- **Payment**: Within 7 days of merge

## Rules and Guidelines

### Do's

✅ Follow responsible disclosure practices
✅ Provide detailed reproduction steps
✅ Suggest fixes when possible
✅ Respect user privacy and data
✅ Follow code style and contribution guidelines
✅ Add tests for new code
✅ Keep backward compatibility (see Interface Compatibility Rules)

### Don'ts

❌ Publicly disclose before fix is deployed
❌ Exploit vulnerabilities beyond demonstration
❌ Access or modify user data
❌ Perform DoS attacks
❌ Submit duplicate reports
❌ Break existing public APIs
❌ Leave TODO comments or placeholders

## Disqualifications

 Reports/contributions will be rejected if:

- Already known or reported
- Out of scope
- Theoretical without proof of concept
- Violates program rules
- Low quality or incomplete
- Breaks interface compatibility
- Fails CI checks

## Recognition

### Hall of Fame

Top contributors are featured in:
- Project README
- Security hall of fame page
- Annual security report
- Social media acknowledgments

### Swag

Contributors with accepted submissions receive:
- Digital badges
- Project stickers
- T-shirts (for significant contributions)

## Legal

### Safe Harbor

We will not pursue legal action against researchers who:
- Act in good faith
- Follow program guidelines
- Avoid privacy violations
- Don't disrupt services

### Terms

- Rewards are discretionary
- We reserve the right to modify the program
- Participation implies acceptance of terms
- Taxes are the responsibility of recipients
- Rewards are subject to verification

## FAQ

**Q: Can I work on multiple bounties?**
A: Yes, but claim each issue before starting.

**Q: What if someone else submits the same issue?**
A: First valid reporter receives the reward.

**Q: Can I submit issues found by automated tools?**
A: Yes, if you verify and provide context.

**Q: How long do I have to fix a claimed issue?**
A: 14 days for small issues, 30 days for larger ones. Request extensions if needed.

**Q: What if my PR is rejected?**
A: You can revise based on feedback. No reward for rejected PRs.

**Q: Can I remain anonymous?**
A: Yes, but you must provide payment details.

## Contact

- **Security issues**: security@comeback.dev
- **Development bounties**: bounty@comeback.dev
- **General questions**: GitHub Discussions
- **Program updates**: Follow [@comeback_dev](https://twitter.com/comeback_dev)

## Resources

- [SECURITY.md](../SECURITY.md) - Security policy
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) - Community standards
- [Interface Compatibility Rules](../docs/interface-compatibility.md) - API compatibility requirements

---

*Program launched: 2026-08-01*
*Last updated: 2026-08-01*
