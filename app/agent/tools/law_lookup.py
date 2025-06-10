from typing import List, Dict, Any
from langchain.tools import BaseTool

class LawLookupTool(BaseTool):
    name = "law_lookup"
    description = "Look up applicable Indian laws for a given legal issue"
    
    def _run(self, query: str, category: str = "", location: str = "") -> List[Dict[str, Any]]:
        """Look up relevant Indian laws based on the query"""
        
        # Mock database of Indian laws - in production, this would be a proper database
        indian_laws_db = {
            "consumer protection": [
                {
                    "act": "Consumer Protection Act, 2019",
                    "section": "Section 2(7) - Definition of Consumer",
                    "description": "Defines who qualifies as a consumer under the act",
                    "penalty": "As per Section 87 - imprisonment up to 1 year or fine up to Rs 10,000"
                },
                {
                    "act": "Consumer Protection Act, 2019",
                    "section": "Section 35 - Jurisdiction of District Commission",
                    "description": "Cases involving goods/services up to Rs 1 crore",
                    "penalty": "Compensation and damages as deemed fit"
                }
            ],
            "labour law": [
                {
                    "act": "Industrial Disputes Act, 1947",
                    "section": "Section 25F - Conditions precedent to retrenchment",
                    "description": "Requirements for lawful retrenchment of workers",
                    "penalty": "Reinstatement with back wages"
                },
                {
                    "act": "Payment of Wages Act, 1936",
                    "section": "Section 7 - Deductions from wages",
                    "description": "Authorized deductions from employee wages",
                    "penalty": "10 times the amount wrongfully deducted"
                }
            ],
            "property law": [
                {
                    "act": "Transfer of Property Act, 1882",
                    "section": "Section 54 - Sale of immovable property",
                    "description": "Requirements for valid sale of property",
                    "penalty": "Contract may be declared void"
                },
                {
                    "act": "Registration Act, 1908",
                    "section": "Section 17 - Documents requiring registration",
                    "description": "Mandatory registration for property documents",
                    "penalty": "Document inadmissible as evidence"
                }
            ],
            "criminal law": [
                {
                    "act": "Indian Penal Code, 1860",
                    "section": "Section 420 - Cheating",
                    "description": "Punishment for cheating and dishonestly inducing delivery of property",
                    "penalty": "Imprisonment up to 7 years and fine"
                },
                {
                    "act": "Indian Penal Code, 1860",
                    "section": "Section 506 - Criminal intimidation",
                    "description": "Threatening another with injury to person, reputation or property",
                    "penalty": "Imprisonment up to 2 years or fine or both"
                }
            ],
            "family law": [
                {
                    "act": "Hindu Marriage Act, 1955",
                    "section": "Section 13 - Divorce",
                    "description": "Grounds for dissolution of marriage",
                    "penalty": "Dissolution of marriage and related reliefs"
                },
                {
                    "act": "Protection of Women from Domestic Violence Act, 2005",
                    "section": "Section 12 - Protection orders",
                    "description": "Court orders to protect women from domestic violence",
                    "penalty": "Imprisonment up to 1 year or fine up to Rs 20,000"
                }
            ]
        }
        
        # Simple keyword matching - in production, use more sophisticated NLP
        category_lower = category.lower()
        relevant_laws = []
        
        for law_category, laws in indian_laws_db.items():
            if law_category in category_lower or any(word in query.lower() for word in law_category.split()):
                relevant_laws.extend(laws)
        
        # If no specific match, return general laws
        if not relevant_laws:
            relevant_laws = [
                {
                    "act": "Indian Contract Act, 1872",
                    "section": "Section 73 - Compensation for breach of contract",
                    "description": "Compensation for loss or damage caused by breach",
                    "penalty": "Compensation for actual loss"
                },
                {
                    "act": "Code of Civil Procedure, 1908",
                    "section": "Order VII Rule 1 - Plaint to contain facts",
                    "description": "Requirements for filing a civil suit",
                    "penalty": "Suit may be rejected or dismissed"
                }
            ]
        
        return relevant_laws[:3]  # Return top 3 relevant laws
    
    async def _arun(self, query: str, category: str = "", location: str = "") -> List[Dict[str, Any]]:
        return self._run(query, category, location)
