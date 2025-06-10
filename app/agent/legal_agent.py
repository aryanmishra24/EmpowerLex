from typing import Dict, List, Optional
from langchain.agents import AgentExecutor
from langchain.agents import Tool, OpenAIFunctionsAgent
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage

from ..services.gemini_service import gemini_service
from .tools.law_lookup import LawLookupTool
from .tools.draft_generator import DraftGeneratorTool
from .tools.ngo_finder import NGOFinderTool
from .tools.next_steps import NextStepsTool

class LegalAgent:
    def __init__(self, openai_api_key: str = None):
        # Initialize tools
        self.law_lookup = LawLookupTool()
        self.draft_generator = DraftGeneratorTool()
        self.ngo_finder = NGOFinderTool()
        self.next_steps = NextStepsTool()
        
        # Create tool list
        self.tools = [
            Tool(
                name="law_lookup",
                func=self.law_lookup.run,
                description="Find applicable Indian laws for a legal issue"
            ),
            Tool(
                name="draft_generator",
                func=self.draft_generator.run,
                description="Generate legal complaint drafts"
            ),
            Tool(
                name="ngo_finder",
                func=self.ngo_finder.run,
                description="Find relevant NGOs and legal aid organizations"
            ),
            Tool(
                name="next_steps",
                func=self.next_steps.run,
                description="Provide next steps and timeline for legal proceedings"
            )
        ]
        
        # Load system prompt
        with open("app/agent/prompts/system.txt", "r") as f:
            system_prompt = f.read()
        
        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Initialize OpenAI as fallback if API key is provided
        if openai_api_key:
            self.llm = ChatOpenAI(
                temperature=0,
                model_name="gpt-4-turbo-preview",
                openai_api_key=openai_api_key
            )
            self.agent_executor = AgentExecutor.from_agent_and_tools(
                agent=self._create_agent(),
                tools=self.tools,
                memory=self.memory,
                verbose=True
            )
        else:
            self.llm = None
            self.agent_executor = None
    
    def _create_agent(self):
        """Create the agent with the prompt and tools"""
        return OpenAIFunctionsAgent(
            llm=self.llm,
            prompt=self.prompt,
            tools=self.tools
        )
    
    async def process_case(
        self,
        title: str,
        description: str,
        category: str,
        location: Optional[str] = None
    ) -> Dict:
        """Process a legal case and generate comprehensive response"""
        
        # Get Gemini analysis
        gemini_analysis = await gemini_service.generate_legal_analysis(
            title=title,
            description=description,
            category=category,
            location=location
        )
        
        # Find applicable laws
        laws = self.law_lookup.run({
            "query": description,
            "category": category,
            "location": location
        })
        
        # Generate draft
        draft = self.draft_generator.run({
            "title": title,
            "description": description,
            "category": category,
            "laws": laws,
            "location": location
        })
        
        # Find relevant NGOs
        ngos = self.ngo_finder.run({
            "category": category,
            "location": location
        })
        
        # Get next steps
        steps = self.next_steps.run({
            "category": category,
            "case_title": title
        })
        
        return {
            "title": title,
            "category": category,
            "location": location,
            "applicable_laws": laws,
            "draft": draft,
            "suggested_ngos": ngos,
            "next_steps": steps,
            "ai_analysis": gemini_analysis
        }
    
    async def chat(self, message: str) -> str:
        """Handle chat interactions with the agent"""
        if self.agent_executor:
            # Use OpenAI if available
            response = await self.agent_executor.arun(message)
            return response
        else:
            # Fallback to Gemini
            response = await gemini_service.generate_content(message)
            return response if response else "I apologize, but I'm unable to process your request at this time." 