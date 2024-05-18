import os
import clr
import time
import json
import sys
sys.dont_write_bytecode = True



class AIVoiceEditor:
    master_control_settings = {
        "Volume": 1,
        "Speed": 1.2,
        "Pitch": 1.3,
        "PitchRange": 1.25
    }
    
    def __init__(self,settings=None):
        # 設定を引数から受け取る。引数が無ければクラスのデフォルト設定を使う
        if settings is None:
            self.settings = AIVoiceEditor.master_control_settings
        else:
            self.settings = settings
        self._editor_dir = os.environ['ProgramW6432'] + '\\AI\\AIVoice\\AIVoiceEditor\\'
        self._check_installation()
        self._load_api()
        self.tts_control = self._initialize_editor()
        
    def _check_installation(self):
        if not os.path.isfile(self._editor_dir + 'AI.Talk.Editor.Api.dll'):
            print("A.I.VOICE Editor (v1.3.0以降) がインストールされていません。")
            exit()

    def _load_api(self):
        # pythonnet DLLの読み込み
        clr.AddReference(self._editor_dir + "AI.Talk.Editor.Api")
        from AI.Talk.Editor.Api import TtsControl, HostStatus
        self.TtsControl = TtsControl
        self.HostStatus = HostStatus

    def _initialize_editor(self):
        tts_control = self.TtsControl()        
        # A.I.VOICE Editor APIの初期化
        host_name = tts_control.GetAvailableHostNames()[0]
        tts_control.Initialize(host_name)        
        # A.I.VOICE Editorの起動
        if tts_control.Status == self.HostStatus.NotRunning:
            tts_control.StartHost()        
        # A.I.VOICE Editorへ接続
        tts_control.Connect()
        host_version = tts_control.Version
        print(f"{host_name} (v{host_version}) へ接続しました。")        
        # マスターコントロールの設定をJSON形式に変換
        json_settings = json.dumps(self.settings)
        # JSON形式の設定をTtsControlに適用
        tts_control.set_MasterControl(json_settings)
        
        return tts_control

    def play_text(self, text):
        # テキストを設定
        self.tts_control.Text = text
        # 再生
        play_time = self.tts_control.GetPlayTime()
        self.tts_control.Play()
        # Play()は再生完了を待たないので予め取得した再生時間+α分sleepで待つ
        time.sleep((play_time + 500) / 1000)

    def close_editor(self):
        # 接続を終了する前に情報を取得
        host_name = self.tts_control.GetAvailableHostNames()[0]
        host_version = self.tts_control.Version
        # A.I.VOICE Editorとの接続を終了する
        self.tts_control.Disconnect()
        print(f"{host_name} (v{host_version}) との接続を終了しました。")


