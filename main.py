import re
import sqlite3
import logging
import pandas as pd
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")

class EnterpriseBdrEngine:
    def __init__(self):
        self.raw_leads: List[Dict[str, str]] = []
        self.db_conn = sqlite3.connect(":memory:")

    def load_massive_uncleaned_matrix(self) -> None:
        logging.info("Deploying high-volume uncleaned target lead matrix...")
        self.raw_leads = [
            # Tri-State Commercial Fleets (Target Variables for Coast Payments)
            {"raw_company": "   GOTHAM LOGISTICS CORP  ", "raw_industry": "Logistics / Trucking", "raw_contact": "ops@gothamtransit.com"},
            {"raw_company": "BRONX HEATING AND AC LLC", "raw_industry": "Commercial HVAC / Fleets", "raw_contact": "DIRECTOR: service@bronxhvac.com"},
            {"raw_company": "   GOTHAM LOGISTICS CORP  ", "raw_industry": "Logistics / Trucking", "raw_contact": "ops@gothamtransit.com"}, 
            {"raw_company": "KEYSTONE FREIGHT SYS", "raw_industry": "Shipping / Fleets", "raw_contact": "dispatch@keystonefreight.net; billing@keystone.net"},
            {"raw_company": "METRO PLUMBING GROUP", "raw_industry": "Plumbing Fleets", "raw_contact": "UNKNOWN CORRUPTED TEXT"}, 
            
            # Venture-Backed Scaleups (Target Variables for Gynger Tech BNPL)
            {"raw_company": "NEO-CLOUD AUTOMATIONS INC", "raw_industry": "B2B SaaS / DevTools", "raw_contact": "founder@neocloud.io"},
            {"raw_company": "  VERTEX   DATA LABS ", "raw_industry": "Enterprise Software", "raw_contact": "infrastructure@vertexlabs.ai"},
            {"raw_company": "APEX CYBERSECURITY", "raw_industry": "SaaS / Security", "raw_contact": "corrupted-email-field"}, 
            {"raw_company": "NEO-CLOUD AUTOMATIONS INC", "raw_industry": "B2B SaaS / DevTools", "raw_contact": "founder@neocloud.io"}, 
            {"raw_company": "QUANTUM AI PLATFORMS", "raw_industry": "Artificial Intelligence", "raw_contact": "billing@quantumai.tech"},
            
            # Quantitative Finance & Macro Context (Target Variables for ValCtrl)
            {"raw_company": "  ALPHA QUANT   FUND  ", "raw_industry": "FinTech / Hedge Fund", "raw_contact": "tradingops@alphaquant.trade"},
            {"raw_company": "STRATTON MACRO FORECASTING", "raw_industry": "Macro Research / Analytics", "raw_contact": "research@strattonmacro.com"},
            {"raw_company": "CAPITAL LINE INFRASTRUCTURE", "raw_industry": "FinTech / Fixed Income", "raw_contact": "contact@caplinefin.com"},
            {"raw_company": "SYSTEMIC ANOMALY NODE", "raw_industry": "N/A", "raw_contact": "no-data"}, 
        ]

    def clean_via_pandas(self) -> pd.DataFrame:
        logging.info("Executing vectorized string normalization...")
        df = pd.DataFrame(self.raw_leads)
        df["company_clean"] = df["raw_company"].str.upper().str.replace(r"\s+", " ", regex=True).str.strip()
        df["industry_clean"] = df["raw_industry"].str.lower().str.strip()

        email_regex = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
        def parse_email(text: str) -> Optional[str]:
            matches = email_regex.findall(str(text))
            return matches[0].lower() if matches else None

        df["verified_email"] = df["raw_contact"].apply(parse_email)
        return df

    def enforce_sql_integrity(self, df: pd.DataFrame) -> pd.DataFrame:
        logging.info("Ingesting data variables into SQLite environment...")
        df.to_sql("staging_ledger", self.db_conn, index=False, if_exists="replace")

        sql_query = """
            SELECT 
                company_clean AS Target_Company,
                industry_clean AS Industry_Vertical,
                verified_email AS Primary_Outbound_Email
            FROM staging_ledger
            WHERE verified_email IS NOT NULL 
              AND company_clean NOT LIKE '%SYSTEMIC%'
            GROUP BY company_clean;
        """
        final_sheet = pd.read_sql_query(sql_query, self.db_conn)
        self.db_conn.close()
        return final_sheet

if __name__ == "__main__":
    engine = EnterpriseBdrEngine()
    engine.load_massive_uncleaned_matrix()
    normalized_frame = engine.clean_via_pandas()
    production_ready_leads = engine.enforce_sql_integrity(normalized_frame)
    production_ready_leads.to_csv("verified_bdr_targets.csv", index=False)
    print("\n" + "="*75)
    print(production_ready_leads.to_string(index=False))
    print("="*75 + "\n[✓] Executed Successfully.")
