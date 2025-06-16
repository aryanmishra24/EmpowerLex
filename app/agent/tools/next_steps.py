from typing import List, Dict, Any
from langchain.tools import BaseTool
from ...services.gemini_service import gemini_service
import logging

logger = logging.getLogger(__name__)

class NextStepsTool(BaseTool):
    name = "next_steps"
    description = "Provide next steps and timeline for legal proceedings"
    
    async def _run(self, *args, **kwargs) -> List[str]:
        """Generate next steps based on case details"""
        try:
            # Handle both dictionary and individual arguments
            if len(args) == 1 and isinstance(args[0], dict):
                case = args[0]
            else:
                case = {
                    "category": kwargs.get("category", ""),
                    "case_title": kwargs.get("case_title", ""),
                    "description": kwargs.get("description", ""),
                    "location": kwargs.get("location", "")
                }
            
            # Get legal analysis and next steps from Gemini
            analysis = await gemini_service.generate_legal_analysis(
                title=case.get("case_title", ""),
                description=case.get("description", ""),
                category=case.get("category", ""),
                location=case.get("location", "")
            )
            
            # Generate structured next steps using Gemini, tailored for Indian context and Markdown formatting
            prompt = f"""Based on the following case details, generate a structured list of next steps with specific actions and timelines, tailored for the Indian legal and social context:

Title: {case.get('case_title', '')}
Description: {case.get('description', '')}
Category: {case.get('category', '')}
Location: {case.get('location', '')}

Legal Analysis: {analysis}

Please provide:
1. Immediate safety measures (mention Indian emergency number 112, local police, and FIR process)
2. Legal documentation requirements (reference Indian laws and procedures)
3. Legal protection options (such as Protection Orders, approaching Magistrate, etc.)
4. Support services and organizations (Indian NGOs, NALSA, helplines, etc.)
5. Ongoing safety measures (culturally relevant)
6. Legal proceedings timeline (Indian court process)

Format the output using Markdown for bold, italics, and lists. Use clear line breaks between steps and actions."""

            next_steps = await gemini_service.generate_content(prompt)
            
            # Convert the response into a list of strings
            steps = []
            if next_steps:
                # Split by newlines and filter out empty lines
                steps = [step.strip() for step in next_steps.split('\n') if step.strip()]
            
            return steps
            
        except Exception as e:
            logger.error(f"Error generating next steps: {str(e)}", exc_info=True)
            return [f"Error generating next steps: {str(e)}"]
    
    async def _arun(self, case: Dict[str, Any]) -> Dict[str, Any]:
        """Async implementation of the tool"""
        try:
            # Get next steps
            next_steps = await self._run(case)
            
            # Get legal analysis
            analysis = await gemini_service.generate_legal_analysis(
                title=case.get('title', ''),
                description=case.get('description', ''),
                category=case.get('category', ''),
                location=case.get('location', '')
            )
            
            return {
                'next_steps': next_steps,
                'analysis': analysis
            }
        except Exception as e:
            logger.error(f"Error in async execution: {str(e)}", exc_info=True)
            return {
                'next_steps': [f"Error generating next steps: {str(e)}"],
                'analysis': "Error generating analysis"
            }
