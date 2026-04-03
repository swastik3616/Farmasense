---
title: "CI Failure in branch ${{ github.ref }}"
labels: [ "bug", "automated-ci" ]
assignees: [ "${{ github.actor }}" ]
---

### ⚠️ Backend CI Failure Detailed Report

The automated test suite failed on branch **${{ github.ref }}**.

**Commit:** [${{ github.sha }}](https://github.com/${{ github.repository }}/commit/${{ github.sha }})
**Actor:** ${{ github.actor }}
**Workflow Run:** [View Logs](https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }})

Please investigate the following:
- [ ] Review test coverage (target is 70%).
- [ ] Check for runtime errors in backend logs.
- [ ] Verify environment variables.
