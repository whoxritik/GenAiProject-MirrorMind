import random
from typing import Dict, List
from datetime import datetime

class HealthTips:
    """
    Provide personalized health tips based on detected emotions and patterns
    """
    
    def __init__(self):
        self.emotion_tips = {
            'happy': [
                "You're radiating positive energy! Share your joy with others - it's contagious. 😊",
                "Great mood detected! This is a perfect time for creative activities or learning something new.",
                "Your happiness is wonderful! Consider capturing this moment in a journal or photo.",
                "Positive vibes detected! Use this energy to tackle challenging tasks you've been avoiding.",
                "You look fantastic! Remember what contributed to this mood for future reference."
            ],
            
            'neutral': [
                "Steady as you go! Sometimes neutral is exactly what we need. Take time to check in with yourself.",
                "You seem balanced today. This is a great time for planning or organizing your thoughts.",
                "Neutral energy detected. Consider doing something that usually brings you joy.",
                "You appear calm and centered. Perfect time for meditation or mindful breathing.",
                "Balanced mood observed. Use this stability to tackle routine tasks efficiently."
            ],
            
            'sad': [
                "It's okay to feel down sometimes. Consider reaching out to a friend or loved one. 💙",
                "Gentle reminder: This feeling is temporary. Try some light exercise or go for a walk in nature.",
                "You might benefit from some self-care today. Take a warm bath, listen to music, or practice gratitude.",
                "It's normal to have low moments. Consider journaling your thoughts or talking to someone you trust.",
                "Sending you virtual support. Remember past times you overcame difficulties - you're stronger than you know."
            ],
            
            'angry': [
                "Take a deep breath. Try counting to 10 or practice the 4-7-8 breathing technique. 😤➜😌",
                "Feeling frustrated? Physical exercise can be a great outlet for angry energy.",
                "Step away from stressful situations if possible. Sometimes perspective comes with distance.",
                "Try progressive muscle relaxation: tense and release each muscle group for 5 seconds.",
                "Channel this energy productively - clean, organize, or tackle a challenging workout."
            ],
            
            'tired': [
                "You look exhausted! Consider taking a 10-20 minute power nap if possible. 😴",
                "Fatigue detected. Make sure you're staying hydrated and getting adequate sleep tonight.",
                "Low energy observed. Try some gentle stretching or step outside for fresh air.",
                "Consider checking your caffeine and meal timing - small frequent meals can help energy levels.",
                "Prioritize rest today. Your body might be telling you to slow down and recharge."
            ],
            
            'surprised': [
                "Life keeps you on your toes! Take a moment to process unexpected events. ✨",
                "Surprise can be energizing! Use this heightened awareness for focused tasks.",
                "Unexpected moments make life interesting. Embrace the spontaneity when possible.",
                "Take time to process new information or changes. Deep breaths help with adjustment.",
                "Surprise can trigger stress. If needed, use grounding techniques like naming 5 things you can see."
            ],
            
            'fear': [
                "Fear is your mind's way of protecting you. Take slow, deep breaths and ground yourself. 🛡️",
                "Try the 5-4-3-2-1 technique: 5 things you see, 4 you hear, 3 you feel, 2 you smell, 1 you taste.",
                "Remember that most fears are about future events. Focus on what you can control right now.",
                "Consider talking to someone you trust about what's worrying you. Sharing often helps.",
                "Practice self-compassion. It's normal to feel afraid sometimes - you're being human."
            ]
        }
        
        self.general_wellness_tips = [
            "Stay hydrated! Aim for 8 glasses of water throughout the day. 💧",
            "Take breaks from screens every 20 minutes - look at something 20 feet away for 20 seconds.",
            "Practice gratitude: think of 3 things you're thankful for today. 🙏",
            "Get some sunlight if possible - it helps regulate your circadian rhythm. ☀️",
            "Remember to stand and stretch every hour if you're sitting for long periods.",
            "Deep breathing exercises can instantly calm your nervous system. Try it now! 🧘‍♀️",
            "A 10-minute walk can significantly boost your mood and energy levels. 🚶‍♀️",
            "Limit multitasking - focus on one task at a time for better mental clarity.",
            "Connect with nature, even if it's just looking at plants or trees through a window. 🌿"
        ]
        
        self.time_based_tips = {
            'morning': [
                "Start your day with intention! Set 1-3 priorities for today. 🌅",
                "Morning sunlight helps regulate your sleep-wake cycle. Step outside if you can!",
                "Consider starting with gentle stretches or movement to wake up your body.",
                "Hydrate first thing - your body has been fasting all night. 💧"
            ],
            'afternoon': [
                "Afternoon energy dip is normal! Try a brief walk or healthy snack. 🍎",
                "Perfect time for your most challenging tasks - your brain is typically sharp now.",
                "If you're feeling sluggish, try standing or doing desk exercises. 💪",
                "Don't forget to eat lunch if you haven't - your brain needs fuel!"
            ],
            'evening': [
                "Wind down time! Consider dimming lights and reducing screen time. 🌙",
                "Evening reflection: what went well today? What are you grateful for?",
                "Prepare for tomorrow to reduce morning stress - lay out clothes, prep breakfast. 📋",
                "Start your bedtime routine 1 hour before sleep for better rest quality."
            ]
        }
    
    def get_tip(self, emotion: str, include_general: bool = True) -> str:
        """
        Get a personalized tip based on detected emotion
        
        Args:
            emotion: Detected emotion label
            include_general: Whether to sometimes include general wellness tips
            
        Returns:
            Personalized health tip string
        """
        tips = []
        
        # Add emotion-specific tips
        if emotion in self.emotion_tips:
            tips.extend(self.emotion_tips[emotion])
        
        # Add time-based tips
        current_hour = datetime.now().hour
        if 5 <= current_hour < 12:
            tips.extend(self.time_based_tips['morning'])
        elif 12 <= current_hour < 17:
            tips.extend(self.time_based_tips['afternoon'])
        else:
            tips.extend(self.time_based_tips['evening'])
        
        # Sometimes add general wellness tips
        if include_general and random.random() < 0.3:
            tips.extend(self.general_wellness_tips)
        
        # Return random tip from available options
        return random.choice(tips) if tips else "Take care of yourself today! 💚"
    
    def get_contextual_tip(self, emotion: str, confidence: float, time_of_day: str = None) -> str:
        """
        Get a more contextual tip based on emotion and confidence level
        
        Args:
            emotion: Detected emotion
            confidence: Confidence level (0.0 to 1.0)
            time_of_day: Optional time context ('morning', 'afternoon', 'evening')
            
        Returns:
            Contextual health tip
        """
        base_tip = self.get_tip(emotion)
        
        # Adjust based on confidence level
        if confidence < 0.5:
            uncertainty_tips = [
                "Your emotions seem mixed right now - that's perfectly normal! Take a moment to check in with yourself.",
                "It's okay to feel uncertain about your emotions. Sometimes we experience multiple feelings at once.",
                "Mixed signals detected - consider what might be contributing to these complex feelings."
            ]
            return random.choice(uncertainty_tips)
        
        # Add time-specific context if provided
        if time_of_day and time_of_day in self.time_based_tips:
            time_tips = self.time_based_tips[time_of_day]
            if random.random() < 0.5:  # 50% chance to use time-specific tip
                return random.choice(time_tips)
        
        return base_tip
    
    def get_weekly_recommendations(self, dominant_emotion: str, mood_diversity: int) -> List[str]:
        """
        Get weekly recommendations based on mood patterns
        
        Args:
            dominant_emotion: Most frequent emotion this week
            mood_diversity: Number of different emotions experienced
            
        Returns:
            List of weekly recommendations
        """
        recommendations = []
        
        # Based on dominant emotion
        if dominant_emotion == 'happy':
            recommendations.append("🌟 You've had a great week! Consider sharing your positive strategies with others.")
        elif dominant_emotion == 'sad':
            recommendations.append("💙 You've had some tough moments. Be gentle with yourself and consider seeking support.")
        elif dominant_emotion == 'angry':
            recommendations.append("😤 High stress detected. Focus on stress management techniques this week.")
        elif dominant_emotion == 'tired':
            recommendations.append("😴 Fatigue seems to be a pattern. Prioritize sleep hygiene and energy management.")
        
        # Based on mood diversity
        if mood_diversity <= 2:
            recommendations.append("🎭 Your emotions have been fairly consistent. Consider activities that bring variety to your routine.")
        elif mood_diversity >= 5:
            recommendations.append("🌈 You've experienced a wide range of emotions - this shows healthy emotional awareness!")
        
        # General weekly recommendations
        weekly_general = [
            "📅 Plan some self-care activities for the upcoming week.",
            "🎯 Set realistic goals that support your mental well-being.",
            "🤝 Schedule time to connect with friends or family.",
            "🧘‍♀️ Consider adding a mindfulness practice to your routine.",
            "📚 Learn about emotional intelligence and self-awareness techniques."
        ]
        
        recommendations.extend(random.sample(weekly_general, 2))
        
        return recommendations
    
    def get_emergency_resources(self) -> Dict[str, str]:
        """
        Get emergency mental health resources
        
        Returns:
            Dictionary of crisis resources
        """
        return {
            'crisis_hotline': 'National Suicide Prevention Lifeline: 988',
            'crisis_text': 'Crisis Text Line: Text HOME to 741741',
            'emergency': 'Emergency Services: 911',
            'online_support': 'Visit crisis.org for online support',
            'disclaimer': 'This app is not a substitute for professional mental health care.'
        }
    
    def format_tip_with_emoji(self, tip: str) -> str:
        """
        Ensure tips have appropriate emojis for better visual appeal
        
        Args:
            tip: Original tip text
            
        Returns:
            Tip with emoji if not already present
        """
        if any(char in tip for char in ['😊', '😌', '💙', '😤', '😴', '✨', '🛡️', '💧', '🙏', '☀️', '🧘‍♀️', '🚶‍♀️', '🌿', '🌅', '🍎', '💪', '🌙', '📋', '💚']):
            return tip  # Already has emoji
        
        # Add appropriate emoji based on content
        if 'happy' in tip.lower() or 'joy' in tip.lower():
            return f"😊 {tip}"
        elif 'calm' in tip.lower() or 'peace' in tip.lower():
            return f"😌 {tip}"
        elif 'water' in tip.lower() or 'hydrat' in tip.lower():
            return f"💧 {tip}"
        elif 'exercise' in tip.lower() or 'walk' in tip.lower():
            return f"🚶‍♀️ {tip}"
        elif 'breath' in tip.lower():
            return f"🧘‍♀️ {tip}"
        else:
            return f"💡 {tip}"
