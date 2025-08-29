from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

app = FastAPI(title="GDPR Agent API")

class UserInput(BaseModel):
    user_input: str

def main(user_input="What is GDPR?"):
    from src.graph.graph_build import graph_func
    chat_graph_run = graph_func()
    state = {"messages": user_input}
    res = chat_graph_run.invoke(state)
    ai_messages = [
        msg.content for msg in res["messages"]
        if getattr(msg, "type", None) == "ai"
    ]
    # print(res["messages"])
    # return res["messages"]
    print(ai_messages)
    return ai_messages[0] if ai_messages else None

@app.post("/ask_gdpr_bot")
async def ask_gdpr(user_question: str):
    answer = main(user_question)
    return {"answer": answer}

@app.get("/healthz")
def health():
    return {"ok": True}

# Optional: keep CLI entry point
if __name__ == "__main__":
    main()
