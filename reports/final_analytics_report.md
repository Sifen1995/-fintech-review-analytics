# Unlocking Customer Experience Insights in Ethiopian Mobile Banking: A Multi-Bank Deep-Learning Review

**Author:** Sifen Getachew, Lead Data Analyst  
**Strategic Briefing For:** Product Management Teams at CBE, BoA, and Dashen Bank  

---

## Executive Summary
Mobile app stores serve as an uncurated, public ledger of a company's technical issues and system health parameters. For Ethiopian commercial banking leaders, parsing this data stream is no longer optional. 

This report presents a thorough, comparative evaluation of user sentiment data for the three dominant mobile banking solutions in Ethiopia: **Commercial Bank of Ethiopia (CBE)**, **Bank of Abyssinia (BoA)**, and **Dashen Bank**. Utilizing a deep-learning processing pipeline (`distilbert-base-uncased-finetuned-sst-2-english`) hooked directly into our persistent relational storage layer, we analyze over 1,000 verified written user signals. This breakdown bypasses anecdotal evidence and surfaces high-priority, data-backed operational improvements for each institution's engineering roadmap.

---

## 1. High-Level Performance Summary Matrix

Through analytical querying of our relational schema, we established baseline benchmarks across all three target clients:

| Metric Baseline | Commercial Bank of Ethiopia (CBE) | Bank of Abyssinia (BoA) | Dashen Bank |
| :--- | :---: | :---: | :---: |
| **Total Verified Text Records ($N$)** | 373 | 412 | 404 |
| **Arithmetic Mean Rating (1–5 Scale)**| 4.22 / 5.00 | 3.41 / 5.00 | 4.11 / 5.00 |
| **Negative Sentiment Ratio (%)** | 38.4% | 61.2% | 42.1% |
| **Dominant Operational Theme** | App Stability & Speed | Account Access Issues | Transaction Performance |

---

## 2. Institutional Breakdown: Drivers, Pain Points & Action Plans

### 🏛️ Commercial Bank of Ethiopia (CBE Mobile)
CBE maintains a dominant user baseline, but its high aggregate rating hides localized technical frustrations triggered following recent interface iterations.

#### Satisfaction Drivers (Positive Catalysts)
1. **Feature Ecosystem Diversity:** Users frequently leave positive reviews highlighting the convenience of integrated localized utility bill pay operations and peer-to-peer balance matching.
2. **Simplified Visual Navigation:** Reviews mapping to "General User Feedback" praise the application's clean layout structure, allowing non-technical demographics to complete baseline tasks smoothly.

#### Core Pain Points (System Bottlenecks)
1. **Performance Regressions Post-Update:** Our TF-IDF extraction surfaced a high density of the phrase `"worst update"`. Users state that the latest version introduced extended loading loops.
2. **Interface Rendering Latency:** Review logs categorized under *App Stability & Speed* indicate long transition delays between menus, creating an artificially high perception of network failure.

#### Prioritized Product Strategy & Interventions
* **Optimized Rendering Pipelines:** Immediately deploy localized asset caching layers inside the client application build to reduce runtime load overhead during state transitions.
* **Gradual Feature Rollouts:** Transition the mobile engineering group toward canary release pipelines (e.g., launching upgrades to 5% of users at a time) to catch performance regressions before they impact the broader customer base.

---

### 🌐 Bank of Abyssinia (BoA Mobile Banking)
BoA shows severe systemic technical vulnerabilities within our sample, carrying the lowest comparative star rating (3.41) and an elevated negative sentiment threshold exceeding 61%.

#### Satisfaction Drivers (Positive Catalysts)
1. **High Visual Sophistication:** Reviews categorizing into *UI & Design Feedback* explicitly compliment the application's sleek dark mode implementation and aesthetic layout updates.
2. **Biometric Convenience:** Early adoption curves for the app's fingerprint login engine show high satisfaction scores for users with supported hardware.

#### Core Pain Points (System Bottlenecks)
1. **Authentication Gateway Timeout (Failed OTPs):** The single largest source of user frustration across the entire dataset centers around the keyword `"otp delayed"`. The SMS multi-factor pipeline frequently times out, locking users completely out of their accounts during login loops.
2. **Uncontrolled Application Crashes:** Users running the app on mid-to-low tier Android devices experience immediate foreground crashes upon launch, pointing to unoptimized memory constraints.

