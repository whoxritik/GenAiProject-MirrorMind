import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from typing import List, Dict, Optional, Tuple
import streamlit as st

class EmotionJournal:
    """
    Handle emotion logging and journal functionality with SQLite database
    """
    
    def __init__(self, db_path: str = "emotion_journal.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the SQLite database with required tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create emotions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS emotions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    date DATE,
                    emotion TEXT NOT NULL,
                    confidence REAL,
                    notes TEXT,
                    session_id TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create journal_entries table for manual entries
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS journal_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE,
                    mood_rating INTEGER,
                    notes TEXT,
                    tags TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create mood_streaks table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mood_streaks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    streak_type TEXT,
                    start_date DATE,
                    end_date DATE,
                    current_count INTEGER,
                    best_count INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error initializing database: {e}")
    
    def log_emotion(self, emotion: str, confidence: float = 0.0, notes: str = "", session_id: str = ""):
        """Log detected emotion to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            current_time = datetime.now()
            current_date = current_time.date()
            
            cursor.execute('''
                INSERT INTO emotions (timestamp, date, emotion, confidence, notes, session_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (current_time, current_date, emotion, confidence, notes, session_id))
            
            conn.commit()
            conn.close()
            
            # Update mood streaks
            self.update_mood_streaks(emotion, current_date)
            
        except Exception as e:
            print(f"Error logging emotion: {e}")
    
    def get_emotion_history(self, days: int = 30) -> pd.DataFrame:
        """Get emotion history for specified number of days"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)
            
            query = '''
                SELECT timestamp, date, emotion, confidence, notes
                FROM emotions 
                WHERE date >= ? AND date <= ?
                ORDER BY timestamp DESC
            '''
            
            df = pd.read_sql_query(query, conn, params=(start_date, end_date))
            conn.close()
            
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df['date'] = pd.to_datetime(df['date'])
            
            return df
            
        except Exception as e:
            print(f"Error getting emotion history: {e}")
            return pd.DataFrame()
    
    def get_daily_emotion_summary(self, days: int = 7) -> pd.DataFrame:
        """Get daily emotion summary with counts"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)
            
            query = '''
                SELECT date, emotion, COUNT(*) as count
                FROM emotions 
                WHERE date >= ? AND date <= ?
                GROUP BY date, emotion
                ORDER BY date DESC
            '''
            
            df = pd.read_sql_query(query, conn, params=(start_date, end_date))
            conn.close()
            
            return df
            
        except Exception as e:
            print(f"Error getting daily summary: {e}")
            return pd.DataFrame()
    
    def get_mood_insights(self, days: int = 7) -> Dict:
        """Get mood insights and analytics"""
        try:
            df = self.get_emotion_history(days)
            
            if df.empty:
                return {
                    'total_entries': 0,
                    'dominant_emotion': 'neutral',
                    'average_confidence': 0.0,
                    'emotion_distribution': {},
                    'daily_averages': {},
                    'insights': ["No data available for analysis."]
                }
            
            # Calculate insights
            total_entries = len(df)
            emotion_counts = df['emotion'].value_counts()
            dominant_emotion = emotion_counts.index[0] if not emotion_counts.empty else 'neutral'
            average_confidence = df['confidence'].mean()
            
            # Daily averages
            daily_counts = df.groupby('date')['emotion'].count()
            daily_averages = {
                'avg_detections_per_day': daily_counts.mean(),
                'most_active_day': daily_counts.idxmax() if not daily_counts.empty else None
            }
            
            # Generate insights
            insights = self._generate_mood_insights(df, emotion_counts, days)
            
            return {
                'total_entries': total_entries,
                'dominant_emotion': dominant_emotion,
                'average_confidence': round(average_confidence, 2),
                'emotion_distribution': emotion_counts.to_dict(),
                'daily_averages': daily_averages,
                'insights': insights
            }
            
        except Exception as e:
            print(f"Error getting mood insights: {e}")
            return {'total_entries': 0, 'insights': [f"Error analyzing data: {e}"]}
    
    def _generate_mood_insights(self, df: pd.DataFrame, emotion_counts: pd.Series, days: int) -> List[str]:
        """Generate personalized mood insights"""
        insights = []
        total_entries = len(df)
        
        if total_entries == 0:
            return ["No mood data available yet."]
        
        # Dominant emotion insight
        dominant = emotion_counts.index[0]
        dominant_pct = (emotion_counts[dominant] / total_entries) * 100
        
        emotion_emojis = {
            'happy': '😊', 'sad': '😔', 'angry': '😡', 
            'neutral': '😐', 'tired': '😴', 'surprised': '😮'
        }
        
        emoji = emotion_emojis.get(dominant, '🙂')
        insights.append(f"{emoji} You've been predominantly {dominant} ({dominant_pct:.1f}% of the time)")
        
        # Trend analysis
        if len(df) >= 2:
            recent_emotions = df.head(5)['emotion'].tolist()
            if len(set(recent_emotions)) == 1:
                insights.append(f"🔄 Your mood has been consistent recently")
            else:
                insights.append(f"🌈 Your emotions show healthy variation")
        
        # Positive vs negative ratio
        positive_emotions = ['happy', 'surprised']
        negative_emotions = ['sad', 'angry', 'tired']
        
        positive_count = sum(emotion_counts.get(e, 0) for e in positive_emotions)
        negative_count = sum(emotion_counts.get(e, 0) for e in negative_emotions)
        
        if positive_count > negative_count:
            insights.append("✨ You're experiencing more positive emotions - keep it up!")
        elif negative_count > positive_count * 2:
            insights.append("💙 Consider some self-care activities to boost your mood")
        
        # Weekly comparison
        if days >= 7:
            insights.append(f"📊 You had {total_entries} emotion detections in the last {days} days")
        
        return insights
    
    def update_mood_streaks(self, emotion: str, date):
        """Update mood streak counters"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Define positive and negative emotions
            positive_emotions = ['happy', 'surprised']
            negative_emotions = ['sad', 'angry']
            
            if emotion in positive_emotions:
                streak_type = 'positive'
            elif emotion in negative_emotions:
                streak_type = 'negative'
            else:
                streak_type = 'neutral'
            
            # Get current streak
            cursor.execute('''
                SELECT * FROM mood_streaks 
                WHERE streak_type = ? 
                ORDER BY created_at DESC 
                LIMIT 1
            ''', (streak_type,))
            
            current_streak = cursor.fetchone()
            
            if current_streak:
                # Update existing streak
                streak_id, _, start_date, end_date, current_count, best_count, _ = current_streak
                
                # Check if streak continues (within 2 days)
                last_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                if (date - last_date).days <= 2:
                    new_count = current_count + 1
                    new_best = max(best_count, new_count)
                    
                    cursor.execute('''
                        UPDATE mood_streaks 
                        SET end_date = ?, current_count = ?, best_count = ?
                        WHERE id = ?
                    ''', (date, new_count, new_best, streak_id))
                else:
                    # Start new streak
                    cursor.execute('''
                        INSERT INTO mood_streaks (streak_type, start_date, end_date, current_count, best_count)
                        VALUES (?, ?, ?, 1, ?)
                    ''', (streak_type, date, date, max(1, best_count)))
            else:
                # Create first streak
                cursor.execute('''
                    INSERT INTO mood_streaks (streak_type, start_date, end_date, current_count, best_count)
                    VALUES (?, ?, ?, 1, 1)
                ''', (streak_type, date, date))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error updating mood streaks: {e}")
    
    def get_current_streaks(self) -> Dict:
        """Get current mood streaks"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT streak_type, current_count, best_count, start_date, end_date
                FROM mood_streaks 
                WHERE current_count > 0
                ORDER BY created_at DESC
            ''')
            
            streaks = cursor.fetchall()
            conn.close()
            
            streak_data = {}
            for streak_type, current, best, start, end in streaks:
                streak_data[streak_type] = {
                    'current': current,
                    'best': best,
                    'start_date': start,
                    'end_date': end
                }
            
            return streak_data
            
        except Exception as e:
            print(f"Error getting streaks: {e}")
            return {}
    
    def export_to_csv(self, days: int = 30) -> str:
        """Export emotion data to CSV file"""
        try:
            df = self.get_emotion_history(days)
            
            if df.empty:
                return ""
            
            filename = f"emotion_journal_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(filename, index=False)
            
            return filename
            
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return ""
    
    def create_emotion_heatmap(self, days: int = 30) -> go.Figure:
        """Create calendar heatmap of emotions"""
        try:
            df = self.get_daily_emotion_summary(days)
            
            if df.empty:
                fig = go.Figure()
                fig.add_annotation(
                    text="No emotion data available",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5, showarrow=False,
                    font=dict(size=16, color="gray")
                )
                return fig
            
            # Create pivot table for heatmap
            pivot_df = df.pivot_table(
                index='emotion', 
                columns='date', 
                values='count', 
                fill_value=0
            )
            
            # Create heatmap
            fig = go.Figure(data=go.Heatmap(
                z=pivot_df.values,
                x=pivot_df.columns,
                y=pivot_df.index,
                colorscale='Blues',
                showscale=True,
                hoverongaps=False
            ))
            
            fig.update_layout(
                title="Emotion Calendar Heatmap",
                xaxis_title="Date",
                yaxis_title="Emotion",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#E5E7EB',
                title_font_color='#FFFFFF'
            )
            
            return fig
            
        except Exception as e:
            print(f"Error creating heatmap: {e}")
            return go.Figure()
    
    def get_weekly_comparison(self) -> Dict:
        """Compare this week with last week"""
        try:
            today = datetime.now().date()
            
            # This week
            this_week_start = today - timedelta(days=today.weekday())
            this_week_emotions = self.get_emotion_history(7)
            
            # Last week  
            last_week_start = this_week_start - timedelta(days=7)
            last_week_end = this_week_start - timedelta(days=1)
            
            conn = sqlite3.connect(self.db_path)
            last_week_query = '''
                SELECT emotion, COUNT(*) as count
                FROM emotions 
                WHERE date >= ? AND date <= ?
                GROUP BY emotion
            '''
            
            last_week_df = pd.read_sql_query(
                last_week_query, 
                conn, 
                params=(last_week_start, last_week_end)
            )
            conn.close()
            
            # Calculate changes
            this_week_counts = this_week_emotions['emotion'].value_counts() if not this_week_emotions.empty else pd.Series()
            last_week_counts = last_week_df.set_index('emotion')['count'] if not last_week_df.empty else pd.Series()
            
            comparison = {
                'this_week_total': len(this_week_emotions),
                'last_week_total': last_week_counts.sum() if not last_week_counts.empty else 0,
                'emotion_changes': {},
                'overall_trend': 'stable'
            }
            
            # Calculate emotion changes
            all_emotions = set(this_week_counts.index) | set(last_week_counts.index)
            for emotion in all_emotions:
                this_week = this_week_counts.get(emotion, 0)
                last_week = last_week_counts.get(emotion, 0)
                change = this_week - last_week
                comparison['emotion_changes'][emotion] = {
                    'this_week': this_week,
                    'last_week': last_week,
                    'change': change
                }
            
            # Determine overall trend
            positive_change = sum(1 for e in ['happy', 'surprised'] 
                                if comparison['emotion_changes'].get(e, {}).get('change', 0) > 0)
            negative_change = sum(1 for e in ['sad', 'angry', 'tired'] 
                                if comparison['emotion_changes'].get(e, {}).get('change', 0) > 0)
            
            if positive_change > negative_change:
                comparison['overall_trend'] = 'improving'
            elif negative_change > positive_change:
                comparison['overall_trend'] = 'declining'
            
            return comparison
            
        except Exception as e:
            print(f"Error getting weekly comparison: {e}")
            return {'this_week_total': 0, 'last_week_total': 0, 'emotion_changes': {}}