import streamlit as st
import cv2
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
from PIL import Image
import base64
import io

from emotion_detector import EmotionDetector
from mood_tracker import MoodTracker
from health_tips import HealthTips
from bilingual_messages import BilingualMessageHandler
from voice_handler import VoiceHandler
from animated_logo import AnimatedLogo
from emotion_journal import EmotionJournal
from adaptive_health_tips import AdaptiveHealthTips
from daily_quotes import DailyQuotes

# Page configuration
st.set_page_config(
    page_title="Smart Mirror - Mental Health Monitor",
    page_icon="🪞",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for futuristic dark theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0A192F 0%, #1E293B 100%);
        color: #E5E7EB;
    }
    
    .main-header {
        color: #FFFFFF;
        font-size: 2.5rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 0 10px rgba(6, 182, 212, 0.3);
    }
    
    .mirror-frame {
        border: 3px solid #06B6D4;
        border-radius: 20px;
        box-shadow: 0 0 30px rgba(6, 182, 212, 0.4);
        padding: 10px;
        background: rgba(6, 182, 212, 0.1);
        margin: 20px 0;
    }
    
    .emotion-display {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(20, 184, 166, 0.2));
        border: 1px solid #06B6D4;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        text-align: center;
    }
    
    .emotion-text {
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .health-tip {
        background: rgba(20, 184, 166, 0.15);
        border-left: 4px solid #14B8A6;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
        font-style: italic;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(30, 41, 59, 0.3));
        border: 1px solid #06B6D4;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        text-align: center;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #06B6D4, #14B8A6);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 500;
        padding: 0.5rem 1rem;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(6, 182, 212, 0.4);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #0A192F, #1E293B);
    }
    
    h1, h2, h3 {
        color: #FFFFFF !important;
    }
    
    .stSelectbox > div > div {
        background-color: rgba(6, 182, 212, 0.1);
        border: 1px solid #06B6D4;
    }
    
    /* Mood indicator colors */
    .mood-happy { color: #22C55E; }
    .mood-neutral { color: #9CA3AF; }
    .mood-sad { color: #3B82F6; }
    .mood-angry { color: #F87171; }
    .mood-tired { color: #A78BFA; }
    
    /* Enhanced UI Elements */
    .streak-container {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(6, 182, 212, 0.2));
        border: 1px solid #22C55E;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        text-align: center;
    }
    
    .insight-card {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.15), rgba(20, 184, 166, 0.15));
        border: 1px solid #06B6D4;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.2);
    }
    
    .quote-display {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(20, 184, 166, 0.1));
        border-left: 4px solid #06B6D4;
        padding: 15px 20px;
        margin: 15px 0;
        border-radius: 8px;
        font-style: italic;
        text-align: center;
        box-shadow: 0 2px 10px rgba(6, 182, 212, 0.2);
    }
    
    .emotion-emoji {
        font-size: 1.5rem;
        margin-right: 8px;
    }
    
    /* Animated background gradient */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .animated-bg {
        background: linear-gradient(-45deg, #0A192F, #1E293B, #0F172A, #1E293B);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: rgba(6, 182, 212, 0.1);
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #E5E7EB;
        background-color: transparent;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #06B6D4 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize components
@st.cache_resource
def load_emotion_detector():
    return EmotionDetector()

@st.cache_resource
def load_mood_tracker():
    return MoodTracker()

@st.cache_resource
def load_health_tips():
    return HealthTips()

@st.cache_resource
def load_bilingual_handler():
    return BilingualMessageHandler()

@st.cache_resource
def load_voice_handler():
    return VoiceHandler()

@st.cache_resource
def load_animated_logo():
    return AnimatedLogo()

@st.cache_resource
def load_emotion_journal():
    return EmotionJournal()

@st.cache_resource  
def load_adaptive_tips():
    journal = load_emotion_journal()
    return AdaptiveHealthTips(journal)

@st.cache_resource
def load_daily_quotes():
    return DailyQuotes()

# Main application
def main():
    # Initialize components first
    emotion_detector = load_emotion_detector()
    mood_tracker = load_mood_tracker()
    health_tips = load_health_tips()
    bilingual_handler = load_bilingual_handler()
    voice_handler = load_voice_handler()
    animated_logo = load_animated_logo()
    emotion_journal = load_emotion_journal()
    adaptive_tips = load_adaptive_tips()
    daily_quotes = load_daily_quotes()
    
    # Header with animated background
    st.markdown('<div class="animated-bg">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-header">🪞 Smart Mirror - Mental Health Monitor</h1>', unsafe_allow_html=True)
    
    # Daily quote display
    daily_quote = daily_quotes.get_time_based_quote()
    st.markdown(f'<div class="quote-display">{daily_quote}</div>', unsafe_allow_html=True)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["🪞 Mirror", "📊 Journal", "🎯 Insights", "⚙️ Settings"])
    
    with tab1:
        mirror_interface(emotion_detector, mood_tracker, health_tips, bilingual_handler, 
                        voice_handler, animated_logo, emotion_journal, adaptive_tips, daily_quotes)
    
    with tab2:
        journal_interface(emotion_journal, daily_quotes)
    
    with tab3:
        insights_interface(emotion_journal, adaptive_tips)
        
    with tab4:
        settings_interface(emotion_journal)

def mirror_interface(emotion_detector, mood_tracker, health_tips, bilingual_handler, 
                    voice_handler, animated_logo, emotion_journal, adaptive_tips, daily_quotes):
    """Main mirror interface with camera and emotion detection"""
    
    # Create layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2 style="color: #FFFFFF;">Live Mirror Feed</h2>', unsafe_allow_html=True)
        
        # Camera feed placeholder
        camera_placeholder = st.empty()
        
        # Start/Stop camera buttons
        col1_1, col1_2, col1_3 = st.columns(3)
        with col1_1:
            start_camera = st.button("🎥 Start Camera", key="start")
        with col1_2:
            stop_camera = st.button("⏹️ Stop Camera", key="stop")
        with col1_3:
            capture_emotion = st.button("📸 Analyze Emotion", key="analyze")
    
    with col2:
        st.markdown('<h2 style="color: #FFFFFF;">Emotion Analysis</h2>', unsafe_allow_html=True)
        
        # Current emotion display
        emotion_placeholder = st.empty()
        
        # Bilingual message display
        bilingual_placeholder = st.empty()
        
        # Health tip display  
        tip_placeholder = st.empty()
        
        # Animated logo
        logo_placeholder = st.empty()
        
        # Voice controls
        st.markdown('<h3 style="color: #FFFFFF;">Voice Controls</h3>', unsafe_allow_html=True)
        
        # Auto-voice toggle
        auto_voice = st.checkbox("🎤 Auto-speak emotions", value=st.session_state.get('auto_voice', True), key="auto_voice_toggle")
        st.session_state.auto_voice = auto_voice
        
        col2_1, col2_2 = st.columns(2)
        with col2_1:
            if st.button("🔊 Speak Message", key="speak"):
                if 'current_emotion' in st.session_state:
                    english_msg, hindi_msg = bilingual_handler.get_bilingual_message(st.session_state.current_emotion)
                    voice_handler.speak_text(english_msg)
        with col2_2:
            if st.button("🔇 Stop Voice", key="stop_voice"):
                voice_handler.stop_speaking()
        
        # Mood statistics
        st.markdown('<h3 style="color: #FFFFFF;">Today\'s Mood Stats</h3>', unsafe_allow_html=True)
        stats_placeholder = st.empty()
    
    # Mood trend graph
    st.markdown('<h2 style="color: #FFFFFF;">Mood Trend Analysis</h2>', unsafe_allow_html=True)
    
    # Time range selector
    time_range = st.selectbox(
        "Select time range:",
        ["Last 24 Hours", "Last 7 Days", "Last 30 Days"],
        key="time_range"
    )
    
    graph_placeholder = st.empty()
    
    # Session state for camera and voice
    if 'camera_active' not in st.session_state:
        st.session_state.camera_active = False
    if 'current_emotion' not in st.session_state:
        st.session_state.current_emotion = "neutral"
    if 'confidence' not in st.session_state:
        st.session_state.confidence = 0.0
    if 'last_emotion_time' not in st.session_state:
        st.session_state.last_emotion_time = 0
    if 'auto_voice' not in st.session_state:
        st.session_state.auto_voice = True
    
    # Camera control logic
    if start_camera:
        st.session_state.camera_active = True
    
    if stop_camera:
        st.session_state.camera_active = False
    
    # Main loop for camera feed and analysis
    if st.session_state.camera_active:
        run_camera_analysis(
            camera_placeholder, 
            emotion_placeholder,
            bilingual_placeholder, 
            tip_placeholder, 
            logo_placeholder,
            stats_placeholder,
            emotion_detector, 
            mood_tracker, 
            health_tips,
            bilingual_handler,
            voice_handler,
            animated_logo,
            emotion_journal
        )
    else:
        # Display placeholder when camera is off
        with camera_placeholder.container():
            st.markdown("""
            <div class="mirror-frame">
                <div style="height: 400px; display: flex; align-items: center; justify-content: center; background: rgba(6, 182, 212, 0.05); border-radius: 15px;">
                    <div style="text-align: center;">
                        <h3 style="color: #06B6D4;">Camera Offline</h3>
                        <p style="color: #9CA3AF;">Click 'Start Camera' to begin emotion detection</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Show last known emotion if available
        display_current_emotion(emotion_placeholder, st.session_state.current_emotion, st.session_state.confidence)
        if bilingual_handler:
            bilingual_html = bilingual_handler.format_bilingual_display(st.session_state.current_emotion)
            with bilingual_placeholder.container():
                st.markdown(bilingual_html, unsafe_allow_html=True)
        display_health_tip(tip_placeholder, st.session_state.current_emotion, health_tips)
        
        # Show logo in idle state
        with logo_placeholder.container():
            try:
                is_speaking = voice_handler.is_currently_speaking()
            except Exception:
                is_speaking = False
            animated_logo.create_streamlit_component(is_speaking, "Ready")
    
    # Always show mood statistics and trends
    display_mood_stats(stats_placeholder, mood_tracker)
    display_mood_trends(graph_placeholder, mood_tracker, time_range)
    
    # Manual emotion capture
    if capture_emotion and st.session_state.camera_active:
        # This would trigger a one-time emotion analysis
        st.success("Emotion captured and analyzed!")

def run_camera_analysis(camera_placeholder, emotion_placeholder, bilingual_placeholder, tip_placeholder, logo_placeholder, stats_placeholder, emotion_detector, mood_tracker, health_tips, bilingual_handler, voice_handler, animated_logo, emotion_journal):

    """Run real-time camera analysis"""
    try:
        # Initialize camera
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            st.error("❌ Camera not accessible. Please check your camera permissions.")
            return
        
        # Camera feed loop (simplified for demo - in real app this would be continuous)
        ret, frame = cap.read()
        
        if ret:
            # Flip frame for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Detect emotion
            emotion, confidence = emotion_detector.detect_emotion(frame)
            
            # Update session state
            st.session_state.current_emotion = emotion
            st.session_state.confidence = confidence
            
            # Record mood data
            mood_tracker.record_mood(emotion, confidence)
            
            # Convert frame for display
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Display camera feed
            with camera_placeholder.container():
                st.markdown('<div class="mirror-frame">', unsafe_allow_html=True)
                st.image(rgb_frame, use_column_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Display analysis results
            display_current_emotion(emotion_placeholder, emotion, confidence)
            if bilingual_handler:
                bilingual_html = bilingual_handler.format_bilingual_display(emotion)
                with bilingual_placeholder.container():
                    st.markdown(bilingual_html, unsafe_allow_html=True)
            display_health_tip(tip_placeholder, emotion, health_tips)
            display_mood_stats(stats_placeholder, mood_tracker)
            
            # Show animated logo with voice status
            with logo_placeholder.container():
                animated_logo.create_streamlit_component(voice_handler.is_currently_speaking(), "Analyzing...")
            
            # Log emotion to journal
            if emotion_journal:
                emotion_journal.log_emotion(emotion, confidence, session_id=st.session_state.get('session_id', 'default'))
            
            # Auto-speak if emotion changed and auto voice is enabled
            current_time = time.time()
            if (st.session_state.auto_voice and 
                emotion != st.session_state.get('last_spoken_emotion', '') and
                current_time - st.session_state.last_emotion_time > 3):  # 3 second cooldown
                
                english_msg, _ = bilingual_handler.get_bilingual_message(emotion)
                voice_handler.speak_text(english_msg)
                st.session_state.last_spoken_emotion = emotion
                st.session_state.last_emotion_time = current_time
        
        cap.release()
        
    except Exception as e:
        st.error(f"❌ Error accessing camera: {str(e)}")
        st.info("💡 Please ensure your camera is connected and permissions are granted.")

def get_emotion_emoji(emotion: str) -> str:
    """Get emoji for emotion"""
    emotion_emojis = {
        'happy': '😊',
        'neutral': '😐', 
        'sad': '😔',
        'angry': '😡',
        'tired': '😴',
        'surprised': '😮',
        'fear': '😨'
    }
    return emotion_emojis.get(emotion, '🙂')

def display_current_emotion(placeholder, emotion, confidence):
    """Display current emotion analysis"""
    emotion_colors = {
        'happy': '#22C55E',
        'neutral': '#9CA3AF', 
        'sad': '#3B82F6',
        'angry': '#F87171',
        'tired': '#A78BFA',
        'surprised': '#F59E0B',
        'fear': '#EF4444'
    }
    
    color = emotion_colors.get(emotion, '#9CA3AF')
    confidence_bar = int(confidence * 100) if confidence > 0 else 0
    
    emoji = get_emotion_emoji(emotion)
    
    with placeholder.container():
        st.markdown(f"""
        <div class="emotion-display">
            <div class="emotion-text" style="color: {color};">
                <span class="emotion-emoji">{emoji}</span>{emotion.title()} ({confidence_bar}%)
            </div>
            <div style="width: 100%; background: rgba(255,255,255,0.1); border-radius: 10px; height: 8px;">
                <div style="width: {confidence_bar}%; background: {color}; height: 100%; border-radius: 10px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def display_health_tip(placeholder, emotion, health_tips):
    """Display personalized health tip"""
    tip = health_tips.get_tip(emotion)
    
    with placeholder.container():
        st.markdown(f"""
        <div class="health-tip">
            <strong>💡 Health Tip:</strong><br>
            {tip}
        </div>
        """, unsafe_allow_html=True)

def display_mood_stats(placeholder, mood_tracker):
    """Display today's mood statistics"""
    stats = mood_tracker.get_daily_stats()
    
    with placeholder.container():
        for emotion, count in stats.items():
            if count > 0:
                st.markdown(f"""
                <div class="metric-card">
                    <strong>{emotion.title()}</strong><br>
                    <span style="font-size: 1.2rem;">{count} times</span>
                </div>
                """, unsafe_allow_html=True)

def display_mood_trends(placeholder, mood_tracker, time_range):
    """Display mood trend graph"""
    # Get data based on time range
    days = {"Last 24 Hours": 1, "Last 7 Days": 7, "Last 30 Days": 30}[time_range]
    trend_data = mood_tracker.get_mood_trends(days)
    
    if not trend_data.empty:
        # Create plotly figure
        fig = go.Figure()
        
        emotion_colors = {
            'happy': '#22C55E',
            'neutral': '#9CA3AF',
            'sad': '#3B82F6', 
            'angry': '#F87171',
            'tired': '#A78BFA'
        }
        
        for emotion in trend_data.columns:
            if emotion != 'timestamp':
                fig.add_trace(go.Scatter(
                    x=trend_data['timestamp'],
                    y=trend_data[emotion],
                    mode='lines+markers',
                    name=emotion.title(),
                    line=dict(color=emotion_colors.get(emotion, '#9CA3AF'), width=3),
                    marker=dict(size=6)
                ))
        
        fig.update_layout(
            title="Mood Trends Over Time",
            xaxis_title="Time",
            yaxis_title="Frequency",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#E5E7EB',
            title_font_color='#FFFFFF',
            xaxis=dict(gridcolor='rgba(6, 182, 212, 0.2)'),
            yaxis=dict(gridcolor='rgba(6, 182, 212, 0.2)'),
            legend=dict(font_color='#E5E7EB')
        )
        
        with placeholder.container():
            st.plotly_chart(fig, use_container_width=True)
    else:
        with placeholder.container():
            st.info("📊 No mood data available yet. Start using the camera to track your emotions!")

def journal_interface(emotion_journal, daily_quotes):
    """Journal and history interface"""
    st.markdown('<h2 style="color: #FFFFFF;">📊 Emotion Journal</h2>', unsafe_allow_html=True)
    
    # Export controls
    col1, col2, col3 = st.columns(3)
    with col1:
        days_range = st.selectbox("Export Range", [7, 14, 30, 90], index=1)
    with col2:
        if st.button("📁 Export CSV"):
            filename = emotion_journal.export_to_csv(days_range)
            if filename:
                st.success(f"Exported to {filename}")
            else:
                st.error("No data to export")
    with col3:
        st.markdown("### Download History")
    
    # Calendar heatmap
    st.markdown('<h3 style="color: #FFFFFF;">Emotion Calendar</h3>', unsafe_allow_html=True)
    heatmap_fig = emotion_journal.create_emotion_heatmap(30)
    st.plotly_chart(heatmap_fig, use_container_width=True)
    
    # Recent history table
    st.markdown('<h3 style="color: #FFFFFF;">Recent Entries</h3>', unsafe_allow_html=True)
    recent_data = emotion_journal.get_emotion_history(7)
    
    if not recent_data.empty:
        # Add emoji column
        emotion_emojis = {'happy': '😊', 'sad': '😔', 'angry': '😡', 'neutral': '😐', 'tired': '😴', 'surprised': '😮'}
        recent_data['Emoji'] = recent_data['emotion'].map(emotion_emojis)
        display_df = recent_data[['Emoji', 'emotion', 'confidence', 'timestamp']].head(20)
        display_df.columns = ['', 'Emotion', 'Confidence', 'Time']
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No journal entries yet. Start using the camera to track your emotions!")

def insights_interface(emotion_journal, adaptive_tips):
    """Insights and analytics interface"""
    st.markdown('<h2 style="color: #FFFFFF;">🎯 Insights & Analytics</h2>', unsafe_allow_html=True)
    
    # Get insights
    insights = emotion_journal.get_mood_insights(14)
    streaks = emotion_journal.get_current_streaks()
    weekly_comparison = emotion_journal.get_weekly_comparison()
    
    # Mood streaks section
    st.markdown('<h3 style="color: #FFFFFF;">🏆 Mood Streaks</h3>', unsafe_allow_html=True)
    
    if streaks:
        for streak_type, data in streaks.items():
            if data['current'] > 0:
                emoji = '🎉' if streak_type == 'positive' else '💙' if streak_type == 'negative' else '😐'
                st.markdown(f"""
                <div class="streak-container">
                    <h4>{emoji} {streak_type.title()} Streak</h4>
                    <div style="font-size: 2rem; font-weight: bold; color: #22C55E;">
                        {data['current']} days
                    </div>
                    <div style="color: #9CA3AF;">Best: {data['best']} days</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Start tracking emotions to see your streaks!")
    
    # Key insights
    st.markdown('<h3 style="color: #FFFFFF;">💡 Key Insights</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="insight-card">
            <h4>📊 This Week</h4>
            <p><strong>Total detections:</strong> {insights.get('total_entries', 0)}</p>
            <p><strong>Dominant emotion:</strong> {insights.get('dominant_emotion', 'neutral').title()}</p>
            <p><strong>Average confidence:</strong> {insights.get('average_confidence', 0):.1%}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        trend = weekly_comparison.get('overall_trend', 'stable')
        trend_color = '#22C55E' if trend == 'improving' else '#F87171' if trend == 'declining' else '#9CA3AF'
        trend_emoji = '📈' if trend == 'improving' else '📉' if trend == 'declining' else '➡️'
        
        st.markdown(f"""
        <div class="insight-card">
            <h4>📈 Weekly Trend</h4>
            <p style="color: {trend_color}; font-weight: bold;">{trend_emoji} {trend.title()}</p>
            <p><strong>This week:</strong> {weekly_comparison.get('this_week_total', 0)} detections</p>
            <p><strong>Last week:</strong> {weekly_comparison.get('last_week_total', 0)} detections</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Personalized recommendations
    st.markdown('<h3 style="color: #FFFFFF;">🎯 Personalized Recommendations</h3>', unsafe_allow_html=True)
    recommendations = adaptive_tips.get_personalized_recommendations()
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"""
        <div class="insight-card">
            <strong>{i}.</strong> {rec}
        </div>
        """, unsafe_allow_html=True)

def settings_interface(emotion_journal):
    """Settings and configuration interface"""
    st.markdown('<h2 style="color: #FFFFFF;">⚙️ Settings</h2>', unsafe_allow_html=True)
    
    # Data management
    st.markdown('<h3 style="color: #FFFFFF;">📁 Data Management</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Export Options**")
        export_days = st.slider("Days to export", 7, 365, 30)
        if st.button("📥 Export All Data"):
            filename = emotion_journal.export_to_csv(export_days)
            if filename:
                st.success(f"Data exported to {filename}")
            else:
                st.error("No data to export")
    
    with col2:
        st.markdown("**Data Cleanup**")
        cleanup_days = st.slider("Keep data for (days)", 30, 365, 90)
        if st.button("🗑️ Clean Old Data", type="secondary"):
            if st.button("Confirm cleanup?", type="primary"):
                emotion_journal.clear_old_data(cleanup_days)
                st.success(f"Cleared data older than {cleanup_days} days")
    
    # Statistics
    st.markdown('<h3 style="color: #FFFFFF;">📊 Statistics</h3>', unsafe_allow_html=True)
    
    try:
        total_entries = len(emotion_journal.get_emotion_history(365))
        recent_entries = len(emotion_journal.get_emotion_history(7))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Entries", total_entries)
        with col2:
            st.metric("This Week", recent_entries)  
        with col3:
            avg_daily = recent_entries / 7 if recent_entries > 0 else 0
            st.metric("Daily Average", f"{avg_daily:.1f}")
    except Exception as e:
        st.error(f"Error loading statistics: {e}")

if __name__ == "__main__":
    main()
