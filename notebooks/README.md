# Notebooks

---

# Fintech Customer Experience Analytics

## Data Collection & Scraping Methodology (Task 1)

This section outlines the process of extracting user feedback for three major Ethiopian banking applications: **Commercial Bank of Ethiopia (CBE)**, **Bank of Abyssinia (BoA)**, and **Dashen Bank**.

### 1. Methodology

To ensure a robust and reproducible dataset, the following approach was taken:

* **Tooling:** Utilized the `google-play-scraper` Python library to interface with the Google Play Store’s frontend API.
* **Targeting:** Data was pulled using unique Application IDs (Package Names):
* **CBE:** `com.combanketh.mobilebanking`
* **BoA:** `com.boa.boaMobileBanking`
* **Dashen:** `com.cr2.amolelight`


* **Sampling Strategy:** We implemented a "Newest First" sorting strategy to capture the most recent user sentiment, ensuring the analysis reflects the current state of the apps (May 2026).
* **Fields Extracted:** Review content, star rating, date/timestamp, bank identifier, and source metadata.

### 2. Date Range

* **Start Date:** 15 may 2026
* **End Date:** 15 May 2026
* **Context:** This range was selected to capture a mix of historical performance and immediate reactions to recent app updates.

### 3. Data Cleaning & Preprocessing

To transform raw HTML/JSON responses into an analysis-ready format, we applied:

* **De-duplication:** Removed duplicate entries based on unique review IDs to prevent sentiment bias.
* **Handling Missing Values:** Dropped records where the `review_text` was empty (e.g., ratings-only submissions).
* **Normalization:** Converted all timestamps to standard `YYYY-MM-DD` format to facilitate time-series analysis in Task 4.

### 4. Limitations & Challenges

* **Language Barrier:** A significant portion of reviews are written in Amharic or "Amhinglish" (Amharic written with Latin characters). Current scraping focused on English text; future iterations may require specialized translation layers.
* **Rate Limiting:** Google Play Store imposes limits on deep-scrolling. To maintain connection stability, we implemented a 2-second cooldown between bank requests.
* **Data Sparsity:** While we hit the target of **400+ reviews per bank**, some banks have a higher volume of ratings than written reviews, limiting the depth of thematic analysis for those specific institutions.

---

