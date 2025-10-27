import streamlit as st
import time
import numpy as np

class AnimatedLogo:
    """
    Create Siri-style animated logo with wave animations
    """
    
    def __init__(self):
        self.animation_active = False
        
    def generate_wave_animation_css(self, is_active: bool = False) -> str:
        """
        Generate CSS for animated wave logo
        
        Args:
            is_active: Whether the animation should be active
            
        Returns:
            CSS string for the animated logo
        """
        animation_state = "running" if is_active else "paused"
        
        return f"""
        <style>
        @keyframes pulse {{
            0% {{ transform: scale(1); opacity: 0.8; }}
            50% {{ transform: scale(1.1); opacity: 1; }}
            100% {{ transform: scale(1); opacity: 0.8; }}
        }}
        
        @keyframes wave {{
            0% {{ transform: scaleY(0.5); }}
            25% {{ transform: scaleY(1.2); }}
            50% {{ transform: scaleY(0.8); }}
            75% {{ transform: scaleY(1.4); }}
            100% {{ transform: scaleY(0.5); }}
        }}
        
        @keyframes glow {{
            0% {{ box-shadow: 0 0 20px rgba(6, 182, 212, 0.4); }}
            50% {{ box-shadow: 0 0 40px rgba(6, 182, 212, 0.8), 0 0 60px rgba(20, 184, 166, 0.4); }}
            100% {{ box-shadow: 0 0 20px rgba(6, 182, 212, 0.4); }}
        }}
        
        .voice-logo-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 20px 0;
            height: 100px;
        }}
        
        .voice-logo {{
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: linear-gradient(135deg, #06B6D4, #14B8A6);
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            animation: pulse 2s ease-in-out infinite {animation_state},
                      glow 3s ease-in-out infinite {animation_state};
        }}
        
        .voice-logo::before {{
            content: '';
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.3), rgba(20, 184, 166, 0.3));
            transform: scale(1.2);
            animation: pulse 1.5s ease-in-out infinite {animation_state};
        }}
        
        .wave-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 40px;
            gap: 3px;
        }}
        
        .wave-bar {{
            width: 4px;
            background: #FFFFFF;
            border-radius: 2px;
            animation: wave 1s ease-in-out infinite {animation_state};
        }}
        
        .wave-bar:nth-child(1) {{ height: 20px; animation-delay: 0s; }}
        .wave-bar:nth-child(2) {{ height: 30px; animation-delay: 0.1s; }}
        .wave-bar:nth-child(3) {{ height: 25px; animation-delay: 0.2s; }}
        .wave-bar:nth-child(4) {{ height: 35px; animation-delay: 0.3s; }}
        .wave-bar:nth-child(5) {{ height: 20px; animation-delay: 0.4s; }}
        .wave-bar:nth-child(6) {{ height: 30px; animation-delay: 0.5s; }}
        .wave-bar:nth-child(7) {{ height: 25px; animation-delay: 0.6s; }}
        
        .logo-text {{
            color: #06B6D4;
            font-size: 0.9rem;
            font-weight: 500;
            margin-top: 10px;
            text-align: center;
            opacity: {1 if is_active else 0.7};
            transition: opacity 0.3s ease;
        }}
        </style>
        """
    
    def render_animated_logo(self, is_speaking: bool = False, status_text: str = "AI Assistant") -> str:
        """
        Render the animated logo HTML
        
        Args:
            is_speaking: Whether the AI is currently speaking
            status_text: Text to display below the logo
            
        Returns:
            HTML string for the animated logo
        """
        css = self.generate_wave_animation_css(is_speaking)
        
        # Dynamic status text based on speaking state
        if is_speaking:
            display_text = "🎤 Speaking..."
            text_color = "#22C55E"  # Green when speaking
        else:
            display_text = status_text
            text_color = "#06B6D4"  # Teal when idle
        
        html = f"""
        {css}
        <div class="voice-logo-container">
            <div style="text-align: center;">
                <div class="voice-logo">
                    <div class="wave-container">
                        <div class="wave-bar"></div>
                        <div class="wave-bar"></div>
                        <div class="wave-bar"></div>
                        <div class="wave-bar"></div>
                        <div class="wave-bar"></div>
                        <div class="wave-bar"></div>
                        <div class="wave-bar"></div>
                    </div>
                </div>
                <div class="logo-text" style="color: {text_color};">
                    {display_text}
                </div>
            </div>
        </div>
        """
        
        return html
    
    def create_streamlit_component(self, is_speaking: bool = False, status_text: str = "Smart Mirror AI"):
        """
        Create Streamlit component for the animated logo
        
        Args:
            is_speaking: Whether the AI is currently speaking
            status_text: Status text to display
        """
        logo_html = self.render_animated_logo(is_speaking, status_text)
        st.markdown(logo_html, unsafe_allow_html=True)
    
    def get_simple_status_indicator(self, is_speaking: bool = False) -> str:
        """
        Get a simple status indicator for the logo
        
        Args:
            is_speaking: Whether currently speaking
            
        Returns:
            Status indicator HTML
        """
        if is_speaking:
            return """
            <div style="text-align: center; padding: 10px;">
                <div style="display: inline-block; width: 12px; height: 12px; 
                           background: #22C55E; border-radius: 50%; 
                           animation: pulse 1s ease-in-out infinite;">
                </div>
                <span style="margin-left: 10px; color: #22C55E; font-weight: 500;">
                    🎤 AI is speaking...
                </span>
            </div>
            """
        else:
            return """
            <div style="text-align: center; padding: 10px;">
                <div style="display: inline-block; width: 12px; height: 12px; 
                           background: #06B6D4; border-radius: 50%;">
                </div>
                <span style="margin-left: 10px; color: #06B6D4; font-weight: 500;">
                    🤖 Ready
                </span>
            </div>
            """