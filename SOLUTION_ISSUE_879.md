# Solution for Issue #879

## 🛠️ Proposed Solution (by Aditya Waghamare)

### Analysis
The `BountyDescription` component in `MergeFi/frontend` uses `react-markdown` to render issue bodies with a custom `markdownComponents` map. However, it lacks an `img` component override, causing markdown embedded screenshots (`![...](...)`) to render as unstyled, bare `<img>` tags that can overflow container bounds on narrow viewports.

### Fix
Add an `img` override to `markdownComponents` in `src/components/bounty/BountyDescription.tsx` that constrains the image width (`max-w-full`), adds rounded borders (`rounded-xl`), and maintains security and styling consistency.

### Implementation
```tsx
// In src/components/bounty/BountyDescription.tsx under markdownComponents:
img: ({ node, ...props }) => (
  // eslint-disable-next-line @next/next/no-img-element
  <img
    {...props}
    className="max-w-full rounded-xl my-4 object-contain"
    loading="lazy"
    alt={props.alt || ''}
  />
),
```

### Testing
Verify by rendering an issue containing wide markdown screenshots (`![screenshot](url)`) within `BountyDescription` on mobile and desktop viewports to ensure proper containment without layout overflow.

---
*Submitted by Aditya Waghamare*
💰 **Payout Address (Base L2 / EVM):** `0xb61dBcdBc3407F71EaCb64D4CBFAcf9FFfe2415C`