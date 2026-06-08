# 📊 Programmatic Ingestion Engine for Outbound Growth

## Executive Summary
Early-stage Business Development (BDR) and Growth teams lose hundreds of high-leverage hours processing messy target prospect spreadsheets. Manual copy-pasting and raw directory dumps frequently introduce structural corruptions, whitespace padding, and broken tracking variables. This data chaos directly triggers revenue leakage and puts the company's official outbound email domain health at risk.

This repository hosts a production-grade, object-oriented data ingestion engine engineered in **Python and SQL**. It automates the web ingestion of raw B2B indices, applies vectorized transformations to resolve string irregularities, parses out validated emails using advanced Regular Expressions, and forces relational database deduplication to protect company domain health.

---

## 🛠️ Key Operational Problems Solved
* **Whitespace & Entity Resolution:** Clears destructive interior gaps, forcing entries like `"   VALCTRL   inc.  "` into pristine database formats (`"VALCTRL INC."`).
* **Deterministic Target Email Isolation:** Utilizes an optimized regular expression mapping module (`[\w\.-]+@[\w\.-]+\.\w+`) to selectively parse out true corporate emails (`dsimon@coastpay.com`).
* **Database-Level Deduplication:** Ingests normalized matrices into an ephemeral, relational SQLite database to clear duplicate accounts via structured relational filters (`GROUP BY`). This guarantees your outbound growth team never spam-emails the same founder twice, defending deliverability scores.

---

## ⚙️ Tech Stack Primitives
* **Core Languages:** Python 3.x, Structured Query Language (SQL)
* **Data Tools:** Pandas, Beautiful Soup 4, Requests, SQLite3, Re

---

## 👤 About the Engineer
I am an incoming **Lehigh University Economics graduate ('26)** and a **two-time university Williams Prize winner for writing**. I specialize in bridging the gap between advanced quantitative data models and high-converting, narrative sales persuasion to build scalable customer acquisition systems for early-stage B2B SaaS and FinTech companies.
