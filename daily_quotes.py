import random
from datetime import datetime
from typing import Dict, List

class DailyQuotes:
    """
    Provide motivational daily quotes for the smart mirror
    """
    
    def __init__(self):
        self.quotes = {
            'morning': [
                "🌅 'Today is a new beginning. Make it count!' - Unknown",
                "☀️ 'Every morning is a chance to rewrite your story.' - Anonymous", 
                "🌟 'Rise up and attack the day with enthusiasm!' - Unknown",
                "🌱 'The morning always has a way of creeping up on me and peeking in my bedroom window.' - John Lennon",
                "✨ 'Morning is an important time of day because how you spend your morning can often tell you what kind of day you are going to have.' - Lemony Snicket",
                "🌈 'Each morning brings new potential, but only if you make the most of it.' - Unknown",
                "💫 'Wake up with determination. Go to bed with satisfaction.' - Unknown",
                "🌄 'Today's accomplishments were yesterday's impossibilities.' - Robert H. Schuller"
            ],
            
            'afternoon': [
                "🌞 'The afternoon knows what the morning never suspected.' - Unknown",
                "💪 'Success is the sum of small efforts repeated day in and day out.' - Robert Collier",
                "🎯 'You are never too old to set another goal or to dream a new dream.' - C.S. Lewis",
                "⚡ 'Energy and persistence conquer all things.' - Benjamin Franklin",
                "🚀 'Don't watch the clock; do what it does. Keep going.' - Sam Levenson",
                "🌟 'The only way to do great work is to love what you do.' - Steve Jobs",
                "💎 'Difficult roads often lead to beautiful destinations.' - Zig Ziglar",
                "🔥 'Your limitation—it's only your imagination.' - Unknown"
            ],
            
            'evening': [
                "🌙 'Rest when you're weary. Refresh and renew yourself.' - Unknown",
                "✨ 'The evening is a time of real experimentation.' - Unknown",
                "🌃 'As the sun sets, let your worries fade away.' - Anonymous",
                "💤 'Sleep is the best meditation.' - Dalai Lama",
                "🌟 'End your day with gratitude and begin tomorrow with hope.' - Unknown",
                "🕯️ 'Evening is the time to reflect on the day and prepare for tomorrow.' - Unknown",
                "🌛 'Night is a world lit by itself.' - Antonio Porchia",
                "💫 'The evening's the best part of the day.' - Unknown"
            ],
            
            'motivational': [
                "💪 'Believe you can and you're halfway there.' - Theodore Roosevelt",
                "🎯 'The only impossible journey is the one you never begin.' - Tony Robbins",
                "🌟 'Your mental health is just as important as your physical health.' - Unknown",
                "💖 'You are braver than you believe, stronger than you seem.' - A.A. Milne",
                "🌱 'Progress, not perfection.' - Unknown",
                "✨ 'Self-care is not selfish. You cannot serve from an empty vessel.' - Eleanor Brown",
                "🌈 'Every small positive change can make a big difference.' - Unknown",
                "🦋 'You are not your thoughts. You are the observer of your thoughts.' - Unknown",
                "💡 'Mental health is not a destination but a process.' - Unknown",
                "🌸 'Be patient with yourself. Self-growth is tender.' - Unknown"
            ],
            
            'wellness': [
                "🧘‍♀️ 'Peace comes from within. Do not seek it without.' - Buddha",
                "💚 'Take care of your body. It's the only place you have to live.' - Jim Rohn",
                "🌿 'Mental health is not about what's wrong with you, but what's right with you.' - Unknown",
                "🌊 'You can't calm the storm, so stop trying. Calm yourself and the storm will pass.' - Timber Hawkeye",
                "🌺 'Healing takes time, and asking for help is a courageous step.' - Mariska Hargitay",
                "☯️ 'Balance is not better time management, but better boundary management.' - Betsy Jacobson",
                "🌟 'You are worthy of love and belonging.' - Brené Brown",
                "🦋 'What lies behind us and what lies before us are tiny matters compared to what lies within us.' - Ralph Waldo Emerson"
            ],
            
            'emotion_specific': {
                'happy': [
                    "😊 'Happiness is not something ready-made. It comes from your own actions.' - Dalai Lama",
                    "🎉 'The secret of being happy is accepting where you are in life.' - Unknown",
                    "✨ 'Joy is the simplest form of gratitude.' - Karl Barth",
                    "🌟 'Happiness radiates like the fragrance from a flower.' - Unknown"
                ],
                'sad': [
                    "💙 'It's okay not to be okay. Just don't give up.' - Unknown",
                    "🌧️ 'Storms don't last forever.' - Unknown",
                    "🌱 'Even the darkest night will end and the sun will rise.' - Victor Hugo",
                    "💫 'Your current situation is not your final destination.' - Unknown"
                ],
                'angry': [
                    "🌬️ 'When anger rises, think of the consequences.' - Confucius",
                    "🧘‍♂️ 'You will not be punished for your anger, you will be punished by your anger.' - Buddha",
                    "💨 'Take a deep breath and count to ten.' - Unknown",
                    "⚡ 'Channel your anger into positive action.' - Unknown"
                ],
                'tired': [
                    "😴 'Rest is not idleness, it is restoration.' - Unknown",
                    "🛌 'Sleep is the golden chain that ties health and our bodies together.' - Thomas Dekker",
                    "💤 'Take time to make your soul happy.' - Unknown",
                    "🌙 'Your body needs rest. Your mind needs peace.' - Unknown"
                ],
                'neutral': [
                    "⚖️ 'Sometimes the most productive thing you can do is relax.' - Mark Black",
                    "🧘‍♀️ 'In the midst of movement and chaos, keep stillness inside of you.' - Deepak Chopra",
                    "🌊 'Calm minds bring inner strength and self-confidence.' - Dalai Lama",
                    "🕯️ 'Quiet the mind and the soul will speak.' - Unknown"
                ]
            }
        }
    
    def get_daily_quote(self, emotion: str = None, time_of_day: str = None) -> str:
        """
        Get appropriate daily quote based on emotion and time
        
        Args:
            emotion: Current detected emotion
            time_of_day: Time context ('morning', 'afternoon', 'evening')
        
        Returns:
            Appropriate motivational quote
        """
        try:
            # If specific emotion is provided and we have quotes for it
            if emotion and emotion in self.quotes['emotion_specific']:
                if random.random() < 0.3:  # 30% chance to use emotion-specific quote
                    return random.choice(self.quotes['emotion_specific'][emotion])
            
            # Use time-based quotes if time is provided
            if time_of_day and time_of_day in self.quotes:
                if random.random() < 0.6:  # 60% chance to use time-based quote
                    return random.choice(self.quotes[time_of_day])
            
            # Default to motivational or wellness quotes
            quote_category = random.choice(['motivational', 'wellness'])
            return random.choice(self.quotes[quote_category])
            
        except Exception as e:
            print(f"Error getting daily quote: {e}")
            return "🌟 'Take care of yourself today. You are worth it.' - Unknown"
    
    def get_time_based_quote(self) -> str:
        """Get quote based on current time of day"""
        current_hour = datetime.now().hour
        
        if 5 <= current_hour < 12:
            time_of_day = 'morning'
        elif 12 <= current_hour < 17:
            time_of_day = 'afternoon'  
        else:
            time_of_day = 'evening'
        
        return self.get_daily_quote(time_of_day=time_of_day)
    
    def get_emotion_supportive_quote(self, emotion: str) -> str:
        """Get supportive quote for specific emotion"""
        if emotion in self.quotes['emotion_specific']:
            return random.choice(self.quotes['emotion_specific'][emotion])
        else:
            return self.get_daily_quote()
    
    def get_weekly_inspiration(self) -> str:
        """Get special weekly inspiration message"""
        weekly_quotes = [
            "🌟 'This week is a blank canvas. Paint it with your dreams!' - Unknown",
            "💪 'A week of small progress is still progress.' - Unknown",
            "🌱 'Every week is a new opportunity to grow.' - Unknown",
            "✨ 'Make this week amazing, one day at a time.' - Unknown",
            "🎯 'Focus on progress, not perfection this week.' - Unknown",
            "🌈 'Let this week be full of possibilities and positive energy.' - Unknown",
            "💫 'Week by week, you're becoming who you're meant to be.' - Unknown"
        ]
        
        return random.choice(weekly_quotes)
    
    def format_quote_for_display(self, quote: str, is_main_display: bool = True) -> str:
        """Format quote for UI display"""
        if is_main_display:
            return f"""
            <div style="
                background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(20, 184, 166, 0.1));
                border-left: 4px solid #06B6D4;
                padding: 15px 20px;
                margin: 15px 0;
                border-radius: 8px;
                font-style: italic;
                text-align: center;
                box-shadow: 0 2px 10px rgba(6, 182, 212, 0.2);
            ">
                <div style="color: #E5E7EB; font-size: 1.1rem; line-height: 1.4;">
                    {quote}
                </div>
            </div>
            """
        else:
            return f"""
            <div style="
                color: #06B6D4;
                font-style: italic;
                text-align: center;
                padding: 10px;
                font-size: 0.95rem;
            ">
                {quote}
            </div>
            """