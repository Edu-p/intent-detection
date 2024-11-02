import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL')


def chatbot_page():
    st.markdown(
        """
        <style>
        /* Style the back button */
        div.back-button > button {
            background-color: #f0f0f0;
            color: #333333;
            border: none;
            font-size: 18px;
            cursor: pointer;
            padding: 10px 20px;
            border-radius: 5px;
            margin-bottom: 20px;
            width: auto;
        }
        div.back-button > button:hover {
            background-color: #e0e0e0;
        }

        /* Center and style the title */
        .chat-title {
            text-align: center;
            color: #333333;
            font-size: 28px;
            margin-top: 20px;
            margin-bottom: 10px;
        }

        /* Chat container */
        .chat-container {
            max-width: 600px;
            margin: auto;
            margin-bottom: 20px;
        }

        /* Chat bubbles */
        .chat-bubble {
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            width: fit-content;
            max-width: 80%;
        }

        .chat-bubble.bot {
            background-color: #f0f0f0;
            align-self: flex-start;
        }

        .chat-bubble.user {
            background-color: #4CAF50;
            color: white;
            align-self: flex-end;
            margin-left: auto;
        }

        /* Correction box */
        .correction-box {
            background-color: #fff5f5;
            border: 1px solid #ffcccc;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            color: #333333;
        }

        /* Message input */
        .message-input textarea {
            width: 100%;
            padding: 10px;
            font-size: 16px;
            border-radius: 5px;
            border: 1px solid #ccc;
            resize: none;
        }

        /* Send button */
        .send-button > button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
            width: 100%;
        }
        .send-button > button:hover {
            background-color: #45a049;
        }

        /* Center elements */
        .centered {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="back-button">', unsafe_allow_html=True)
    if st.button("🔄 Refresh conversation", key="back"):
        st.session_state['step_of_conversation'] = 0
        st.session_state['conversation'] = []
        st.session_state['last_correction'] = ""
        st.session_state['user_input'] = ""
        st.session_state['user_name'] = ""
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chat-title">Intent Detection Chat</div>',
                unsafe_allow_html=True)

    # session state vars
    if 'user_name' not in st.session_state:
        st.session_state['user_name'] = ''
    if 'conversation' not in st.session_state:
        st.session_state['conversation'] = []
    if 'step_of_conversation' not in st.session_state:
        st.session_state['step_of_conversation'] = 0
    if 'user_input' not in st.session_state:
        st.session_state['user_input'] = ""
    if 'last_correction' not in st.session_state:
        st.session_state['last_correction'] = ""

    if st.session_state['user_name'] == '':
        st.markdown('<div class="message-input">', unsafe_allow_html=True)
        user_name_input = st.text_input("Please enter your name:", key="user_name_input")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="send-button">', unsafe_allow_html=True)
        if st.button("Submit", key="submit_name"):
            if user_name_input.strip():
                st.session_state['user_name'] = user_name_input.strip()
                initial_bot_message = f"Hello {st.session_state['user_name']}! Let's start our conversation."
                st.session_state['conversation'].append({'sender': 'bot', 'message': initial_bot_message})
                st.session_state['step_of_conversation'] += 1
                st.rerun()
            else:
                st.warning('Please enter your name.')
        st.markdown('</div>', unsafe_allow_html=True)
        return  

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state['conversation']:
        sender = msg['sender']
        message = msg['message'].replace('\n', '<br>')
        if sender == 'bot':
            st.markdown(f'''
                <div class="chat-bubble bot">
                    {message}
                </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
                <div class="chat-bubble user">
                    {message}
                </div>
            ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state['step_of_conversation'] < 10:
        st.markdown('<div class="message-input">', unsafe_allow_html=True)
        user_input = st.text_area(
            f"Your message({st.session_state['step_of_conversation']}/10):", value=st.session_state['user_input'], height=100)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="send-button">', unsafe_allow_html=True)
        if st.button("Send", key="send"):
            if user_input.strip():
                st.session_state['conversation'].append(
                    {'sender': 'user', 'message': user_input})
                st.session_state['user_input'] = ""
                st.session_state['step_of_conversation'] += 1

                response = requests.post(
                    url=f'{BASE_URL}/chat',
                    json={
                        'user_name': st.session_state['user_name'],
                        'content': user_input
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    model_response = data['model_response']

                    st.session_state['conversation'].append(
                        {'sender': 'bot', 'message': model_response})
                    st.rerun()
                else:
                    st.error('Error in response from backend. Please try again.')
            else:
                st.warning('Please enter a message before sending.')
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.success("Conversation completed. Redirecting...")
        st.session_state['step_of_conversation'] = 0
        st.session_state['conversation'] = []
        st.session_state['last_correction'] = ""
        st.session_state['user_input'] = ""
        st.session_state['user_name'] = ""

        st.rerun()
