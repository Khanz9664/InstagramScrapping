import time
import random
import logging
from config import (
    get_random_user_agent,
    DELAY_CONFIG,
    VIEWPORT_CONFIG,
    WEBGL_SPOOFING,
    BROWSER_FEATURES
)

logger = logging.getLogger(__name__)

def apply_anti_detection(page):
    """Advanced anti-detection measures with multiple fingerprint protections"""
    try:
        # User Agent Rotation
        user_agent = get_random_user_agent()
        page.set_extra_http_headers({"User-Agent": user_agent})
        logger.info(f"🔄 Set User-Agent to: {user_agent}")

        # Viewport Spoofing
        viewport = get_viewport_config()
        page.set_viewport_size(viewport)
        logger.info(f"🖥️ Set viewport to: {viewport['width']}x{viewport['height']}")

        # Browser Feature Manipulation
        if BROWSER_FEATURES['disable_webdriver']:
            page.add_init_script("delete Object.getPrototypeOf(navigator).webdriver")

        if BROWSER_FEATURES['disable_webrtc']:
            page.add_init_script("""
                Object.defineProperty(navigator, 'credentials', { get: () => undefined });
                RTCPeerConnection = undefined;
            """)

        # WebGL Spoofing
        if WEBGL_SPOOFING['enabled']:
            page.add_init_script(f"""
                const getParameter = WebGLRenderingContext.prototype.getParameter;
                WebGLRenderingContext.prototype.getParameter = function(parameter) {{
                    if (parameter === 37445) {{ return '{WEBGL_SPOOFING['vendor']}'; }}
                    if (parameter === 37446) {{ return '{WEBGL_SPOOFING['renderer']}'; }}
                    return getParameter(parameter);
                }};
            """)

        # Fingerprint Evasion
        if BROWSER_FEATURES.get('disable_canvas_fingerprint', False):
            page.add_init_script("""
                HTMLCanvasElement.prototype.toDataURL = function() { return ""; };
                HTMLCanvasElement.prototype.getContext = function() { return null; };
            """)

        if BROWSER_FEATURES.get('disable_audio_fingerprint', False):
            page.add_init_script("""
                AudioContext = function() { this.createOscillator = function() { return { start: function() {} }; }; };
            """)

        # Behavioral Delay
        apply_behavioral_delay()
        
        # Language Spoofing
        page.set_extra_http_headers({"Accept-Language": "en-US,en;q=0.9"})

    except Exception as e:
        logger.error(f"❌ Anti-detection error: {str(e)}")

def get_viewport_config():
    """Get realistic viewport from common device resolutions"""
    return random.choice(VIEWPORT_CONFIG['presets'])

def apply_behavioral_delay():
    """Advanced delay patterns with random distribution"""
    min_delay, max_delay = DELAY_CONFIG['range']
    delay_type = DELAY_CONFIG.get('type', 'uniform')
    
    if delay_type == 'normal':
        # Normal distribution around mean
        delay = random.normalvariate(
            (min_delay + max_delay) / 2,
            (max_delay - min_delay) / 4
        )
    else:  # Default to uniform
        delay = random.uniform(min_delay, max_delay)
    
    delay = max(min(delay, max_delay), min_delay)
    logger.info(f"⏳ Applying {delay_type} delay: {round(delay, 2)}s")
    time.sleep(delay)

