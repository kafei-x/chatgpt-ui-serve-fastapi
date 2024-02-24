from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain.memory import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability.",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)


chain = prompt | chat


store = {}

def get_by_session_id(session_id: int) -> BaseChatMessageHistory:
    
    # 存放会话和历史记录的映射
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def del_by_session_id(session_id: int):
    
    if session_id in store:
        history = store[session_id]
        history.clear()
        del store[session_id]
        return True, None
    return False, f"error: {session_id} not in store"



chain_with_message_history = RunnableWithMessageHistory(
    chain,
    get_by_session_id,       # function, 根据key获取历史记录
    input_messages_key="input",
    history_messages_key="chat_history",
)