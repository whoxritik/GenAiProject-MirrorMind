import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional

class MoodTracker:
    """
    Track and analyze mood patterns over time
    """
    
    def __init__(self, data_file: str = "mood_data.json"):
        self.data_file = data_file
        self.mood_history = self._load_data()
        
    def _load_data(self) -> List[Dict]:
        """Load mood data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            print(f"Error loading mood data: {e}")
            return []
    
    def _save_data(self):
        """Save mood data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.mood_history, f, default=str, indent=2)
        except Exception as e:
            print(f"Error saving mood data: {e}")
    
    def record_mood(self, emotion: str, confidence: float, notes: str = ""):
        """
        Record a new mood entry
        
        Args:
            emotion: Detected emotion label
            confidence: Confidence score (0.0 to 1.0)
            notes: Optional user notes
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'emotion': emotion,
            'confidence': confidence,
            'notes': notes,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'hour': datetime.now().hour
        }
        
        self.mood_history.append(entry)
        self._save_data()
    
    def get_daily_stats(self, date: Optional[str] = None) -> Dict[str, int]:
        """
        Get mood statistics for a specific date
        
        Args:
            date: Date in 'YYYY-MM-DD' format. If None, uses today.
            
        Returns:
            Dictionary mapping emotions to their frequency counts
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        daily_moods = [entry for entry in self.mood_history if entry['date'] == date]
        
        emotion_counts = {}
        for entry in daily_moods:
            emotion = entry['emotion']
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        return emotion_counts
    
    def get_mood_trends(self, days: int = 7) -> pd.DataFrame:
        """
        Get mood trends over the specified number of days
        
        Args:
            days: Number of days to look back
            
        Returns:
            DataFrame with timestamp and emotion frequency data
        """
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Filter data within date range
            filtered_data = []
            for entry in self.mood_history:
                entry_time = datetime.fromisoformat(entry['timestamp'])
                if start_date <= entry_time <= end_date:
                    filtered_data.append(entry)
            
            if not filtered_data:
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(filtered_data)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Group by hour and count emotions
            df_hourly = df.groupby([df['timestamp'].dt.floor('H'), 'emotion']).size().unstack(fill_value=0)
            df_hourly = df_hourly.reset_index()
            
            return df_hourly
            
        except Exception as e:
            print(f"Error getting mood trends: {e}")
            return pd.DataFrame()
    
    def get_weekly_summary(self) -> Dict:
        """
        Get weekly mood summary with insights
        
        Returns:
            Dictionary with weekly statistics and insights
        """
        week_data = self.get_mood_trends(7)
        
        if week_data.empty:
            return {
                'total_entries': 0,
                'dominant_emotion': 'neutral',
                'mood_diversity': 0,
                'insights': ["No mood data available for the past week."]
            }
        
        # Calculate statistics
        emotion_cols = [col for col in week_data.columns if col != 'timestamp']
        total_entries = week_data[emotion_cols].sum().sum()
        
        if total_entries > 0:
            emotion_totals = week_data[emotion_cols].sum()
            dominant_emotion = emotion_totals.idxmax()
            mood_diversity = len(emotion_totals[emotion_totals > 0])
            
            # Generate insights
            insights = self._generate_insights(emotion_totals, total_entries)
            
            return {
                'total_entries': int(total_entries),
                'dominant_emotion': dominant_emotion,
                'mood_diversity': mood_diversity,
                'emotion_breakdown': emotion_totals.to_dict(),
                'insights': insights
            }
        else:
            return {
                'total_entries': 0,
                'dominant_emotion': 'neutral',
                'mood_diversity': 0,
                'insights': ["No mood entries recorded this week."]
            }
    
    def _generate_insights(self, emotion_totals: pd.Series, total_entries: int) -> List[str]:
        """Generate personalized insights based on mood data"""
        insights = []
        
        # Calculate percentages
        percentages = (emotion_totals / total_entries * 100).round(1)
        
        # Dominant emotion insight
        dominant = percentages.idxmax()
        dominant_pct = percentages[dominant]
        
        if dominant_pct > 50:
            insights.append(f"You've been predominantly {dominant} this week ({dominant_pct}% of the time).")
        
        # Emotional balance insight
        if percentages.get('happy', 0) > 30:
            insights.append("Great job maintaining positive emotions this week! 😊")
        elif percentages.get('happy', 0) < 10 and percentages.get('sad', 0) > 20:
            insights.append("Consider activities that boost your mood - perhaps exercise, music, or connecting with friends.")
        
        # Stress indicators
        if percentages.get('angry', 0) > 20 or percentages.get('tired', 0) > 30:
            insights.append("You might be experiencing elevated stress. Consider relaxation techniques or better sleep habits.")
        
        # Consistency insight
        non_zero_emotions = len(percentages[percentages > 5])
        if non_zero_emotions >= 4:
            insights.append("Your emotions show healthy variation - this is normal and indicates emotional awareness.")
        
        return insights if insights else ["Keep tracking your emotions to gain more insights!"]
    
    def get_hourly_patterns(self) -> Dict[int, Dict[str, int]]:
        """
        Analyze mood patterns by hour of day
        
        Returns:
            Dictionary mapping hours to emotion frequency
        """
        hourly_patterns = {}
        
        for entry in self.mood_history:
            hour = entry['hour']
            emotion = entry['emotion']
            
            if hour not in hourly_patterns:
                hourly_patterns[hour] = {}
            
            hourly_patterns[hour][emotion] = hourly_patterns[hour].get(emotion, 0) + 1
        
        return hourly_patterns
    
    def export_data(self, format: str = 'csv') -> str:
        """
        Export mood data in specified format
        
        Args:
            format: Export format ('csv', 'json')
            
        Returns:
            Filename of exported data
        """
        try:
            if format.lower() == 'csv':
                df = pd.DataFrame(self.mood_history)
                filename = f"mood_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df.to_csv(filename, index=False)
                return filename
            
            elif format.lower() == 'json':
                filename = f"mood_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(filename, 'w') as f:
                    json.dump(self.mood_history, f, indent=2, default=str)
                return filename
            
            else:
                raise ValueError("Unsupported format. Use 'csv' or 'json'.")
                
        except Exception as e:
            print(f"Error exporting data: {e}")
            return ""
    
    def clear_old_data(self, days: int = 90):
        """
        Remove mood data older than specified days
        
        Args:
            days: Number of days to retain
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        self.mood_history = [
            entry for entry in self.mood_history 
            if datetime.fromisoformat(entry['timestamp']) >= cutoff_date
        ]
        
        self._save_data()
        print(f"Cleared mood data older than {days} days.")
