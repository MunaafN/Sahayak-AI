import os
import logging
import speech_recognition as sr
import io
import base64
from typing import Optional

# Optional Google Cloud imports
try:
    from google.cloud import speech
    GOOGLE_SPEECH_AVAILABLE = True
except ImportError:
    GOOGLE_SPEECH_AVAILABLE = False

try:
    from google.cloud import texttospeech
    GOOGLE_TTS_AVAILABLE = True
except ImportError:
    GOOGLE_TTS_AVAILABLE = False

logger = logging.getLogger(__name__)

class SpeechService:
    """Service for speech recognition and audio processing"""
    
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        
        # Initialize Google Cloud Speech and TTS clients if credentials and libraries are available
        self.speech_client = None
        self.tts_client = None
        
        try:
            if self.project_id and GOOGLE_SPEECH_AVAILABLE:
                self.speech_client = speech.SpeechClient()
                logger.info("Google Cloud Speech client initialized")
        except Exception as e:
            logger.warning(f"Could not initialize Google Cloud Speech client: {e}")
            
        try:
            if self.project_id and GOOGLE_TTS_AVAILABLE:
                self.tts_client = texttospeech.TextToSpeechClient()
                logger.info("Google Cloud TTS client initialized")
        except Exception as e:
            logger.warning(f"Could not initialize Google Cloud TTS client: {e}")
            
        if not self.speech_client and not self.tts_client:
            logger.info("Speech service running in demo mode (Google Cloud not configured)")
    
    async def transcribe_audio(self, audio_content: bytes, language: str = "en-US") -> str:
        """
        Transcribe audio to text using Google Cloud Speech-to-Text
        
        Args:
            audio_content: Audio file content in bytes
            language: Language code for transcription
            
        Returns:
            Transcribed text
        """
        try:
            logger.info(f"Transcribing audio in language: {language}")
            
            # For demo purposes, return mock transcription
            # In production, replace with actual Google Cloud Speech API call
            
            mock_transcriptions = {
                "en": "The cat sat on the mat. It was a big cat. The cat was black and white.",
                "hi": "बिल्ली चटाई पर बैठी थी। वह एक बड़ी बिल्ली थी।",
                "mr": "मांजर चटईवर बसली होती. ती एक मोठी मांजर होती."
            }
            
            # Return mock transcription based on language
            lang_code = language.split('-')[0] if '-' in language else language
            return mock_transcriptions.get(lang_code, mock_transcriptions["en"])
            
            # Actual implementation would be:
            # if self.speech_client:
            #     audio = speech.RecognitionAudio(content=audio_content)
            #     config = speech.RecognitionConfig(
            #         encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            #         sample_rate_hertz=48000,
            #         language_code=self._get_language_code(language),
            #     )
            #     response = self.speech_client.recognize(config=config, audio=audio)
            #     return response.results[0].alternatives[0].transcript if response.results else ""
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            raise Exception(f"Audio transcription failed: {str(e)}")
    
    async def text_to_speech(self, text: str, language: str = "en") -> str:
        """
        Convert text to speech using browser Web Speech API (client-side)
        Returns instructions for client-side TTS
        
        Args:
            text: Text to convert to speech
            language: Language code for speech
            
        Returns:
            Base64 encoded audio or instructions for client-side TTS
        """
        try:
            logger.info(f"Preparing TTS for text: {text[:50]}... in language: {language}")
            
            # For demo purposes, return instructions for client-side Web Speech API
            # This is more compatible and doesn't require server-side audio processing
            
            language_voices = {
                "en": "en-US",
                "hi": "hi-IN", 
                "mr": "mr-IN"
            }
            
            voice_lang = language_voices.get(language, "en-US")
            
            # Return configuration for client-side TTS
            tts_config = {
                "text": text,
                "lang": voice_lang,
                "rate": 0.8,  # Slower for educational content
                "pitch": 1.0,
                "volume": 1.0,
                "useWebSpeechAPI": True
            }
            
            # Encode as base64 for consistent API response
            import json
            config_json = json.dumps(tts_config)
            config_b64 = base64.b64encode(config_json.encode()).decode()
            
            return config_b64
            
            # Actual Google Cloud TTS implementation would be:
            # if self.tts_client:
            #     synthesis_input = texttospeech.SynthesisInput(text=text)
            #     voice = texttospeech.VoiceSelectionParams(
            #         language_code=voice_lang,
            #         ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            #     )
            #     audio_config = texttospeech.AudioConfig(
            #         audio_encoding=texttospeech.AudioEncoding.MP3
            #     )
            #     response = self.tts_client.synthesize_speech(
            #         input=synthesis_input, voice=voice, audio_config=audio_config
            #     )
            #     return base64.b64encode(response.audio_content).decode()
            
        except Exception as e:
            logger.error(f"Error in text-to-speech: {str(e)}")
            # Return fallback configuration
            fallback_config = {
                "text": text,
                "lang": "en-US",
                "rate": 0.8,
                "pitch": 1.0,
                "volume": 1.0,
                "useWebSpeechAPI": True
            }
            import json
            config_json = json.dumps(fallback_config)
            return base64.b64encode(config_json.encode()).decode()
    
    def _get_language_code(self, language: str) -> str:
        """Convert language code to Google Cloud Speech format"""
        language_mapping = {
            "en": "en-US",
            "hi": "hi-IN", 
            "mr": "mr-IN"
        }
        return language_mapping.get(language, "en-US")
    
    async def analyze_reading_fluency(self, original_text: str, transcribed_text: str) -> dict:
        """
        Analyze reading fluency by comparing original and transcribed text
        
        Args:
            original_text: The text that should have been read
            transcribed_text: The text that was actually transcribed from audio
            
        Returns:
            Dictionary with fluency analysis
        """
        try:
            # Simple analysis - in production, use more sophisticated NLP
            original_words = original_text.lower().split()
            transcribed_words = transcribed_text.lower().split()
            
            # Calculate basic accuracy
            correct_words = 0
            total_words = len(original_words)
            
            for i, word in enumerate(original_words):
                if i < len(transcribed_words) and word == transcribed_words[i]:
                    correct_words += 1
            
            accuracy = (correct_words / total_words) * 100 if total_words > 0 else 0
            
            # Determine fluency level
            if accuracy >= 95:
                fluency_level = "Excellent"
            elif accuracy >= 85:
                fluency_level = "Good"
            elif accuracy >= 70:
                fluency_level = "Needs Improvement"
            else:
                fluency_level = "Poor"
            
            return {
                "accuracy": round(accuracy, 1),
                "fluency_level": fluency_level,
                "correct_words": correct_words,
                "total_words": total_words,
                "mistakes": self._find_mistakes(original_words, transcribed_words)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing reading fluency: {str(e)}")
            return {
                "accuracy": 0,
                "fluency_level": "Error",
                "correct_words": 0,
                "total_words": 0,
                "mistakes": []
            }
    
    def _find_mistakes(self, original_words: list, transcribed_words: list) -> list:
        """Find mistakes in reading by comparing word lists"""
        mistakes = []
        
        for i, original_word in enumerate(original_words):
            if i < len(transcribed_words):
                transcribed_word = transcribed_words[i]
                if original_word != transcribed_word:
                    mistakes.append({
                        "expected": original_word,
                        "actual": transcribed_word,
                        "position": i
                    })
            else:
                mistakes.append({
                    "expected": original_word,
                    "actual": "[skipped]",
                    "position": i
                })
        
        return mistakes 