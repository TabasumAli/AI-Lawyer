# from rag_pipeline import answer_query, retrieve_docs, llm_model
# import re
# import streamlit as st

# # Inject custom CSS for chat container with vertical scrollbar on the left
# st.markdown(
#     """
#     <style>
#     /* Chat container with a fixed height and scrollbar on the left */
#     .chat-container {
#         max-width: 800px;
#         margin: auto;
#         padding: 10px;
#         max-height: 500px; /* Fixed height for the chat window */
#         overflow-y: auto;  /* Enable vertical scrolling when content overflows */
#         border: 1px solid #ddd;
#         background-color: #f9f9f9;
#         direction: rtl;   /* Scrollbar appears on the left side */
#     }
#     .chat-container > div {
#         direction: ltr;  /* Ensure the text remains left-to-right */
#     }
#     /* Styling for user and AI messages */
#     .user-message {
#         background-color: #DCF8C6;
#         border-radius: 10px;
#         padding: 10px;
#         margin: 5px 0;
#         text-align: right;
#     }
#     .ai-message {
#         background-color: #F1F0F0;
#         border-radius: 10px;
#         padding: 10px;
#         margin: 5px 0;
#         text-align: left;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # Sidebar with PDF uploader placed above the instructions
# with st.sidebar:
#     # Upload PDF first
#     uploaded_file = st.file_uploader(
#         "Upload PDF", type="pdf", accept_multiple_files=False
#     )

#     # Then show instructions
#     st.header("Instructions")
#     st.markdown(
#         """
#         - **Upload a PDF:** Upload the Declaration PDF.
#         - **Enter your prompt:** For example, "If a government forbids the right to assemble peacefully, which articles are violated and why?"
#         - **Chat:** Engage in a debate-like conversation.
#         """
#     )

# # Page title
# st.title("AI Lawyer Chatbot")

# # Use a form for the text input to enable clear-on-submit behavior
# with st.form(key="chat_form", clear_on_submit=True):
#     user_query = st.text_area(
#         "Enter your prompt:", height=150, placeholder="Ask Anything!"
#     )
#     submit_button = st.form_submit_button("Send")

