---
name: diagram
description: Explain a PR, design decision or trade-off as a summary plus a verified HTML diagram
---
1. Briefly summarize the problem, options, and recommendation.
2. Build a single-file HTML page with an inline SVG diagram of the decision points and trade-offs.
3. Review the summary and diagram for language the intended audience can understand. Explain unfamiliar terms and abbreviations on first use.
4. Open it in terminal-browser beside the conversation. If terminal-browser is unavailable, check the page with another browser tool instead.
5. Check in front of the user that the SVG renders and no text overflows its box, gets clipped, or falls outside the viewBox. After each fix to the HTML, reload and check again. When done in terminal-browser, clear its in-use indicator.
6. Ask one question in the user’s language about whether the explanation is clear or which part to expand.
