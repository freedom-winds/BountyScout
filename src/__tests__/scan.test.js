const scan = require('../scan');

describe('Bounty Scanner', () => {
  test('should filter bounty issues correctly', () => {
    const mockIssues = [
      { title: 'Bounty: Add tests', comments: 2, updated_at: '2026-10-09T02:44:32Z', html_url: 'url1' },
      { title: 'Regular issue', comments: 0, updated_at: '2026-10-09T02:44:32Z', html_url: 'url2' },
      { title: 'BOUNTY-002: Fix bug', comments: 8, updated_at: '2026-10-09T02:38:55Z', html_url: 'url3' }
    ];

    const result = scan.filterBountyIssues(mockIssues);
    expect(result).toHaveLength(2);
    expect(result[0].title).toBe('Bounty: Add tests');
    expect(result[1].title).toBe('BOUNTY-002: Fix bug');
  });

  test('should generate markdown report correctly', () => {
    const mockResults = {
      scanTime: '2026-10-09T02:46:00Z',
      report: [
        {
          title: 'Test Bounty',
          url: 'https://github.com/test/repo/issues/1',
          repo: 'test/repo',
          comments: 5,
          updated: '2026-10-09T02:44:32Z'
        }
      ]
    };

    const markdown = scan.generateMarkdownReport(mockResults);
    expect(markdown).toContain('### Active Bounty Scan Results');
    expect(markdown).toContain('Test Bounty');
    expect(markdown).toContain('test/repo');
  });
});
