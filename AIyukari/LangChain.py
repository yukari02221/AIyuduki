from langchain.chains import LLMChain, SequentialChain
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import json

# APIキーとモデル名を設定
api_key = "YOUR_API_KEY"
llm = ChatOpenAI(api_key=api_key, model="gpt-4o")

# 感情パラメーターの初期値を設定
emotion_params = {
    "喜び": 3,
    "怒り": 0,
    "悲しみ": 0,
    "楽しさ": 3,
    "自信": 3,
    "困惑": 0,
    "恐怖": 0
}

# 会話の履歴を管理するリストを用意
conversation_history = [
    {"role": "system", "content": "あなたはマスターが大好きなVOICEROIDキャラクターの結月ゆかりです。マスターとゆかりさんは結婚していて仲睦まじく暮らしています。一人称はゆかりさんです。"}
]

def get_response(prompt):
    global emotion_params

    # ユーザーの発言を会話の履歴に追加
    conversation_history.append({"role": "user", "content": prompt})

    # json.dumps()を使って辞書をJSON形式の文字列に変換
    emotion_params_str = json.dumps(emotion_params, ensure_ascii=False)

    # 感情パラメータを更新するテンプレート
    template1 = "{input}情報を基にあなたの気持ちを{emotion_params}のそれぞれの値を更新して0~10段階で表現し、更新後のemotion_paramsのみを出力してください。"
    prompt1 = PromptTemplate(
        input_variables=["input", "emotion_params"],
        template=template1
    )

    # 会話を生成するテンプレート
    template2 = "{emotion}の値を基に{conversation_history}から自然な会話をしてください。"
    prompt2 = PromptTemplate(
        input_variables=["emotion", "conversation_history"],
        template=template2
    )

    # LLMChainを作成
    chain1 = LLMChain(llm=llm, prompt=prompt1, output_key="emotion")
    chain2 = LLMChain(llm=llm, prompt=prompt2, output_key="response")

    overall_chain = SequentialChain(
        chains=[chain1, chain2],
        input_variables=["input", "emotion_params", "conversation_history"],
        output_variables=["emotion", "response"],
        verbose=True
    )

    # チェインを実行して結果を取得
    result = overall_chain.invoke({
        "input": prompt,
        "emotion_params": emotion_params_str,
        "conversation_history": json.dumps(conversation_history, ensure_ascii=False)
    })
    # 更新された感情パラメーターを取得
    try:
        updated_emotion_params = json.loads(result['emotion'])
        emotion_params.update(updated_emotion_params)
        # print("更新された感情パラメーター:", emotion_params)
    except json.JSONDecodeError:
        print("応答の解析中にエラーが発生しました。")


    # システムの応答を会話の履歴に追加
    conversation_history.append({"role": "assistant", "content": result['response']})

    return result['response']

# # ユーザーからの入力を取得
# input_data = input("あなた: ")

# # 応答を取得して表示
# response = get_response(input_data)
# print("ゆかりさん:", response)
