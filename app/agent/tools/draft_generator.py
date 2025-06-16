from typing import Dict, Any
from langchain_community.tools import BaseTool
from datetime import datetime
from ...services.gemini_service import gemini_service
import logging

logger = logging.getLogger(__name__)

class DraftGeneratorTool(BaseTool):
    name = "draft_generator"
    description = "Generate legal complaint drafts based on case details"
    
    async def _run(self, *args, **kwargs) -> str:
        """Generate a legal draft based on case details"""
        try:
            # Handle both dictionary and individual arguments
            if len(args) == 1 and isinstance(args[0], dict):
                case = args[0]
            else:
                case = {
                    "title": kwargs.get("title", ""),
                    "description": kwargs.get("description", ""),
                    "category": kwargs.get("category", ""),
                    "laws": kwargs.get("laws", []),
                    "location": kwargs.get("location", "")
                }
            
            # Get Gemini analysis first
            analysis = await gemini_service.generate_legal_analysis(
                title=case.get("title", ""),
                description=case.get("description", ""),
                category=case.get("category", ""),
                location=case.get("location", "")
            )
            
            # Check for threat-related keywords
            threat_keywords = ["threat", "kill", "murder", "assault", "violence", "abuse", "harass"]
            is_threat_case = any(keyword in case.get("title", "").lower() or 
                               keyword in case.get("description", "").lower() 
                               for keyword in threat_keywords)
            
            if is_threat_case:
                # Generate threat-specific draft
                draft = f"""IN THE COURT OF THE CHIEF JUDICIAL MAGISTRATE
AT {case.get('location', '')}

FIRST INFORMATION REPORT (FIR)
UNDER SECTION 154 OF THE CODE OF CRIMINAL PROCEDURE, 1973

Date: {datetime.now().strftime('%d-%m-%Y')}

TO,
The Station House Officer
Police Station: [POLICE STATION NAME]
District: [DISTRICT NAME]
State: [STATE NAME]

SUBJECT: FIR for Death Threats and Criminal Intimidation

MOST RESPECTFULLY SHOWETH:

1. That I, [YOUR FULL NAME], aged [AGE] years, residing at [YOUR COMPLETE ADDRESS], am filing this FIR regarding serious death threats and criminal intimidation.

2. FACTS OF THE CASE:
   {case.get('description', '')}

3. APPLICABLE LAWS:
   The above acts constitute violations under:
   - Indian Penal Code, 1860:
     * Section 503: Criminal Intimidation
     * Section 506: Punishment for Criminal Intimidation
     * Section 307: Attempt to Murder
   - Protection of Women from Domestic Violence Act, 2005 (if applicable)
   - Scheduled Castes and Scheduled Tribes (Prevention of Atrocities) Act, 1989 (if applicable)

4. EVIDENCE:
   a) Any text messages, emails, or social media communications containing threats
   b) Witness statements (if any)
   c) Any other relevant evidence

5. RELIEF SOUGHT:
   a) Registration of FIR under relevant sections of IPC
   b) Immediate police protection
   c) Investigation of the threats
   d) Appropriate legal action against the accused

6. VERIFICATION:
   I, [YOUR NAME], do hereby verify that the contents of this FIR are true and correct to the best of my knowledge and belief.

Date: {datetime.now().strftime('%d-%m-%Y')}
Place: {case.get('location', '')}

                                                    (Complainant)

LEGAL ANALYSIS:
{analysis}

IMPORTANT NEXT STEPS:
1. File this FIR at your nearest police station
2. Request a copy of the FIR with the FIR number
3. Consider applying for a restraining order
4. Keep all evidence safe and documented
5. Inform trusted friends/family about the situation
6. Consider seeking legal aid from:
   - State Legal Services Authority
   - National Commission for Minorities (if applicable)
   - Women's Commission (if applicable)
"""
            else:
                # Use existing draft generation logic for other cases
                draft = f"""LEGAL DRAFT
===========

Title: {case.get('title', '')}
Category: {case.get('category', '')}
Status: pending
Date: {datetime.now().strftime('%Y-%m-%d')}

Draft Content:
-------------
IN THE APPROPRIATE COURT
AT {case.get('location', '')}

COMPLAINT/PETITION UNDER RELEVANT PROVISIONS OF INDIAN LAW

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
THE HONOURABLE Appropriate Court

MOST RESPECTFULLY SHOWETH:

1. That the Complainant is a [resident/consumer/employee/etc.] and the Respondent is [business/individual/employer/etc.].

2. FACTS OF THE CASE:
   {case.get('description', '')}

3. LEGAL GROUNDS:
   The above acts of the Respondent constitute violations under:
   {chr(10).join(f'   - {law}' for law in case.get('laws', []))}

4. CAUSE OF ACTION:
   The cause of action arose on [DATE] when {case.get('description', '')}

5. JURISDICTION:
   This Hon'ble Appropriate Court has jurisdiction to try this matter as per the relevant provisions of law.

6. LIMITATION:
   This complaint/petition is within the prescribed period of limitation.

7. RELIEF SOUGHT:
   a) Direct the Respondent to [specific relief based on case type]
   b) Award compensation/damages of Rs. [amount] to the Complainant
   c) Award costs of this proceeding
   d) Pass any other order deemed fit and proper in the circumstances

WHEREFORE, the Complainant most respectfully prays that this Hon'ble Appropriate Court may be pleased to allow this complaint/petition and grant the reliefs prayed for.

Date: {datetime.now().strftime('%d-%m-%Y')}
Place: {case.get('location', '')}

                                                    (Complainant)

VERIFICATION:
I, [NAME], the above-named Complainant, do hereby verify that the contents of the above complaint are true and correct to the best of my knowledge and belief and that nothing material has been concealed therefrom.

Verified at {case.get('location', '')} on this {datetime.now().strftime('%d')} day of {datetime.now().strftime('%B')}, {datetime.now().strftime('%Y')}.

                                                    (Complainant)

LEGAL ANALYSIS:
{analysis}"""

            return draft
        except Exception as e:
            logger.error(f"Error generating draft: {str(e)}", exc_info=True)
            return f"Error generating draft: {str(e)}"
    
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
    
    async def _arun(self, case: Dict[str, Any]) -> Dict[str, Any]:
        return await self._run(case)
