from agent.ikea_agent import ikea_agent
import streamlit as st

st.title("IKEA İndirimli Ürünler Kataloğu Asistanı")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show Previous Message
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# New Message
if prompt := st.chat_input("Ürün arayın..."):
    # User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Bot respond
    with st.chat_message("assistant"):
        response = ikea_agent(prompt)
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Clear Button
if st.button("🗑️ Temizle"):
    st.session_state.messages = []
    st.rerun()