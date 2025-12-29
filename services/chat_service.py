from langchain_core.messages import get_buffer_string, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, MessagesState
from langchain_core.messages import trim_messages

from config.settings import settings

class ChatService:
    def __init__(self, thread_id: str):
        self.thread_id = thread_id
        self.memory = MemorySaver()
        self.llm = ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.model_name
        )

        self.trimmer = trim_messages(
            strategy="last",
            max_tokens=settings.max_tokens,
            token_counter=self._count_tokens,
            include_system=True,
            start_on="human"
        )

        self.graph = self._build_graph()
        self._initialize_system_prompt()

    def send_message(self, user_message: str) -> str:

        result = self.graph.invoke(
            {"messages": [HumanMessage(content=user_message)]},
            {"configurable": {"thread_id": self.thread_id}}
        )

        return result["messages"][-1].content

    def get_history(self):
        state = self.graph.get_state(
            {"configurable": {"thread_id": self.thread_id}}
        )
        messages = state.values.get("messages", [])

        return self._filter_system_messages(messages)

    def _count_tokens(self, messages: list) -> int:
        text = get_buffer_string(messages)
        return self.llm.get_num_tokens(text)

    def _build_graph(self):
        workflow = StateGraph(state_schema=MessagesState)
        workflow.add_edge(START, "model")
        workflow.add_node("model", self._call_model)

        return workflow.compile(checkpointer=self.memory)

    def _call_model(self, state: MessagesState) -> dict:
        trimmed = self.trimmer.invoke(state["messages"])
        completion = self.llm.invoke(trimmed)
        return {"messages": completion}

    def _initialize_system_prompt(self):
        system_msg = SystemMessage(content=settings.system_prompt)
        self.graph.invoke(
            {"messages": [system_msg]},
            {"configurable": {"thread_id": self.thread_id}}
        )


    def _filter_system_messages(self, messages):
        filtered = [msg for msg in messages if msg.type in ["human", "ai"]]
        return filtered[1:] if len(filtered) > 0 and filtered[0].type == "ai" else filtered
