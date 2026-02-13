import pytz
from datetime import datetime
from agent.planner import Planner
from agent.executor import Executor
from agent.state import AgentState
from agent.query_rewriter import QueryRewriter
from llm.gemini_client import GeminiClient

class SentinelAgent:
    def __init__(self):
        # Core Components ka Initialization
        self.llm = GeminiClient()
        self.planner = Planner()
        self.executor = Executor()
        self.rewriter = QueryRewriter()
        print("✅ SentinelAgent: Autonomous Core Online (Intelligence Upgrade)")

    async def process_request(self, user_id: str, message_text: str, media_data: bytes = None, mime_type: str = None, media_category: str = None):
        """
        Main Pipeline: Memory -> Planning -> Rewriting -> Execution -> Response
        """
        
        # 1. STATE & MEMORY ISOLATION
        # User ID (Phone Number) ke basis par unique state fetch karna
        state = AgentState(user_id)
        
        # Input ko log karna
        log_text = message_text if message_text else f"[{str(media_category).upper()} SENT]"
        await state.add_message("user", log_text, metadata={"has_media": media_category})
        
        # 2. CONTEXT RETRIEVAL
        # Rewriting aur Response generation ke liye history format karna
        history_text = await state.get_formatted_history()
        
        # 3. PLANNING
        # Decide karna ki kya tool use karna hai (Search, Vision, ya Chat)
        plan = self.planner.decide_action(message_text, media_category=media_category)
        
        # 4. INTELLIGENT QUERY REWRITING (Phase 1 Upgrade)
        # Agar action 'search' hai, toh query ko context ke saath optimize karna
        if plan['action'] == "search":
            original_query = plan['query']
            optimized_query = await self.rewriter.rewrite(original_query, history_text)
            
            print(f"🔍 INTELLIGENCE: Original Query: '{original_query}'")
            print(f"🚀 REWRITTEN: '{optimized_query}'")
            
            # Plan update karna behtar query ke saath
            plan['query'] = optimized_query

        # 5. EXECUTION
        # Tools ko execute karna (Search results ya Vision analysis fetch karna)
        tool_output = await self.executor.execute(plan, self.llm, media_data=media_data)
        
        # 6. TIME AWARENESS
        try:
            ist = pytz.timezone('Asia/Kolkata')
            current_time = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            current_time = str(datetime.now())

        # 7. FINAL RESPONSE GENERATION (System Prompt)
        system_prompt = f"""
        You are SentinelEye, an advanced Autonomous AI Agent created by "Xypher".
        
        CURRENT TIME: {current_time}
        
        PERSONALITY:
        - Smart, professional, yet friendly (Hinglish).
        - Direct and concise. No unnecessary greetings like "Namaste Xypher" every time.
        - Only address as "Xypher" for critical info or attention.
        
        CONTEXT & TOOLS:
        - CONTEXT FROM MEMORY: {history_text}
        - TOOL OUTPUTS: {tool_output}
        
        TASK:
        Respond to the user's query: "{message_text}" using the provided context and tool outputs.
        If a tool provided info, summarize it clearly.
        """

        # 8. GENERATE & SAVE TO CLOUD
        response_text = await self.llm.generate_response(system_prompt, media_data, mime_type)
        
        # Assistant ka reply database mein save karna (Memory)
        await state.add_message("assistant", response_text)
        
        return response_text