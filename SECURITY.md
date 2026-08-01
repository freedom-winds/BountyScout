# Security Policy

## Bug Bounty Program

We take the security of our project seriously. To encourage responsible disclosure of security vulnerabilities, we have established a bug bounty program.

### Scope

The following are in scope for our bug bounty program:

- **Critical vulnerabilities**: Remote code execution, authentication bypass, privilege escalation
- **High severity issues**: SQL injection, XSS, CSRF, insecure direct object references
- **Medium severity issues**: Information disclosure, denial of service, security misconfigurations
- **Low severity issues**: Best practice violations with security implications

### Out of Scope

- Issues in third-party dependencies (please report directly to the maintainers)
- Social engineering attacks
- Physical attacks
- Denial of service attacks that require excessive resources
- Issues already known or documented

### Rewards

Reward amounts are determined based on severity and impact:

- **Critical**: $500 - $2,000
- **High**: $200 - $500
- **Medium**: $50 - $200
- **Low**: $10 - $50

Rewards are paid in USD or cryptocurrency equivalent at the researcher's preference.

### Reporting a Vulnerability

To report a security vulnerability:

1. **Email**: Send details to security@comeback.dev (or create a private security advisory on GitHub)
2. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)
   - Your contact information for follow-up

3. **Response timeline**:
   - Initial response: Within 48 hours
   - Status update: Within 7 days
   - Resolution target: 30-90 days depending on severity

### Responsible Disclosure Guidelines

- Give us reasonable time to fix the issue before public disclosure
- Do not exploit the vulnerability beyond what is necessary to demonstrate it
- Do not access, modify, or delete data belonging to others
- Do not perform actions that could harm the availability of our services
- Act in good faith and avoid privacy violations

### Safe Harbor

We will not pursue legal action against researchers who:

- Follow these guidelines
- Report vulnerabilities in good faith
- Avoid privacy violations and service disruption
- Make a good faith effort to comply with this policy

### Recognition

With your permission, we will:

- Acknowledge your contribution in our security hall of fame
- Credit you in release notes when the fix is published
- Provide a reference letter upon request

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Security Best Practices

For users and contributors:

- Keep dependencies up to date
- Use strong authentication mechanisms
- Follow the principle of least privilege
- Validate and sanitize all inputs
- Use parameterized queries to prevent injection attacks
- Enable security headers and HTTPS
- Regularly review access logs

## Contact

For security-related questions or concerns:

- **Email**: security@comeback.dev
- **PGP Key**: [Link to public key if available]
- **GitHub Security Advisories**: [Private vulnerability reporting](https://github.com/Oliversmoke/comeback/security/advisories/new)

---

*Last updated: 2026-08-01*
