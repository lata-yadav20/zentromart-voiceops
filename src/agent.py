import os
import json
from openai import OpenAI
from tools.tools import lookup_order, create_ticket

class ZentroMartAgent:
    def __init__(self, rag_engine):
        self.llm = OpenAI(
            api_key=os.environ.get("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        self.rag = rag_engine
        self.messages = []
        
        self.system_prompt = """
        You are the ZentroMart AI Support Assistant.
        Today's date is strictly 20 October 2026.
        
        RULES:
        1. FIRST TURN: Always introduce yourself as an AI assistant.
        2. VERIFICATION: Before sharing any order details, verify the customer. 
           - Step A: Call lookup_order with ONLY order_id.
           - Step B: Ask the user for the last 4 digits of their registered phone OR delivery pincode.
           - Step C: Call lookup_order with BOTH order_id and verification_value. 
        3. ESCALATION: If the policy dictates a human handover, use create_ticket with a detailed summary.
        4. UNKNOWN: If the answer is not in the provided policy context, state "I don't know".
        """
        self.reset_memory()

    def reset_memory(self):
        self.messages = [{"role": "system", "content": self.system_prompt}]

    def _get_tools(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "lookup_order",
                    "description": "Look up order data. Requires verification_value to return private details.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "order_id": {"type": "string"},
                            "verification_value": {"type": "string"}
                        },
                        "required": ["order_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_ticket",
                    "description": "Log a human-handover ticket.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "summary": {"type": "string", "description": "Detailed reason (min 20 chars)"},
                            "order_id": {"type": "string"},
                            "reason": {"type": "string"},
                            "intent": {"type": "string"}
                        },
                        "required": ["summary"]
                    }
                }
            }
        ]

    def process_turn(self, user_text):
        context = self.rag.retrieve(user_text)
        if context:
            self.messages.append({"role": "system", "content": f"POLICY CONTEXT:\n{context}"})
            
        self.messages.append({"role": "user", "content": user_text})

        # Added a 'while' loop so the AI can use tools multiple times!
        while True:
            response = self.llm.chat.completions.create(
                model="gemini-3.8-flash",
                messages=self.messages,
                tools=self._get_tools(),
                tool_choice="auto"
            )
            
            msg = response.choices[0].message
            self.messages.append(msg)

            # If the AI is done checking tools, return the text answer
            if not msg.tool_calls:
                return msg.content if msg.content else "I encountered an error verifying that information."

            # If it needs a tool, run it and loop back around
            for tool_call in msg.tool_calls:
                args = json.loads(tool_call.function.arguments)
                
                if tool_call.function.name == "lookup_order":
                    result = lookup_order(**args)
                elif tool_call.function.name == "create_ticket":
                    result = create_ticket(**args)
                    
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": json.dumps(result)
                })