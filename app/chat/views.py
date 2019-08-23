from flask import render_template, request, make_response
from flask_login import current_user, login_required
from . import chat

all_msg = []
@chat.route('/')
@login_required
def chat_page():
    return render_template('/chat/chat.html')


@chat.route('/chat.do', methods=['POST'])
@login_required
def deal_chat():
    print("deal_chat.{}".format(request.values.get('chatMsg')))
    chat_msg = request.values.get('chatMsg')
    if chat_msg is None:
        chat_msg = ""
    else:
        if len(all_msg) > 40:
            all_msg.clear()
        all_msg.append("[{}] 说:".format(current_user.username) + chat_msg)

    # print(chat_msg)
    return make_response('\n'.join(all_msg)), 200
