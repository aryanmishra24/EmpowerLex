from typing import List, Dict, Any
from langchain.tools import BaseTool

class NGOFinderTool(BaseTool):
    name = "ngo_finder"
    description = "Find relevant NGOs and legal aid organizations for different types of cases"
    
    def _run(self, category: str, location: str = "") -> List[Dict[str, Any]]:
        """Find NGOs relevant to the case category and location"""
        
        # Mock NGO database - in production, this would be a comprehensive database
        ngo_database = {
            "consumer protection": [
                {
                    "name": "Consumer Guidance Society of India",
                    "contact": "+91-11-2686-4423",
                    "email": "info@cgsi.in",
                    "address": "New Delhi",
                    "services": ["Consumer complaint filing", "Legal consultation", "Mediation"],
                    "website": "www.cgsi.in"
                },
                {
                    "name": "Voluntary Organisation in Interest of Consumer Education (VOICE)",
                    "contact": "+91-11-2616-7456",
                    "email": "voice@del3.vsnl.net.in",
                    "address": "New Delhi",
                    "services": ["Consumer awareness", "Legal aid", "Training programs"],
                    "website": "www.voiceindia.org"
                }
            ],
            "labour law": [
                {
                    "name": "Centre for Indian Trade Unions (CITU)",
                    "contact": "+91-11-2335-4836",
                    "email": "citu@vsnl.com",
                    "address": "New Delhi",
                    "services": ["Worker rights advocacy", "Legal assistance", "Industrial disputes"],
                    "website": "www.citucentre.org"
                },
                {
                    "name": "Self Employed Women's Association (SEWA)",
                    "contact": "+91-79-2550-6444",
                    "email": "mail@sewa.org",
                    "address": "Ahmedabad, Gujarat",
                    "services": ["Women workers rights", "Legal aid", "Skill development"],
                    "website": "www.sewa.org"
                }
            ],
            "family law": [
                {
                    "name": "All India Women's Conference (AIWC)",
                    "contact": "+91-11-2338-0563",
                    "email": "aiwc@airtelmail.in",
                    "address": "New Delhi",
                    "services": ["Women's rights", "Family counseling", "Legal aid"],
                    "website": "www.aiwc.org.in"
                },
                {
                    "name": "Lawyers Collective Women's Rights Initiative",
                    "contact": "+91-11-2685-4846",
                    "email": "lcwri@lawyerscollective.org",
                    "address": "New Delhi",
                    "services": ["Domestic violence cases", "Divorce proceedings", "Child custody"],
                    "website": "www.lawyerscollective.org"
                }
            ],
            "criminal law": [
                {
                    "name": "People's Union for Civil Liberties (PUCL)",
                    "contact": "+91-11-2686-4101",
                    "email": "puclnat@gmail.com",
                    "address": "New Delhi",
                    "services": ["Human rights", "Legal aid", "Criminal justice"],
                    "website": "www.pucl.org"
                },
                {
                    "name": "Common Cause",
                    "contact": "+91-11-2680-3833",
                    "email": "commoncause@bol.net.in",
                    "address": "New Delhi",
                    "services": ["Public interest litigation", "Legal reform", "Justice advocacy"],
                    "website": "www.commoncause-india.org"
                }
            ],
            "property law": [
                {
                    "name": "Housing and Land Rights Network",
                    "contact": "+91-11-4054-1680",
                    "email": "hlrn@hlrn.org.in",
                    "address": "New Delhi",
                    "services": ["Housing rights", "Land disputes", "Forced evictions"],
                    "website": "www.hlrn.org.in"
                }
            ]
        }
        
        # General legal aid organizations
        general_legal_aid = [
            {
                "name": "National Legal Services Authority (NALSA)",
                "contact": "15100 (Toll Free)",
                "email": "nalsa-cji@nic.in",
                "address": "Supreme Court of India, New Delhi",
                "services": ["Free legal aid", "Legal awareness", "Alternative dispute resolution"],
                "website": "www.nalsa.gov.in"
            },
            {
                "name": "Delhi Legal Services Authority",
                "contact": "+91-11-2389-0200",
                "email": "dlsa@delhicourts.nic.in",
                "address": "Delhi High Court, New Delhi",
                "services": ["Free legal aid", "Lok Adalat", "Legal literacy"],
                "website": "www.delhicourts.nic.in"
            }
        ]
        
        category_lower = category.lower()
        relevant_ngos = []
        
        # Find category-specific NGOs
        for ngo_category, ngos in ngo_database.items():
            if ngo_category in category_lower:
                relevant_ngos.extend(ngos)
        
        # Always include general legal aid
        relevant_ngos.extend(general_legal_aid)
        
        # Limit to top 3 most relevant
        return relevant_ngos[:3]
    
    async def _arun(self, category: str, location: str = "") -> List[Dict[str, Any]]:
        return self._run(category, location)
