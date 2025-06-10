from typing import List
from langchain.tools import BaseTool

class NextStepsTool(BaseTool):
    name = "next_steps"
    description = "Provide next steps and timeline for legal proceedings"
    
    def _run(self, category: str, case_title: str) -> List[str]:
        """Generate next steps based on case category"""
        
        steps_map = {
            "consumer protection": [
                "1. Gather all purchase receipts, warranty cards, and communication records",
                "2. Send a legal notice to the seller/service provider (30-60 days response time)",
                "3. If no response, file complaint with District Consumer Commission",
                "4. Pay the prescribed court fee based on compensation claimed",
                "5. Attend hearings as scheduled by the Commission",
                "6. If unsatisfied with District Commission order, appeal to State Commission within 30 days"
            ],
            "labour law": [
                "1. Document all evidence of unfair treatment, salary slips, and employment records",
                "2. Approach the Labour Officer for conciliation (mandatory step)",
                "3. If conciliation fails, file application before Labour Court/Industrial Tribunal",
                "4. Serve notice to the employer through registered post",
                "5. Attend conciliation proceedings and hearings",
                "6. Appeal to High Court if necessary within prescribed time limit"
            ],
            "criminal law": [
                "1. File FIR at the nearest police station immediately",
                "2. Gather and preserve all evidence (documents, witnesses, CCTV footage)",
                "3. Cooperate with police investigation",
                "4. If police refuse to file FIR, approach Magistrate under Section 156(3) CrPC",
                "5. Engage a criminal lawyer for court proceedings",
                "6. Attend all court hearings and provide testimony when required"
            ],
            "family law": [
                "1. Attempt mediation/counseling through family court or counselors",
                "2. Gather relevant documents (marriage certificate, income proof, property papers)",
                "3. File petition in appropriate Family Court",
                "4. Serve notice to the other party",
                "5. Attend court-ordered mediation sessions",
                "6. Proceed with trial if mediation fails, present evidence and witnesses"
            ],
            "property law": [
                "1. Verify property documents and title clearance",
                "2. Send legal notice to the defaulting party",
                "3. File suit for specific performance or damages in Civil Court",
                "4. Apply for temporary injunction if necessary",
                "5. Complete court-ordered procedures (survey, valuation, etc.)",
                "6. Attend trial proceedings and present documentary evidence"
            ],
            "civil law": [
                "1. Send legal notice to the opposite party (mandatory in most cases)",
                "2. Wait for 30-60 days for response to legal notice",
                "3. File civil suit in appropriate court with jurisdiction",
                "4. Pay court fee and process fee for service of summons",
                "5. Attend case management hearings and pre-trial conferences",
                "6. Present evidence, examine witnesses during trial"
            ]
        }
        
        category_lower = category.lower()
        for step_category, steps in steps_map.items():
            if step_category in category_lower:
                return steps
        
        # Default steps for general cases
        return steps_map["civil law"]
    
    async def _arun(self, category: str, case_title: str) -> List[str]:
        return self._run(category, case_title)
