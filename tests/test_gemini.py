import pytest
from app.services.gemini_service import gemini_service

@pytest.mark.asyncio
async def test_gemini_basic():
    """Test basic Gemini API functionality"""
    prompt = "Explain how AI works in a few words"
    response = await gemini_service.generate_content(prompt)
    print("\nBasic Gemini Test:")
    print(f"Prompt: {prompt}")
    print(f"Response: {response}\n")
    assert response is not None

@pytest.mark.asyncio
async def test_legal_analysis():
    """Test legal analysis functionality"""
    test_case = {
        "title": "Consumer Protection Case",
        "description": "I purchased a defective smartphone from an online store. The seller is refusing to replace it.",
        "category": "Consumer Protection",
        "location": "Mumbai"
    }
    
    response = await gemini_service.generate_legal_analysis(**test_case)
    print("\nLegal Analysis Test:")
    print(f"Test Case: {test_case}")
    print(f"Response: {response}\n")
    assert response["source"] == "gemini" 