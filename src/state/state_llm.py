from typing_extensions import TypedDict,List,Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing import Annotated


class ChatMessage(TypedDict):
    """ Schema definition for a chat message. """

    messages: Annotated[list,add_messages]

