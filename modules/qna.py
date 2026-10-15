from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
# from langchain.chains import LLMChain
#from langchain.memory import ConversationBufferMemory
from logger import CustomLogger  # Import CustomLogger
from prompts.qna_prompts import qna_prompt_template
from langchain_core.messages import HumanMessage, AIMessage


class QnAModule:
    """
    Handles Q&A functionality.
    """

    def __init__(self, api_key):
        """
        Initialize the QnA module.
        """
        # Initialize logger
        self.logger = CustomLogger().get_logger()
        self.logger.info("Initializing QnAModule.")

        # Initialize Groq LLM
        self.llm = ChatGroq(
            api_key=api_key,
            model="openai/gpt-oss-20b",
            temperature=0.1,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        self.logger.info("Groq LLM initialized for QnA module.")

        # Custom Prompt
        self.prompt = qna_prompt_template
        self.logger.info("Custom prompt initialized for QnA module.")

        # Initialize memory
        # Store conversation history
        self.qa_history = []
        #self.memory = ConversationBufferMemory(memory_key="history", input_key="question")
        #self.logger.info("Conversation memory initialized for QnA module.")

        # Create chain with memory
        #self.qa_chain = LLMChain(llm=self.llm, prompt=self.prompt, memory=self.memory)
        #self.logger.info("LLMChain created with memory for QnA module.")

    # Function to Handle Q&A
    def handle_qna(self, user_input):
        """
        Handles user queries for Q&A functionality.
        """
        try:
            # Format conversation history for the prompt
            history_text = "\n".join([f"{msg.type}: {msg.content}" for msg in self.qa_history]) if self.qa_history else "No previous history"
            
            # Format the prompt with the history and current question
            formatted_prompt = self.prompt.format(history=history_text, question=user_input)
            
            # Add user message to history
            self.qa_history.append(HumanMessage(content=user_input))
            
            # Call the LLM with the formatted prompt
            response = self.llm.invoke(formatted_prompt)

            # Add assistant response to history
            self.qa_history.append(AIMessage(content=response.content))

            print(f"[DEBUG] QnA Response: {response.content}")

            return response.content
        except Exception as e:
            return f"An error occurred while processing your question: {e}"