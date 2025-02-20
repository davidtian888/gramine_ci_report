import autogen
import os
import requests
from data.constants import *

class OpenAIAnalyser:
    def __init__(self):
        os.environ["no_proxy"] = "localhost,127.0.0.1,::1,10.0.0.0/8,192.168.0.0/16,intel.com,.openai.azure.com,10.*"
        self.llm_config = {
            "config_list": [{
                "model": OPENAI_MODEL,
                "api_key": AZURE_OPENAI_KEY,
                "base_url": AZURE_OPENAI_URL,
                "api_type": "azure",
                "api_version": OPENAI_API_VERSION
            }],
            "temperature" : 0.7,
            "max_tokens": 50
        }
        self.proxies = {
            "http": "http://proxy-dmz.intel.com:911/",
            "https": "http://proxy-dmz.intel.com:912/"
        }
        self.create_agent()
        self.details = rf"""You are an assistant responsible for analyzing the given logs and identifying the root cause of the failure. Look for any error messages, stack traces, or other indications of what went wrong. Analyze the log to identify any potential issues or errors. There may be trace, debug, system calls, and workload execution. Pinpoint the exact cause of failure, as there may be several things that may look like errors.
        
        Pay attention to the following areas or other indications of what went wrong: Network issues, Authentication problems, Repository access permissions, Configuration errors, Git Clone issues, Error Messages, Exceptions and stack traces. Use contextual information from the logs to understand the environment and conditions under which the failure occurred. Provide a concise analysis (20 words).

        Error Logs: """
    
    def create_agent(self):
        session = requests.Session()
        session.proxies.update(self.proxies)
        self.ai_agent = autogen.AssistantAgent("analysis_agent", llm_config=self.llm_config)
        self.user_proxy = autogen.UserProxyAgent("user_proxy",
                        llm_config=False,
                        human_input_mode="NEVER",
                        code_execution_config={
                            "executor": autogen.coding.LocalCommandLineCodeExecutor(work_dir="coding")
                        }
                    )

    def preprocess_text(self, text):
        max_context = 128000
        if len(text) < max_context:
            return text
        
        return text[-min(max_context, len(text)):]

    def generate_inference(self, text):

        text = self.preprocess_text(text)
        prompt = self.details + text       

        chat_results = autogen.initiate_chats([{
                "sender": self.user_proxy,
                "recipient": self.ai_agent,
                "message": prompt,
                "max_turns": 1, 
                "summary_method": "reflection_with_llm",
            }]
        )
        return chat_results[0].summary
    
