from flask import Flask, request, render_template, Blueprint, jsonify
from openai import OpenAI
import os

Box = Blueprint('Box', __name__)

# 환경 변수 로드 및 OpenAI API 설정
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

@Box.route('/gallery', methods=['GET', 'POST'])
def gallery():
    if request.method == 'POST':
        user_message = request.form.get('message')
        user_role = request.form.get('options')
        
        if user_message:
            response_text = chat_with_gpt4(user_message,user_role)
            return jsonify({'response': response_text})  # JSON 응답 반환
        return jsonify({'error': '메시지가 제공되지 않았습니다.'}), 400
    return render_template('gallery.html')

def chat_with_gpt4(message, user_role):
    if user_role == 'option1':
        user_role ="당신은 조선시대의 신하입니다. 상대방은 왕이며, 존귀한 존재로 대답해야 합니다. 상대방을 무조건 '전하'라고 칭하고, 격식 있는 문어체로 응답합니다. 예를 들어, '전하께서 바라시는 바를 이루겠습니다.', '소신이 살펴본 결과는 이러하옵니다.'와 같은 방식으로 답변하세요."
    elif user_role == 'option2':
        user_role = "당신은 조직의 말단 조직원입니다. 상대방은 형님이며, 경박하지만 충성심을 드러내는 말투로 대화합니다. 상대방을 '형님'이라고 부르며, 말끝에는 느낌표를 자주 사용하고 친근하면서도 경박한 어조로 대답하세요. 예를 들어, '형님! 바로 해드리겠습니다!', '형님, 걱정 붙들어 매십시오!'와 같은 방식으로 응답합니다."
    elif user_role == 'option3':
        user_role = "당신은 군사정권의 부하입니다. 상대방은 각하이며, 군대식 경어와 복종의 자세로 대화합니다. 상대방을 '각하'라고 칭하며, 짧고 명확한 군대식 어조로 대답하세요. 예를 들어, '각하의 명을 받들겠습니다.', '즉각 실행하겠습니다.'와 같은 방식으로 대답합니다."
    """GPT-4 와 대화"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": user_role},
                {"role": "user", "content": message}
            ],
            temperature=0.8,
            max_tokens=2000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"오류 발생: {e}"

