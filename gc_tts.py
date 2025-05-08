from google.cloud import texttospeech
from loguru import logger


class GoogleCloudTextToSpeech:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def list_voices(self):
        """Lists the available voices."""

        # Performs the list voices request
        voices = self.client.list_voices()

        for voice in voices.voices:
            # Display the voice's name. Example: tpc-vocoded
            print(f"Name: {voice.name}")

            # Display the supported language codes for this voice. Example: "en-US"
            for language_code in voice.language_codes:
                print(f"Supported language: {language_code}")

            ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender)

            # Display the SSML Voice Gender
            print(f"SSML Voice Gender: {ssml_gender.name}")

            # Display the natural sample rate hertz for this voice. Example: 24000
            print(f"Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}\n")

    def synthesis_input(self, text: str, filename: str = "choregraphe/output.mp3"):
        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            name="en-US-Neural2-D",
            language_code="en-US",
            ssml_gender=texttospeech.SsmlVoiceGender.MALE,
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        with open(filename, "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)
        logger.info(f"Audio content written to file: {filename}")


if __name__ == "__main__":
    gc_tts = GoogleCloudTextToSpeech()
    from mappings import MESSAGES, STREAK_MESSAGES
    from game import MessageType

    for idx, msg in enumerate(STREAK_MESSAGES):
        gc_tts.synthesis_input(
            msg, filename=f"choregraphe/0{MessageType.STREAK}{idx}.mp3"
        )

    for i, q in enumerate(MESSAGES):
        for idx, msg in enumerate(q.encouragements_human):
            gc_tts.synthesis_input(
                msg, filename=f"choregraphe/{i+1}{MessageType.ENCOURAGEMENT}{idx}.mp3"
            )
        for k, v in q.compliments_human.items():
            gc_tts.synthesis_input(
                v, filename=f"choregraphe/{i+1}{MessageType.COMPLIMENT}{k}.mp3"
            )
        for idx, msg in enumerate(q.hints):
            gc_tts.synthesis_input(
                msg, filename=f"choregraphe/{i+1}{MessageType.HINT}{idx}.mp3"
            )
        gc_tts.synthesis_input(
            q.answer,
            filename=f"choregraphe/{i+1}{MessageType.TIMEOUT}0.mp3",
        )
