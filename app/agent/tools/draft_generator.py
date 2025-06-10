from typing import Dict, Any
from langchain_community.tools import BaseTool
from datetime import datetime

class DraftGeneratorTool(BaseTool):
    name = "draft_generator"
    description = "Generate legal complaint drafts based on case details"
    
    def _run(self, title: str, description: str, category: str, laws: list, location: str = "") -> str:
        """Generate a legal complaint draft"""
        
        # Determine court jurisdiction based on category
        jurisdiction_map = {
            "consumer protection": "District Consumer Disputes Redressal Commission",
            "labour law": "Labour Court/Industrial Tribunal",
            "criminal law": "Metropolitan Magistrate/Judicial Magistrate",
            "civil law": "Civil Court",
            "family law": "Family Court",
            "property law": "Civil Court"
        }
        
        jurisdiction = jurisdiction_map.get(category.lower(), "Appropriate Court")
        
        # Generate complaint draft
        draft = f"""IN THE {jurisdiction.upper()}
AT {location.upper() if location else '[PLACE]'}

COMPLAINT/PETITION UNDER RELEVANT PROVISIONS

Between:

[COMPLAINANT NAME]
[Complete Address]
[Phone Number]
[Email Address]
                                                    ...Complainant/Petitioner

AND

[RESPONDENT/DEFENDANT NAME]
[Address if known]
                                                    ...Respondent/Defendant

TO,
THE HONOURABLE {jurisdiction}

MOST RESPECTFULLY SHOWETH:

1. That the Complainant is a [resident/consumer/employee/etc.] and the Respondent is [business/individual/employer/etc.].

2. FACTS OF THE CASE:
   {self._format_facts(description)}

3. LEGAL GROUNDS:
   The above acts of the Respondent constitute violations under:
   {self._format_legal_grounds(laws)}

4. CAUSE OF ACTION:
   The cause of action arose on [DATE] when {title.lower()}.

5. JURISDICTION:
   This Hon'ble {jurisdiction} has jurisdiction to try this matter as per the relevant provisions of law.

6. LIMITATION:
   This complaint/petition is within the prescribed period of limitation.

7. RELIEF SOUGHT:
   a) Direct the Respondent to [specific relief based on case type]
   b) Award compensation/damages of Rs. [amount] to the Complainant
   c) Award costs of this proceeding
   d) Pass any other order deemed fit and proper in the circumstances

WHEREFORE, the Complainant most respectfully prays that this Hon'ble {jurisdiction} may be pleased to allow this complaint/petition and grant the reliefs prayed for.

Date: {datetime.now().strftime('%d-%m-%Y')}
Place: {location if location else '[Place]'}

                                                    (Complainant)

VERIFICATION:
I, [NAME], the above-named Complainant, do hereby verify that the contents of the above complaint are true and correct to the best of my knowledge and belief and that nothing material has been concealed therefrom.

Verified at {location if location else '[Place]'} on this {datetime.now().strftime('%d day of %B, %Y')}.

                                                    (Complainant)"""
        
        return draft
    
    def _format_facts(self, description: str) -> str:
        """Format the case facts in legal style"""
        sentences = description.split('.')
        formatted_facts = []
        
        for i, sentence in enumerate(sentences, 1):
            if sentence.strip():
                formatted_facts.append(f"   {sentence.strip()}.")
        
        return '\n'.join(formatted_facts)
    
    def _format_legal_grounds(self, laws: list) -> str:
        """Format applicable laws"""
        if not laws:
            return "   Relevant provisions of applicable laws."
        
        formatted_laws = []
        for law in laws:
            formatted_laws.append(f"   - {law.get('act', '')} - {law.get('section', '')}")
        
        return '\n'.join(formatted_laws)
    
    async def _arun(self, title: str, description: str, category: str, laws: list, location: str = "") -> str:
        return self._run(title, description, category, laws, location)
