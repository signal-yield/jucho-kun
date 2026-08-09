# 重調クン (Jucho-kun) — Real Estate Due Diligence Plugin for ChatGPT, Codex, and Claude

> 本リポジトリは、SignalYield管理下の jucho-kun 公式コピーです。  
> 初期公開版は、過去の告知・プレス等との整合性維持のため https://github.com/pinotan2024-coder/jucho-kun に残しています。

**重調クン** is a skills-only plugin for ChatGPT, Codex, and Claude that supports the preliminary investigation phase required for preparing Japanese real estate disclosure documents (重要事項説明書 / *Jūyō Jikō Setsumeisho*, Article 35 of the Building Lots and Buildings Transaction Business Act).

What used to take a licensed appraiser or agent **1 hour of desk research** now takes a few minutes.

---

## 🌐 公式サイト・お問い合わせ / Official Website & Contact

業務での活用・組織導入支援・カスタマイズ開発のご相談は、公式サイトよりお問い合わせください。

**▶ 公式サイト**: https://signal-yield.github.io/jucho-kun/

**▶ お問い合わせフォーム**: https://forms.gle/YTzkABzQ2xEwmh917

For inquiries about business use, organizational deployment support, or custom development:
visit our [official website](https://signal-yield.github.io/jucho-kun/) or fill out the [contact form](https://forms.gle/YTzkABzQ2xEwmh917).

---

## What It Does

| Phase | Function | Status |
|-------|----------|--------|
| ① | Generate a full investigation checklist from a property address | ✅ |
| ② | Locate and cite the relevant municipal GIS / hazard portals for the address (zoning, FAR, BCR, fire zone, hazard maps) | ◐ Partial — URLs are located and cited; the skill does not fetch or auto-fill the underlying data |
| ③ | Extract key facts from PDFs (registry certificates, urban planning maps, etc.) | ✅ |
| ④ | Soil / groundwater contamination screening (designated areas, sewerage-law and water-pollution-law notified facilities, historical land-use check) | ✅ |
| ⑤ | Export a structured investigation report as `.xlsx` | ✅ |

> Not yet implemented: drafting the disclosure document text (重説文案作成), and fully automated retrieval of municipal data (the skill locates and cites the relevant portal URLs, but does not scrape or auto-fill their contents).

---

## Who It's For

- 宅地建物取引士 / Licensed Real Estate Agents (*takken-shi*)
- 不動産鑑定士 / Certified Real Estate Appraisers
- 仲介担当者 / Real Estate Brokers and Transaction Coordinators

---

## How to Install

### ChatGPT / Codex

The public-directory submission is being prepared. For repo-hosted Codex testing:

```bash
codex plugin marketplace add signal-yield/jucho-kun
```

Then open `/plugins`, select the `signal-yield` marketplace, and install `jucho-kun`. Start a new conversation after installation.

The same skills-only package is prepared under `plugins/jucho-kun/` for the universal Plugins Directory shared by ChatGPT and Codex.

### Claude Code / Cowork

jucho-kun is distributed as a Claude Code Plugin via a repo-hosted Marketplace.

Verified: installation succeeds with no SSH setup required — no SSH key and no `known_hosts` entry for github.com are needed. No extra prerequisites beyond a working Claude Code CLI.

**Inside an interactive Claude Code / Cowork session**, using slash commands:

1. Add this repository as a Claude Code Marketplace:
   ```
   /plugin marketplace add signal-yield/jucho-kun
   ```
2. Install the plugin:
   ```
   /plugin install jucho-kun@jucho-kun
   ```
3. Type in Japanese to trigger the skill:
   ```
   重説調査して
   ```

**From a terminal**, using the non-interactive CLI (equivalent to steps 1–2 above):

```bash
claude plugin marketplace add signal-yield/jucho-kun
claude plugin install jucho-kun@jucho-kun
```

---

## How to Use

Just type naturally in Japanese:

```
重説調査して
```

The skill will ask you for:
1. Property address (物件住所)
2. Transaction type: 売買 (sale) or 賃貸 (lease)
3. Use type: 居住用 (residential) or 事業用 (commercial)
4. Whether the property is a 区分所有建物 (condominium unit)

Then it generates a checklist, fetches publicly available data, and outputs an Excel report.

---

## Example Output

For **京都府京都市東山区祇園町南側575**（売買・事業用）:

- **Urban Planning** (from Kyoto City GIS): 商業地域, 建ぺい率80%, 容積率400%, 防火地域, 高さ最高20m地区
- **Flood Hazard** (from 国土地理院): 洪水浸水想定区域あり（浸水深0.5〜3.0m）
- **Landslide**: Outside designated hazard zone (hillside area nearby has yellow/red zones)
- **Tsunami / Storm Surge**: Outside designated hazard zone (inland, elevation ≈40.7m)
- Plus a 30-item checklist with direct links to relevant government map services

---

## Important Disclaimer

> **This skill is a first-pass screening tool only.**
> All findings must be verified and the final disclosure document must be prepared, reviewed, and signed by a licensed *takken-shi* (宅建士). The author assumes no legal liability for the use of outputs from this skill.

---

## Author

**松田幸一 / Koichi Matsuda**
不動産鑑定士（Certified Real Estate Appraiser, registered 2002）
Signal Yield Advisory
〒106-0032 東京都港区六本木３－１６－１２ 六本木KSビル５F

- 📧 [signalYield@gmail.com](mailto:signalYield@gmail.com)
- 📝 [note.com/matsudansyaku](https://note.com/matsudansyaku)
- 💼 [VisasQ プロフィール](https://expert.visasq.com/profile/#/)

---

## License

MIT License. Feel free to fork, adapt, and improve.
Pull requests and issue reports are welcome.