# # Initialize chat history in session state if not already present
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = (
#         []
#     )  # Each entry: {"role": "user"/"AI Lawyer", "message": "...", "chain_thought": "..." (optional)}


# def parse_response(response_text: str):
#     """
#     Splits the response_text into two parts:
#       - chain_thought: the hidden reasoning between <think> and </think>
#       - final_answer: the visible answer text after the closing </think> tag
#     """
#     think_match = re.search(r"<think>(.*?)</think>", response_text, re.DOTALL)
#     chain_thought = think_match.group(1).strip() if think_match else ""
#     final_answer = re.sub(
#         r"<think>.*?</think>", "", response_text, flags=re.DOTALL
#     ).strip()
#     return chain_thought, final_answer


# if submit_button:
#     # Enforce that both a PDF is uploaded and a non-empty query is provided
#     if not uploaded_file:
#         st.error("Kindly upload a valid PDF file first!")
#     elif not user_query.strip():
#         st.error("Please enter your query before sending!")
#     else:
#         # Display the user's message in the chat
#         st.chat_message("user").write(user_query)

#         # Retrieve relevant documents and get the chain's response
#         retrieved_docs = retrieve_docs(user_query)
#         response_text = answer_query(
#             documents=retrieved_docs, model=llm_model, query=user_query
#         )
#         chain_thought, final_answer = parse_response(response_text)

#         # Append both the final answer and chain_of_thought to the chat history
#         st.session_state.chat_history.append({"role": "user", "message": user_query})
#         st.session_state.chat_history.append(
#             {
#                 "role": "AI Lawyer",
#                 "message": final_answer,
#                 "chain_thought": chain_thought,
#             }
#         )

# # Display the chat history in a fixed-height scrollable container
# st.markdown('<div class="chat-container">', unsafe_allow_html=True)
# for msg in st.session_state.chat_history:
#     if msg["role"] == "user":
#         st.markdown(
#             f'<div class="user-message"><strong>You:</strong><br>{msg["message"]}</div>',
#             unsafe_allow_html=True,
#         )
#     else:
#         st.markdown(
#             f'<div class="ai-message"><strong>AI Lawyer:</strong><br>{msg["message"]}</div>',
#             unsafe_allow_html=True,
#         )
# st.markdown("</div>", unsafe_allow_html=True)

# # Provide an expander to view the chain-of-thought for the last AI response
# if st.session_state.chat_history:
#     # Extract the last AI response that contains chain_thought
#     ai_messages = [
#         msg for msg in st.session_state.chat_history if msg["role"] == "AI Lawyer"
#     ]
#     if ai_messages:
#         last_ai_msg = ai_messages[-1]
#         with st.expander("Show chain-of-thought for the last response"):
#             if last_ai_msg.get("chain_thought"):
#                 st.markdown(last_ai_msg["chain_thought"])
#             else:
#                 st.markdown("*No chain-of-thought available*")



import streamlit as st
import re
from rag_pipeline import answer_query, retrieve_docs, llm_model

# Inject custom CSS for chat container with vertical scrollbar on the left
st.markdown(
    """
    <style>
    .chat-container {
        max-width: 800px;
        margin: auto;
        padding: 10px;
        max-height: 500px;
        overflow-y: auto;
        border: 1px solid #ddd;
        background-color: #f9f9f9;
        direction: rtl;
    }
    .chat-container > div {
        direction: ltr;
    }
    .user-message {
        background-color: #DCF8C6;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        text-align: right;
    }
    .ai-message {
        background-color: #F1F0F0;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar with PDF uploader
with st.sidebar:
    uploaded_file = st.file_uploader("Upload PDF", type="pdf", accept_multiple_files=False)
    st.header("Instructions")
    st.markdown(
        """
        - **Upload a PDF:** Upload the Declaration PDF.
        - **Enter your prompt:** Ask legal-related queries.
        - **Chat:** Engage in a legal conversation.
        """
    )

st.title("AI Lawyer Chatbot")

with st.form(key="chat_form", clear_on_submit=True):
    user_query = st.text_area("Enter your prompt:", height=150, placeholder="Ask Anything!")
    submit_button = st.form_submit_button("Send")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def parse_response(response_text: str):
    think_match = re.search(r"<think>(.*?)</think>", response_text, re.DOTALL)
    chain_thought = think_match.group(1).strip() if think_match else ""
    final_answer = re.sub(r"<think>.*?</think>", "", response_text, flags=re.DOTALL).strip()
    return chain_thought, final_answer

if submit_button:
    if not uploaded_file:
        st.error("Kindly upload a valid PDF file first!")
    elif not user_query.strip():
        st.error("Please enter your query before sending!")
    else:
        st.chat_message("user").write(user_query)
        retrieved_docs = retrieve_docs(user_query)
        response_text = answer_query(documents=retrieved_docs, model=llm_model, query=user_query)
        chain_thought, final_answer = parse_response(response_text)
        st.session_state.chat_history.append({"role": "user", "message": user_query})
        st.session_state.chat_history.append({"role": "AI Lawyer", "message": final_answer, "chain_thought": chain_thought})

st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-message"><strong>You:</strong><br>{msg["message"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-message"><strong>AI Lawyer:</strong><br>{msg["message"]}</div>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.chat_history:
    ai_messages = [msg for msg in st.session_state.chat_history if msg["role"] == "AI Lawyer"]
    if ai_messages:
        last_ai_msg = ai_messages[-1]
        with st.expander("Show chain-of-thought for the last response"):
            st.markdown(last_ai_msg["chain_thought"] if last_ai_msg.get("chain_thought") else "*No chain-of-thought available*")
