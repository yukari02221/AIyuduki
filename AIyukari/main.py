import sys
from Voiceroid import AIVoiceEditor
from LangChain import get_response
import sys
sys.dont_write_bytecode = True

def main():
    sys.dont_write_bytecode = True

    ai_voice_editor = AIVoiceEditor()
    print("OpenAI Chat Character")
    print("終了するには 'exit' と入力してください。\n")

    try:
        while True:
            user_input = input("あなた: ")
            if user_input.lower() == 'exit':
                ai_voice_editor.close_editor()
                print("対話を終了します。")
                break

            response = get_response(user_input)
            ai_voice_editor.play_text(response)
            print("結月ゆかり: " ,response)
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()