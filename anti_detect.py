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

# Setting up a logger to capture events
logger = logging.getLogger(__name__)

def apply_anti_detection(page):
    """Advanced anti-detection measures with multiple fingerprint protections."""
    try:
        # 1. User Agent Rotation: Randomize the User-Agent header to avoid detection
        user_agent = get_random_user_agent()
        page.set_extra_http_headers({"User-Agent": user_agent})
        logger.info(f"🔄 Set User-Agent to: {user_agent}")

        # 2. Viewport Spoofing: Set the viewport size to simulate a real device
        viewport = get_viewport_config()
        page.set_viewport_size(viewport)
        logger.info(f"🖥️ Set viewport to: {viewport['width']}x{viewport['height']}")

        # 3. Disable WebDriver flag: Bypass detection for headless browsers
        if BROWSER_FEATURES['disable_webdriver']:
            page.add_init_script("delete Object.getPrototypeOf(navigator).webdriver")

        # 4. Override navigator.languages: Simulate a real user by setting languages
        page.add_init_script("Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });")

        # 5. Override navigator.plugins: Return a fake list of plugins to avoid detection
        page.add_init_script("Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });")

        # 6. Add dummy chrome object: Mimic a real browser to avoid headless detection
        page.add_init_script("window.chrome = { runtime: {} };")

        # 7. Override navigator.permissions.query for notifications: Return fake permission states
        page.add_init_script("""
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
            );
        """)

        # 8. Disable WebRTC: Prevent WebRTC from leaking real IP address
        if BROWSER_FEATURES['disable_webrtc']:
            page.add_init_script("""
                Object.defineProperty(navigator, 'credentials', { get: () => undefined });
                RTCPeerConnection = undefined;
            """)

        # 9. WebGL Spoofing: Spoof WebGL rendering context to avoid detection based on hardware
        if WEBGL_SPOOFING['enabled']:
            page.add_init_script(f"""
                const getParameter = WebGLRenderingContext.prototype.getParameter;
                WebGLRenderingContext.prototype.getParameter = function(parameter) {{
                    if (parameter === 37445) {{ return '{WEBGL_SPOOFING['vendor']}'; }}
                    if (parameter === 37446) {{ return '{WEBGL_SPOOFING['renderer']}'; }}
                    return getParameter(parameter);
                }};
            """)

        # 10. Disable canvas fingerprinting: Prevent unique canvas fingerprinting from being captured
        if BROWSER_FEATURES.get('disable_canvas_fingerprint', False):
            page.add_init_script("""
                HTMLCanvasElement.prototype.toDataURL = function() { return ""; };
                HTMLCanvasElement.prototype.getContext = function() { return null; };
            """)

        # 11. Disable audio fingerprinting: Prevent audio context from being used to track the user
        if BROWSER_FEATURES.get('disable_audio_fingerprint', False):
            page.add_init_script("""
                AudioContext = function() { this.createOscillator = function() { return { start: function() {} }; }; };
            """)

        # 12. Override hardware concurrency: Simulate a typical device with a specific number of CPU cores
        page.add_init_script("Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 4 });")

        # 13. Behavioral Delay: Introduce randomized delays to mimic real user behavior
        apply_behavioral_delay()
        
        # 14. Language Spoofing: Set the Accept-Language header to mimic real user behavior
        page.set_extra_http_headers({"Accept-Language": "en-US,en;q=0.9"})

    except Exception as e:
        logger.error(f"❌ Anti-detection error: {str(e)}")

def get_viewport_config():
    """Get a realistic viewport configuration from common device resolutions."""
    return random.choice(VIEWPORT_CONFIG['presets'])

def apply_behavioral_delay():
    """Advanced delay patterns with random distribution to mimic human-like behavior."""
    min_delay, max_delay = DELAY_CONFIG['range']
    delay_type = DELAY_CONFIG.get('type', 'uniform')
    
    if delay_type == 'normal':
        # Apply a normal distribution delay (more human-like)
        delay = random.normalvariate((min_delay + max_delay) / 2, (max_delay - min_delay) / 4)
    else:
        # Apply a uniform delay within the specified range
        delay = random.uniform(min_delay, max_delay)
    
    # Ensure the delay is within the defined range
    delay = max(min(delay, max_delay), min_delay)
    logger.info(f"⏳ Applying {delay_type} delay: {round(delay, 2)}s")
    time.sleep(delay)

