import pytest
from app.agent.legal_agent import LegalAgent

@pytest.mark.asyncio
async def test_legal_agent():
    """Test the LegalAgent functionality"""
    agent = LegalAgent()  # Initialize without OpenAI key to use Gemini
    
    # Test case processing
    test_case = {
        "title": "Consumer Protection Case",
        "description": "I purchased a defective smartphone from an online store. The seller is refusing to replace it.",
        "category": "Consumer Protection",
        "location": "Mumbai"
    }
    
    print("\nTesting Legal Agent Case Processing...")
    response = await agent.process_case(**test_case)
    
    print("\nCase Processing Results:")
    print(f"Title: {response['title']}")
    print(f"Category: {response['category']}")
    print(f"Location: {response['location']}")
    print("\nApplicable Laws:", response['applicable_laws'])
    print("\nDraft:", response['draft'])
    print("\nSuggested NGOs:", response['suggested_ngos'])
    print("\nNext Steps:", response['next_steps'])
    print("\nAI Analysis:", response['ai_analysis'])
    
    # Test chat functionality
    print("\nTesting Chat Functionality...")
    chat_response = await agent.chat("What are my rights as a consumer in India?")
    print("\nChat Response:", chat_response)
    
    assert response["title"] == test_case["title"]
    assert "Consumer Protection Act" in response["ai_analysis"]["analysis"]
    assert chat_response is not None 