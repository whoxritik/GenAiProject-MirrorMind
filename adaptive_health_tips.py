from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import random
from emotion_journal import EmotionJournal

class AdaptiveHealthTips:
    """
    Provide adaptive health tips based on emotion patterns and history
    """
    
    def __init__(self, emotion_journal: EmotionJournal):
        self.journal = emotion_journal
        self.emotion_tips = {
            'happy': {
                'maintain': [
                    "🌟 You're radiating positive energy! Keep doing what you're doing.",
                    "😊 Your happiness is wonderful! Share it with others - it's contagious.",
                    "✨ Great mood detected! Use this energy for creative activities.",
                    "🎉 You look fantastic! Remember what contributed to this mood.",
                    "💫 Perfect time to tackle challenging tasks you've been avoiding."
                ],
                'build_on': [
                    "🌱 Consider starting a new positive habit while you're feeling great!",
                    "📝 Journal about what's making you happy to remember for tough days.",
                    "🤝 Reach out to someone you care about and spread the joy.",
                    "🎯 Set a meaningful goal while your confidence is high.",
                    "💪 This is a great time to try something new or challenging."
                ]
            },
            
            'sad': {
                'immediate': [
                    "💙 It's okay to feel down sometimes. Be gentle with yourself.",
                    "🤗 Consider reaching out to a friend or loved one for support.",
                    "🌿 Try some light exercise or go for a walk in nature.",
                    "🛁 Practice self-care: take a warm bath, listen to music, or read.",
                    "📝 Sometimes journaling your thoughts can help process feelings."
                ],
                'persistent': [
                    "💙 You've been feeling down lately. Consider talking to a counselor or therapist.",
                    "🎵 Music therapy might help - create a playlist of uplifting songs.",
                    "🧘‍♀️ Try mindfulness or meditation apps for emotional balance.",
                    "🌅 Establishing a morning routine can help stabilize your mood.",
                    "👥 Consider joining a support group or community activity."
                ],
                'severe': [
                    "💙 You've been experiencing sadness frequently. Please consider professional support.",
                    "📞 Reach out to a mental health professional - you don't have to handle this alone.",
                    "🆘 If you're having thoughts of self-harm, please contact a crisis helpline immediately.",
                    "👨‍⚕️ Talk to your doctor about how you've been feeling lately.",
                    "🤝 Lean on your support network - friends and family want to help."
                ]
            },
            
            'angry': {
                'immediate': [
                    "😤 Take a deep breath. Try counting to 10 or the 4-7-8 breathing technique.",
                    "🏃‍♀️ Physical exercise can be a great outlet for angry energy.",
                    "🚶‍♂️ Step away from stressful situations if possible.",
                    "💪 Try progressive muscle relaxation: tense and release muscle groups.",
                    "🧘‍♂️ Channel this energy productively - clean, organize, or workout."
                ],
                'frequent': [
                    "😤 You've been stressed frequently. Consider stress management techniques.",
                    "🧘‍♀️ Regular meditation or yoga might help manage anger triggers.",
                    "📝 Keep an anger journal to identify patterns and triggers.",
                    "🎯 Consider anger management strategies or counseling.",
                    "💤 Ensure you're getting enough sleep - fatigue increases irritability."
                ],
                'chronic': [
                    "😤 Chronic stress detected. Consider professional stress management support.",
                    "🏥 Talk to a healthcare provider about stress-related health impacts.",
                    "🧠 Cognitive behavioral therapy can be very effective for anger management.",
                    "⚖️ Work-life balance assessment might be needed.",
                    "🌱 Consider lifestyle changes to reduce chronic stressors."
                ]
            },
            
            'tired': {
                'immediate': [
                    "😴 You look exhausted! Consider a 10-20 minute power nap if possible.",
                    "💧 Make sure you're staying hydrated and eating regular meals.",
                    "🌬️ Try some gentle stretching or step outside for fresh air.",
                    "☕ Check your caffeine timing - avoid late-day caffeine.",
                    "🛏️ Prioritize rest today and plan for better sleep tonight."
                ],
                'frequent': [
                    "😴 You've been tired frequently. Review your sleep hygiene habits.",
                    "📱 Consider limiting screen time before bed for better sleep quality.",
                    "🏃‍♀️ Regular exercise can improve energy levels and sleep quality.",
                    "🍎 Evaluate your diet - proper nutrition affects energy levels.",
                    "⏰ Try to maintain consistent sleep and wake times."
                ],
                'chronic': [
                    "😴 Chronic fatigue detected. Consider consulting a healthcare provider.",
                    "🏥 Rule out underlying health conditions that might cause fatigue.",
                    "🧪 Consider sleep study if sleep issues persist.",
                    "💊 Review medications with your doctor - some can cause fatigue.",
                    "🧘‍♀️ Stress and mental health can significantly impact energy levels."
                ]
            },
            
            'neutral': {
                'stable': [
                    "😐 You seem balanced today. This stability is a strength.",
                    "⚖️ Steady mood is great for productivity and decision-making.",
                    "🧘‍♀️ Use this calm state for reflection or planning.",
                    "📚 Good time for learning or tackling detail-oriented tasks.",
                    "🎯 Consider setting goals or organizing your priorities."
                ],
                'encourage': [
                    "🌱 Feeling neutral? Try something that usually brings you joy.",
                    "☀️ Get some sunlight or do a mood-boosting activity.",
                    "🎵 Listen to music or engage in a creative activity.",
                    "🤝 Connect with friends or family to add some social energy.",
                    "🎉 Sometimes neutral is exactly what we need - embrace the calm."
                ]
            },
            
            'surprised': {
                'process': [
                    "😮 Life keeps you on your toes! Take time to process unexpected events.",
                    "🧘‍♀️ Use grounding techniques if the surprise was overwhelming.",
                    "🎢 Embrace life's unpredictability when you can.",
                    "📝 Journal about unexpected events to process them better.",
                    "🌟 Surprise can bring excitement and new opportunities."
                ]
            }
        }
        
        self.pattern_responses = {
            'happy_streak': [
                "🎉 Amazing! You've been consistently happy. Keep nurturing what's working!",
                "✨ Your positive streak is inspiring! What's your secret?",
                "🌟 You're on a happiness roll! Consider sharing your joy with others."
            ],
            'sad_pattern': [
                "💙 I notice you've been feeling down lately. Would you like some support resources?",
                "🤗 Persistent sadness can be tough. Consider reaching out for professional support.",
                "🌱 You've been struggling lately. Remember, it's okay to ask for help."
            ],
            'stress_pattern': [
                "😤 You've been stressed frequently. Let's work on some stress management strategies.",
                "🧘‍♀️ Chronic stress isn't sustainable. Consider meditation or relaxation techniques.",
                "⚖️ Time to evaluate what's causing ongoing stress in your life."
            ],
            'mixed_emotions': [
                "🌈 You're experiencing a variety of emotions - that's perfectly normal!",
                "🎭 Emotional complexity shows you're processing life experiences well.",
                "⚖️ Mixed feelings indicate you're navigating life's ups and downs."
            ]
        }
    
    def get_adaptive_tip(self, current_emotion: str, confidence: float = 0.0) -> Tuple[str, str]:
        """
        Get adaptive tip based on current emotion and historical patterns
        
        Returns:
            Tuple of (tip_text, tip_category)
        """
        try:
            # Get emotion history for pattern analysis
            recent_history = self.journal.get_emotion_history(7)  # Last 7 days
            longer_history = self.journal.get_emotion_history(14)  # Last 14 days
            
            # Analyze patterns
            patterns = self._analyze_emotion_patterns(recent_history, longer_history, current_emotion)
            
            # Get appropriate tip based on patterns
            tip_text = self._select_tip_based_on_pattern(current_emotion, patterns)
            tip_category = self._get_tip_category(patterns)
            
            return tip_text, tip_category
            
        except Exception as e:
            print(f"Error getting adaptive tip: {e}")
            # Fallback to basic tip
            basic_tips = self.emotion_tips.get(current_emotion, {}).get('immediate', ['Take care of yourself today.'])
            return random.choice(basic_tips), 'basic'
    
    def _analyze_emotion_patterns(self, recent_df, longer_df, current_emotion) -> Dict:
        """Analyze emotion patterns and frequency"""
        patterns = {
            'current_emotion': current_emotion,
            'pattern_type': 'stable',
            'frequency': 'normal',
            'trend': 'stable',
            'concern_level': 'none',
            'consecutive_days': 0,
            'dominant_emotion': 'neutral'
        }
        
        if recent_df.empty:
            return patterns
        
        # Calculate frequencies
        recent_counts = recent_df['emotion'].value_counts()
        total_recent = len(recent_df)
        
        # Determine dominant emotion
        if not recent_counts.empty:
            patterns['dominant_emotion'] = recent_counts.index[0]
        
        # Check for concerning patterns
        concerning_emotions = ['sad', 'angry', 'tired']
        
        # Count consecutive days of concerning emotions
        if current_emotion in concerning_emotions:
            consecutive_days = self._count_consecutive_days(recent_df, concerning_emotions)
            patterns['consecutive_days'] = consecutive_days
            
            if consecutive_days >= 3:
                patterns['concern_level'] = 'high'
                patterns['pattern_type'] = 'persistent_negative'
            elif consecutive_days >= 2:
                patterns['concern_level'] = 'moderate'
                patterns['pattern_type'] = 'frequent_negative'
        
        # Check for positive streaks
        if current_emotion == 'happy':
            happy_days = self._count_consecutive_days(recent_df, ['happy'])
            if happy_days >= 3:
                patterns['pattern_type'] = 'positive_streak'
        
        # Determine frequency
        current_emotion_count = recent_counts.get(current_emotion, 0)
        if total_recent > 0:
            frequency_ratio = current_emotion_count / total_recent
            if frequency_ratio > 0.6:
                patterns['frequency'] = 'high'
            elif frequency_ratio > 0.3:
                patterns['frequency'] = 'moderate'
            else:
                patterns['frequency'] = 'low'
        
        # Trend analysis (compare recent vs older data)
        if not longer_df.empty and len(longer_df) > len(recent_df):
            older_period = longer_df[len(recent_df):]
            older_counts = older_period['emotion'].value_counts()
            
            positive_emotions = ['happy', 'surprised']
            negative_emotions = ['sad', 'angry', 'tired']
            
            recent_positive = sum(recent_counts.get(e, 0) for e in positive_emotions)
            recent_negative = sum(recent_counts.get(e, 0) for e in negative_emotions)
            older_positive = sum(older_counts.get(e, 0) for e in positive_emotions)
            older_negative = sum(older_counts.get(e, 0) for e in negative_emotions)
            
            if recent_positive > older_positive and recent_negative < older_negative:
                patterns['trend'] = 'improving'
            elif recent_positive < older_positive and recent_negative > older_negative:
                patterns['trend'] = 'declining'
        
        return patterns
    
    def _count_consecutive_days(self, df, emotions) -> int:
        """Count consecutive days with specific emotions"""
        if df.empty:
            return 0
        
        # Group by date and check if any of the emotions occurred each day
        daily_emotions = df.groupby('date')['emotion'].apply(list).sort_index(ascending=False)
        
        consecutive_count = 0
        for date, day_emotions in daily_emotions.items():
            if any(emotion in emotions for emotion in day_emotions):
                consecutive_count += 1
            else:
                break
        
        return consecutive_count
    
    def _select_tip_based_on_pattern(self, emotion: str, patterns: Dict) -> str:
        """Select appropriate tip based on emotion and patterns"""
        pattern_type = patterns['pattern_type']
        concern_level = patterns['concern_level']
        consecutive_days = patterns['consecutive_days']
        
        # Handle concerning patterns first
        if concern_level == 'high' and emotion in ['sad', 'angry', 'tired']:
            if emotion == 'sad':
                tips = self.emotion_tips[emotion]['severe']
            elif emotion == 'angry':
                tips = self.emotion_tips[emotion]['chronic']
            else:  # tired
                tips = self.emotion_tips[emotion]['chronic']
            return random.choice(tips)
        
        elif concern_level == 'moderate' and emotion in ['sad', 'angry', 'tired']:
            if emotion == 'sad':
                tips = self.emotion_tips[emotion]['persistent']
            elif emotion == 'angry':
                tips = self.emotion_tips[emotion]['frequent']
            else:  # tired
                tips = self.emotion_tips[emotion]['frequent']
            return random.choice(tips)
        
        # Handle positive patterns
        elif pattern_type == 'positive_streak':
            tips = self.emotion_tips['happy']['build_on']
            return random.choice(tips)
        
        # Default to immediate tips
        else:
            emotion_tips = self.emotion_tips.get(emotion, {})
            if 'immediate' in emotion_tips:
                tips = emotion_tips['immediate']
            elif 'stable' in emotion_tips:
                tips = emotion_tips['stable']
            else:
                tips = ["Take care of yourself today. 💚"]
            
            return random.choice(tips)
    
    def _get_tip_category(self, patterns: Dict) -> str:
        """Determine tip category for UI styling"""
        if patterns['concern_level'] == 'high':
            return 'urgent'
        elif patterns['concern_level'] == 'moderate':
            return 'attention'
        elif patterns['pattern_type'] == 'positive_streak':
            return 'celebrate'
        else:
            return 'normal'
    
    def get_weekly_motivation(self) -> str:
        """Get weekly motivational message based on patterns"""
        try:
            insights = self.journal.get_mood_insights(7)
            streaks = self.journal.get_current_streaks()
            
            messages = []
            
            # Check for positive streaks
            if 'positive' in streaks and streaks['positive']['current'] >= 3:
                messages.append(f"🎉 Amazing! You've had {streaks['positive']['current']} days of positive emotions!")
            
            # Check dominant emotion
            dominant = insights.get('dominant_emotion', 'neutral')
            if dominant == 'happy':
                messages.append("😊 You've been radiating happiness this week!")
            elif dominant in ['sad', 'angry']:
                messages.append("💙 This week has been challenging. Remember to be kind to yourself.")
            
            # Total activity
            total = insights.get('total_entries', 0)
            if total > 20:
                messages.append("📊 You're actively monitoring your mental health - that's fantastic!")
            
            if not messages:
                messages = [
                    "🌟 Keep taking care of your mental health!",
                    "💪 Every day is a new opportunity for emotional growth.",
                    "🌱 Small steps in self-awareness lead to big changes."
                ]
            
            return random.choice(messages)
            
        except Exception as e:
            print(f"Error getting weekly motivation: {e}")
            return "🌟 Keep taking care of your mental health!"
    
    def get_personalized_recommendations(self) -> List[str]:
        """Get personalized recommendations based on overall patterns"""
        try:
            insights = self.journal.get_mood_insights(14)
            emotion_dist = insights.get('emotion_distribution', {})
            
            recommendations = []
            
            # Analyze emotional balance
            total_emotions = sum(emotion_dist.values())
            if total_emotions == 0:
                return ["Start tracking your emotions regularly to get personalized insights!"]
            
            # High stress recommendation
            stress_emotions = emotion_dist.get('angry', 0) + emotion_dist.get('tired', 0)
            if stress_emotions / total_emotions > 0.4:
                recommendations.append("🧘‍♀️ Consider regular meditation or stress management techniques")
                recommendations.append("🏃‍♀️ Regular exercise can significantly reduce stress levels")
            
            # Low positive emotions
            positive_emotions = emotion_dist.get('happy', 0) + emotion_dist.get('surprised', 0)
            if positive_emotions / total_emotions < 0.2:
                recommendations.append("🎵 Engage in activities that typically bring you joy")
                recommendations.append("🤝 Connect with friends and family for emotional support")
            
            # High sadness
            if emotion_dist.get('sad', 0) / total_emotions > 0.3:
                recommendations.append("💙 Consider professional counseling or therapy")
                recommendations.append("📝 Journaling can help process difficult emotions")
            
            # Balanced emotions
            if len(emotion_dist) >= 4 and max(emotion_dist.values()) / total_emotions < 0.5:
                recommendations.append("🌈 Your emotional awareness shows great self-insight!")
                recommendations.append("⚖️ You're maintaining good emotional balance")
            
            if not recommendations:
                recommendations = [
                    "🌟 Continue monitoring your emotions for better self-awareness",
                    "💪 You're taking great steps toward mental wellness"
                ]
            
            return recommendations[:3]  # Return top 3 recommendations
            
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return ["Keep taking care of your mental health! 💚"]