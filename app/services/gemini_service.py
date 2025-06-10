import httpx
from typing import Dict, Any, Optional
import json
from ..config import settings

class GeminiService:
    def __init__(self):
        self.api_key = settings.gemini_api_key
        self.api_url = settings.gemini_api_url
        self.headers = {
            "Content-Type": "application/json"
        }
    
    async def generate_content(self, prompt: str) -> Optional[str]:
        """Generate content using Gemini API (flash model, cURL style)"""
        try:
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ]
            }
            
            print(f"\nMaking API request to: {self.api_url}")
            print(f"Payload: {json.dumps(payload, indent=2)}")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}?key={self.api_key}",
                    json=payload,
                    headers=self.headers,
                    timeout=30.0  # Add timeout
                )
                
                print(f"Response status: {response.status_code}")
                print(f"Response body: {response.text[:500]}...")  # Print first 500 chars
                
                if response.status_code == 200:
                    result = response.json()
                    # Extract the generated text from the response
                    if "candidates" in result and len(result["candidates"]) > 0:
                        candidate = result["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"]:
                            parts = candidate["content"]["parts"]
                            if len(parts) > 0 and "text" in parts[0]:
                                return parts[0]["text"]
                    # If there's an error field in a 200 response
                    if "error" in result:
                        print(f"Gemini API error: {result['error']}")
                else:
                    # Print error details for non-200 responses
                    try:
                        error_json = response.json()
                        print(f"Gemini API error (non-200): {error_json}")
                    except Exception:
                        print("Non-JSON error response:", response.text)
                return None
                
        except httpx.TimeoutException:
            print("Request timed out after 30 seconds")
            return None
        except httpx.HTTPError as e:
            print(f"HTTP Error: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response text: {e.response.text}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None
    
    async def generate_legal_analysis(
        self,
        title: str,
        description: str,
        category: str,
        location: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate legal analysis using Gemini"""
        prompt = f"""Legal Case Analysis:
Title: {title}
Description: {description}
Category: {category}
Location: {location if location else 'Not specified'}

Provide a concise analysis covering:
1. Applicable laws and sections
2. Legal grounds
3. Next steps
4. Timeline
5. Potential challenges

Keep the response clear and structured with bullet points."""
        
        print(f"\nGenerating legal analysis for case: {title}")
        response = await self.generate_content(prompt)
        if response:
            return {
                "analysis": response,
                "source": "gemini"
            }
        return {
            "analysis": "Unable to generate analysis at this time.",
            "source": "error"
        }

# Create a singleton instance
gemini_service = GeminiService() 