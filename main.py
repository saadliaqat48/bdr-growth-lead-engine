import re
import sqlite3
import logging
import json
import pandas as pd
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")

class EnterpriseGrowthIntelligencePipeline:
    def __init__(self):
        self.db_conn = sqlite3.connect(":memory:")
        # Strategic weights reflecting high-intent acquisition sectors
        self.sector_weights = {
            "fintech / ai": 1.0,
            "fintech saas": 0.95,
            "b2b saas / devtools": 0.90,
            "artificial intelligence": 0.85,
            "logistics / trucking": 0.80,
            "commercial hvac / fleets": 0.70,
            "shipping / fleets": 0.70,
            "plumbing fleets": 0.60
        }

    def ingest_bulk_market_ledger(self) -> str:
        """Simulates high-volume, structural corporate directory dump raw payload."""
        raw_payload = [
            {"raw_company": "   VALCTRL   inc.  ", "raw_industry": "FinTech / AI", "raw_contact": "FOUNDER@valctrl.trade; alt: info@valctrl.com", "revenue_tier": "Seed"},
            {"raw_company": "gynger LLC", "raw_industry": "FINTECH SaaS", "raw_contact": "sales@gynger.io", "revenue_tier": "Series A"},
            {"raw_company": "coast payments ", "raw_industry": "b2b logistics", "raw_contact": "dsimon@coastpay.com", "revenue_tier": "Series A"},
            {"raw_company": "   VALCTRL   inc.  ", "raw_industry": "FinTech / AI", "raw_contact": "FOUNDER@valctrl.trade", "revenue_tier": "Seed"}, # Duplicate
            {"raw_company": "GOTHAM LOGISTICS CORP", "raw_industry": "Logistics / Trucking", "raw_contact": "ops@gothamtransit.com", "revenue_tier": "Bootstrapped"},
            {"raw_company": "NEO-CLOUD AUTOMATIONS INC", "raw_industry": "B2B SaaS / DevTools", "raw_contact": "founder@neocloud.io", "revenue_tier": "Seed"},
            {"raw_company": "VERTEX DATA LABS", "raw_industry": "Enterprise Software", "raw_contact": "infrastructure@vertexlabs.ai", "revenue_tier": "Series B"},
            {"raw_company": "BRONX HEATING AND AC LLC", "raw_industry": "Commercial HVAC / Fleets", "raw_contact": "service@bronxhvac.com", "revenue_tier": "Bootstrapped"},
            {"raw_company": "KEYSTONE FREIGHT SYS", "raw_industry": "Shipping / Fleets", "raw_contact": "dispatch@keystonefreight.net", "revenue_tier": "Matured"},
            {"raw_company": "METRO PLUMBING GROUP", "raw_industry": "Plumbing Fleets", "raw_contact": "MALFORMED_ROW_NO_EMAIL", "revenue_tier": "Bootstrapped"},
            {"raw_company": "QUANTUM AI PLATFORMS", "raw_industry": "Artificial Intelligence", "raw_contact": "billing@quantumai.tech", "revenue_tier": "Seed"},
            {"raw_company": "STRATTON MACRO FORECASTING", "raw_industry": "Macro Research / Analytics", "raw_contact": "research@strattonmacro.com", "revenue_tier": "N/A"}
        ]
        return json.dumps(raw_payload)

    def process_and_normalize(self, raw_json_data: str) -> pd.DataFrame:
        """Applies vectorized normalization and uses advanced RegEx patterns."""
        logging.info("Initializing vector cleaning arrays...")
        data = json.loads(raw_json_data)
        df = pd.DataFrame(data)

        # Advanced string parsing transformations
        df["company_clean"] = df["raw_company"].str.upper().str.replace(r"\s+", " ", regex=True).str.strip()
        df["industry_clean"] = df["raw_industry"].str.lower().str.strip()
        df["revenue_tier"] = df["revenue_tier"].str.strip()

        # Isolate true outbound corporate emails
        email_regex = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
        def extract_email(contact_str: str) -> Optional[str]:
            matches = email_regex.findall(str(contact_str))
            return matches[0].lower() if matches else None

        df["verified_email"] = df["raw_contact"].apply(extract_email)
        return df

    def compute_lead_score_matrix(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        ECONOMIC MODELING NODE: Computes a programmatic priority score index (0.00 - 1.00)
        based on industry vertical weight and email domain validation parameters.
        """
        logging.info("Deploying quantitative priority matrix modeling calculations...")
        
        def calculate_score(row) -> float:
            if pd.isna(row["verified_email"]):
                return 0.0
            
            # Base industry alignment weight score
            base_weight = self.sector_weights.get(row["industry_clean"], 0.50)
            
            # Domain structural multiplier bonus (Corporate domains vs generic consumer nodes)
            domain_multiplier = 1.0
            if any(domain in row["verified_email"] for domain in ["gmail.com", "yahoo.com", "outlook.com"]):
                domain_multiplier = 0.50
                
            # Funding/Revenue velocity tracking coefficient
            tier_coefficient = 1.0
            if row["revenue_tier"] in ["Seed", "Series A"]:
                tier_coefficient = 1.15 # High prioritization premium for well-funded buyers

            return round(min(base_weight * domain_multiplier * tier_coefficient, 1.00), 2)

        df["target_priority_score"] = df.apply(calculate_score, axis=1)
        return df

    def enforce_relational_integrity(self, df: pd.DataFrame) -> pd.DataFrame:
        """Executes staging database deduplication and orders entities by target priority score."""
        logging.info("Ingesting clean matrices into memory-staged SQLite workspace...")
        df.to_sql("lead_ledger", self.db_conn, index=False, if_exists="replace")

        sql_query = """
            SELECT 
                company_clean AS Target_Company,
                industry_clean AS Market_Vertical,
                verified_email AS Primary_Outbound_Email,
                revenue_tier AS Capital_Tier,
                target_priority_score AS Priority_Score
            FROM lead_ledger
            WHERE Primary_Outbound_Email IS NOT NULL
            GROUP BY Target_Company
            ORDER BY Priority_Score DESC;
        """
        
        final_ledger = pd.read_sql_query(sql_query, self.db_conn)
        self.db_conn.close()
        return final_ledger

if __name__ == "__main__":
    pipeline = EnterpriseGrowthIntelligencePipeline()
    raw_payload = pipeline.ingest_bulk_market_ledger()
    normalized_frame = pipeline.process_and_normalize(raw_payload)
    enriched_frame = pipeline.compute_lead_score_matrix(normalized_frame)
    production_ready_sheet = pipeline.enforce_relational_integrity(enriched_frame)

    # Save out to operational folder workspace
    production_ready_sheet.to_csv("verified_bdr_targets.csv", index=False)
    print("\n" + "="*85)
    print(production_ready_sheet.to_string(index=False))
    print("="*85 + "\n[✓] Advanced Enterprise Ingestion Pipeline V2 Execution Completed Successfully.")