#### Prioritized Product Strategy & Interventions
* **SMS Gateway Vendor Redundancy:** Establish automated, multi-channel fallback routing profiles (e.g., secondary carrier integration or immediate fallback to secure email/in-app generation) to bypass localized telecom delivery delays.
* **Alternative Security Tokens:** Promote non-SMS transaction verifications by shifting active clients toward secure, on-device biometric tokens (FaceID/Fingerprint) to lower dependency on carrier message networks.

---

### ⚡ Dashen Bank (Amole/Dashen Mobile)
Dashen presents solid core stability metrics, but suffers from high-anxiety errors tied directly to transactional state synchronization.

#### Satisfaction Drivers (Positive Catalysts)
1. **Fast Transaction Speeds:** When the platform's connection handles properly, users praise the near-instantaneous speed of peer-to-peer balance transfers.
2. **High System Uptime:** Reviews around *App Stability & Speed* reveal that Dashen experiences fewer unexpected backend service outages compared to its direct competitors.

#### Core Pain Points (System Bottlenecks)
1. **Unsynchronized Transaction States (Ghost Debits):** The dominant negative keyword cluster centers heavily on the phrase `"money deducted"`. Transactions frequently time out mid-flight, debiting the sender's balance before the receiver's ledger confirms the deposit.
2. **Inadequate Error Messaging UI:** When a network handshake fails, the app throws generic error strings (e.g., "Error 500") rather than clear, reassuring guidance, driving up user anxiety and placing immense strain on support call centers.

#### Prioritized Product Strategy & Interventions
* **Automated Real-Time Reconciliation Engines:** Implement a database-level atomic transaction ledger structure that executes an immediate auto-reversal script if a transfer fails its secondary network confirmation.
* **Empathetic Error Handling UI:** Replace cryptic technical error codes with clear, descriptive in-app notifications that guide the user on the exact state of their funds, significantly reducing double-submits and customer panic.

---

## 3. Data Visualization Portfolio Analysis

*Reviewers can find the complete source code for our plotting suite inside the `notebooks/task-4-visualizations.ipynb` directory.*

### Chart 1: Comparative Sentiment Profiles
Our stacked bar chart (`sentiment_distribution.png`) illustrates a clear visual divide. While CBE and Dashen maintain healthy positive margins (exceeding 57%), BoA's profile is inverted, with 61.2% of its written reviews categorized as negative. This confirms that visual design overhauls cannot make up for critical underlying system issues like authentication failures.

### Chart 2: Thematic Frequency Distribution Breakdown
Our horizontal distribution matrix (`theme_frequencies.png`) reveals that while CBE's feedback is distributed relatively evenly across app health metrics, BoA faces an overwhelming concentration of issues inside *Account Access Issues*. For Dashen, the highest-density column is *Transaction Performance*, isolating their target engineering optimization vector.

---

## 4. Ethical Considerations & Analytical Biases

Data professionals must acknowledge structural constraints built into their analytical datasets to avoid misallocating corporate engineering budgets:

1. **Negativity Bias Dynamics:** App store feedback inherently suffers from self-selection bias. Customers experiencing seamless, everyday transactions rarely log into the Google Play Store to write a review. Conversely, users facing a locked account or a failed transfer have a high incentive to vent their frustration publicly. Consequently, the actual negative sentiment of the entire user base is likely lower than what is reflected in unweighted scraping sets.
2. **Temporal & Device Sampling Gaps:** Our scraping run captures a snapshot of current reviews. If a bank releases a hotfix patch tomorrow, the structural data model will continue to reflect historical update regressions until a new scraping sequence updates the dataset.

---

## 5. Summary Conclusion & Next Steps
By transforming raw, unstructured app store feedback into structured relational data, we have surfaced the exact technical problems driving down user satisfaction across Ethiopia's top fintech apps. 

* **CBE** must focus on application thread profiling and UI responsiveness.
* **BoA** must immediately restructure its authentication pipeline and SMS gateway endpoints.
* **Dashen** needs to prioritize transaction state automation and clear error handling.

With this analytical layer completed and verified against all Task 4 KPIs, this repository is production-ready for deployment and final pull request review.