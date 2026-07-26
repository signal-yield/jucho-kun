# Changelog

All notable changes to jucho-kun are documented in this file.

## [1.1.0] - 2026-07-25

### Fixed

- **Identity**: `plugin.json` / `marketplace.json` author and owner contact info, and the
  buggy `marketplace.json` `plugins[0].source.repo` (previously pointed at the retired
  `pinotan2024-coder/jucho-kun` repo, so adding this Marketplace installed the old repo's
  plugin instead of this one), now point to `signal-yield/jucho-kun`. `LICENSE` copyright
  holder updated accordingly. Two GitHub links in `docs/index.html` corrected.
- **Distribution**: README "How to Install" rewritten from a non-functional
  Releases/`.skill` manual-download flow (Releases had zero entries; this repo is
  plugin-structured and never produced a `.skill` bundle) to the Marketplace flow
  (`/plugin marketplace add` → `/plugin install jucho-kun@signal-yield-advisory`).
  A matching 3-step install block was added to `docs/index.html`.
- **Hazard-check reliability**: SKILL.md no longer instructs writing "確認済み旨を記入"
  for hazard-map results without actually reading the map. A single, explicit definition
  of "★確認済" (site-level result transcribed with confirmation date and source URL) now
  governs when a result may be marked confirmed; items that don't meet it are marked
  "□要確認" with only a reference URL.
- **Feature-status accuracy**: README's feature table no longer claims automated
  municipal-data fetching (✅) for a step that only locates and cites portal URLs; marked
  partial (◐) instead. Added the previously-missing ④ (soil/groundwater contamination
  screening, already implemented) row so the table maps 1:1 to SKILL.md's ①–⑤.
- **Intake flow**: SKILL.md now defines the question order (address → transaction type →
  use type → condominium unit or not) and states that already-provided items are not
  re-asked, covering the previously unspecified "重説調査して" bare-trigger case.
- **Legal terminology**: "瑕疵担保" (superseded by the 2020 Civil Code revision) replaced
  with "契約不適合責任" throughout.
- **Lease coverage**: the 取引条件 (transaction terms) checklist category now branches by
  sale vs. lease; added lease-specific items (contract term/renewal and fixed-term lease
  disclosure, deposit settlement and restoration standards, sublease/use-change and
  prohibited-use clauses, rent payment and move-out conditions).
- **Condominium checklist**: added land-rights type (ownership vs. leasehold, and whether
  site-use rights can be transferred separately from the unit) and exclusive-use rights
  (parking, private garden, roof balcony, etc.) to the condominium-specific item list.
- **Overclaiming**: README's example output no longer states "No risk" for tsunami/storm
  surge, which contradicted the disclaimer that this is a first-pass screening tool;
  changed to "Outside designated hazard zone".
- **Install failure with no SSH configured**: `claude plugin install jucho-kun@signal-yield-advisory`
  failed with a strict SSH host-key verification error
  (`No ED25519 host key is known for github.com`) on any machine without SSH keys /
  `known_hosts` configured for GitHub. Root cause: `marketplace.json`'s
  `plugins[0].source` used the object/GitHub-repo format
  (`{"source": "github", "repo": "..."}`), which `claude plugin install` resolves via
  an SSH clone attempt with no HTTPS fallback (unlike `claude plugin marketplace add`,
  which does fall back to HTTPS). Since the marketplace and its only plugin are the
  same repository, changed `plugins[0].source` to `"./"` instead, which reuses the
  marketplace's already-HTTPS-cloned checkout. Verified end-to-end in a clean,
  SSH-less environment after the fix.

### Added

- `canonical` and `og:url` tags in `docs/index.html`. `og:image` intentionally not added —
  no image asset exists in this repository yet.
- `.github/workflows/link-check.yml`: monthly link check across `.md`/`.html` files,
  opening a GitHub Issue when broken links are found (currently landed with the
  schedule trigger and Issue-creation step disabled pending review of an initial run).

### Changed

- Enabled GitHub Pages (`main` / `docs`) for `signal-yield/jucho-kun`
  (`https://signal-yield.github.io/jucho-kun/`) and migrated README's official-site
  links there from the retired repo's Pages site.

### Notes

- No changes were made to `pinotan2024-coder/jucho-kun` (the original repo, kept for
  press/announcement consistency) or to any local out-of-repo skill installation.
