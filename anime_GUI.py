import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

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

        # Settings panel
        hbox = QHBoxLayout()

        self.speaker_combobox = QComboBox(self)
        self.speaker_combobox.addItem("Speaker 1")
        self.speaker_combobox.addItem("Speaker 2")
        hbox.addWidget(self.speaker_combobox)

        self.slider_speed = self.create_slider("Speed")
        hbox.addWidget(self.slider_speed)

        self.slider_pitch = self.create_slider("Pitch")
        hbox.addWidget(self.slider_pitch)

        self.slider_intonation = self.create_slider("Intonation")
        hbox.addWidget(self.slider_intonation)

        self.slider_volume = self.create_slider("Volume")
        hbox.addWidget(self.slider_volume)

        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def create_slider(self, label_text):
        vbox = QVBoxLayout()

        label = QLabel(label_text, self)
        vbox.addWidget(label)

        slider = QSlider(Qt.Horizontal, self)
        vbox.addWidget(slider)

        return vbox

    def on_speak_clicked(self):
        self.sakura.set_speaker_id(self.speaker_combobox.currentIndex() + 1)
        self.sakura.set_speed(self.slider_speed.value() / 100)
        self.sakura.set_pitch(self.slider_pitch.value() / 100)
        self.sakura.set_intonation(self.slider_intonation.value() / 100)
        self.sakura.set_volume(self.slider_volume.value() / 100)

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