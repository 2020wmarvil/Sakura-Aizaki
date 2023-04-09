import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap

from sakura_aizaki import SakuraAizaki


class AnimeGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.sakura = SakuraAizaki()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Sakura Aizaki')

        vbox = QVBoxLayout()

        self.label_image = QLabel(self)
        pixmap = QPixmap('anime_character.png')  # Replace with the path to your anime character image
        self.label_image.setPixmap(pixmap)
        vbox.addWidget(self.label_image)

        self.label_text = QLabel('こんにちは！私はあなたの言葉を日本語に翻訳できます。', self)
        vbox.addWidget(self.label_text)

        self.button_speak = QPushButton('Speak', self)
        self.button_speak.clicked.connect(self.on_speak_clicked)
        vbox.addWidget(self.button_speak)
        
        self.setLayout(vbox)

    def on_speak_clicked(self):
        audio_data = self.sakura.record_voice()
        transcribed_text = self.sakura.transcribe(audio_data)
        print(f"You: {transcribed_text}")
        if transcribed_text.lower() == "quit":
            self.close()
        chatbot_response = self.sakura.chatbot_response(transcribed_text)
        translated_response = self.sakura.translate_to_japanese(chatbot_response)
        print(f"Sakura Aizaki (Japanese text): {translated_response}")
        self.label_text.setText(translated_response)
        audio_response = self.sakura.text_to_speech(translated_response)
        self.sakura.play_audio(audio_response)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AnimeGUI()
    window.show()
    sys.exit(app.exec_())