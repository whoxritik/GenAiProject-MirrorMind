from typing import Dict, Tuple
import random

class BilingualMessageHandler:
    """
    Handle bilingual emotion messages in English and Hindi
    """
    
    def __init__(self):
        self.emotion_messages = {
            'happy': [
                ("You look happy today, keep it up!", "Aaj aap khush dikh rahe ho, aise hi bane rahiye!"),
                ("Great positive energy detected!", "Bahut acchi positive energy dekhi ja rahi hai!"),
                ("Your smile is contagious!", "Aapki muskurahat bahut pyaari hai!"),
                ("What a wonderful mood!", "Kitna sundar mood hai aapka!"),
                ("Keep spreading that joy!", "Is khushi ko failate rahiye!")
            ],
            
            'sad': [
                ("You seem a bit down today, take care of yourself.", "Aaj aap thode udaas lag rahe ho, apna khayal rakhiye."),
                ("It's okay to feel low sometimes.", "Kabhi kabhi udaas feel karna normal hai."),
                ("Remember, this feeling will pass.", "Yaad rakhiye, ye feeling kuch samay baad chali jayegi."),
                ("You're stronger than you think.", "Aap jitna sochte hai usse zyada strong hai."),
                ("Tomorrow will be a better day.", "Kal ka din behtar hoga.")
            ],
            
            'angry': [
                ("You seem a bit stressed today, try some deep breathing.", "Aaj aap thode stressed lag rahe ho, gehri saans lene ki koshish kijiye."),
                ("Take a moment to calm down.", "Thoda sa shaant hone ki koshish kijiye."),
                ("Deep breaths can help reduce stress.", "Gehri saans lene se stress kam ho sakta hai."),
                ("Try counting to ten slowly.", "Das tak ginti karne ki koshish kijiye."),
                ("Channel this energy into something positive.", "Is energy ko kisi positive kaam me lagaye.")
            ],
            
            'tired': [
                ("You look exhausted, please rest.", "Aap thake hue lag rahe ho, thoda aaram kijiye."),
                ("Consider taking a short break.", "Thoda sa break lene ki sochiye."),
                ("Make sure you're getting enough sleep.", "Puri neend lene ka khayal rakhiye."),
                ("Your body needs some rest.", "Aapke sharir ko aaram ki zarurat hai."),
                ("Hydrate and rest well.", "Paani piye aur acche se aaram kijiye.")
            ],
            
            'neutral': [
                ("You look calm and centered today.", "Aaj aap shaant aur balanced lag rahe ho."),
                ("A steady mood is good for productivity.", "Steady mood productivity ke liye accha hai."),
                ("You seem well-balanced.", "Aap bilkul balanced lag rahe ho."),
                ("This stability is a strength.", "Ye stability ek strength hai."),
                ("Keep maintaining this balance.", "Is balance ko banakar rakhiye.")
            ],
            
            'surprised': [
                ("Life keeps you on your toes!", "Zindagi me surprises aate rahte hai!"),
                ("Unexpected moments make life interesting.", "Achanak ke moments zindagi ko interesting banate hai."),
                ("Take time to process what just happened.", "Jo hua hai usse samjhne ke liye time lijiye."),
                ("Surprise can be energizing.", "Surprise energy de sakta hai."),
                ("Embrace the unexpected.", "Achanak ki cheezoo ko accept kijiye.")
            ],
            
            'fear': [
                ("Don't worry, you'll get through this.", "Pareshan mat hoiye, aap ye kar payenge."),
                ("Take deep breaths and stay grounded.", "Gehri saans lijiye aur grounded rahiye."),
                ("Fear is natural, but you're brave.", "Dar natural hai, lekin aap brave hai."),
                ("Focus on what you can control.", "Jo aap control kar sakte hai uspe focus kijiye."),
                ("You have the strength to overcome this.", "Aap me is se bahar aane ki shakti hai.")
            ]
        }
    
    def get_bilingual_message(self, emotion: str) -> Tuple[str, str]:
        """
        Get bilingual message for detected emotion
        
        Args:
            emotion: Detected emotion label
            
        Returns:
            Tuple of (english_message, hindi_message)
        """
        if emotion in self.emotion_messages:
            return random.choice(self.emotion_messages[emotion])
        else:
            # Default message for unknown emotions
            return (
                "Take care of yourself today.",
                "Aaj apna khayal rakhiye."
            )
    
    def format_bilingual_display(self, emotion: str) -> str:
        """
        Format bilingual message for display
        
        Args:
            emotion: Detected emotion label
            
        Returns:
            Formatted HTML string with both languages
        """
        english_msg, hindi_msg = self.get_bilingual_message(emotion)
        
        return f"""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 1.2rem; margin-bottom: 10px; color: #FFFFFF;">
                <strong>🗣️ English:</strong> {english_msg}
            </div>
            <div style="font-size: 1.1rem; color: #06B6D4; font-style: italic;">
                <strong>हिंदी:</strong> {hindi_msg}
            </div>
        </div>
        """
    
    def get_combined_text_for_tts(self, emotion: str) -> str:
        """
        Get combined text for text-to-speech (English only for better pronunciation)
        
        Args:
            emotion: Detected emotion label
            
        Returns:
            English text for TTS
        """
        english_msg, _ = self.get_bilingual_message(emotion)
        return english_msg