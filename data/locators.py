# -*- coding: utf-8 -*-
"""
Centralized Locator Registry.
Stores primary and backup locators for the 13 Page Objects.
Used by the LocatorHealer for automated recovery.
"""
from appium.webdriver.common.appiumby import AppiumBy as By

LOCATOR_REGISTRY = {
    "splash_page": {
        "logo": {
            "primary": (By.ID, "com.islam.khutba.qa:id/splash_logo"),
            "backups": [
                (By.XPATH, "//android.widget.ImageView[@content-desc='SmartKhotba Logo']"),
                (By.ACCESSIBILITY_ID, "splash_logo_image")
            ]
        }
    },
    "language_page": {
        "arabic_btn": {
            "primary": (By.ID, "com.islam.khutba.qa:id/btn_arabic"),
            "backups": [(By.XPATH, "//android.widget.Button[@text='العربية']")]
        },
        "english_btn": {
            "primary": (By.ID, "com.islam.khutba.qa:id/btn_english"),
            "backups": [(By.XPATH, "//android.widget.Button[@text='English']")]
        }
    },
    "home_page": {
        "welcome_text": {
            "primary": (By.ID, "com.islam.khutba.qa:id/welcome_text"),
            "backups": [
                (By.XPATH, "//*[contains(@resource-id, 'welcome')]"),
                (By.XPATH, "//android.widget.TextView[contains(@text, 'مرحبا') or contains(@text, 'Welcome')]"),
            ],
        },
        "menu_button": {
            "primary": (By.ACCESSIBILITY_ID, "Menu"),
            "backups": [(By.ID, "com.islam.khutba.qa:id/btn_menu")],
        },
        "profile_icon": {
            "primary": (By.ID, "com.islam.khutba.qa:id/profile_icon"),
            "backups": [(By.XPATH, "//*[contains(@resource-id, 'profile')]")],
        },
    },
    "onboarding_page": {
        "next_button": {
            "primary": (By.ID, "com.islam.khutba.qa:id/btn_next"),
            "backups": [
                (By.XPATH, "//*[@resource-id='com.islam.khutba.qa:id/btn_next']"),
                (By.XPATH, "//android.widget.Button[contains(@text,'التالي') or contains(@text,'Next')]")
            ],
        },
        "skip_button": {
            "primary": (By.ID, "com.islam.khutba.qa:id/btn_skip"),
            "backups": [(By.XPATH, "//android.widget.Button[contains(@text,'تخطي') or contains(@text,'Skip')]")],
        },
    },
    "otp_page": {
        "phone_input": {
            "primary": (By.ID, "com.islam.khutba.qa:id/et_phone"),
            "backups": [(By.XPATH, "//android.widget.EditText[contains(@resource-id,'phone')]")],
        },
        "send_otp_button": {
            "primary": (By.ID, "com.islam.khutba.qa:id/btn_send_otp"),
            "backups": [(By.XPATH, "//android.widget.Button[contains(@text,'إرسال') or contains(@text,'Send')]")],
        },
    },
    "main_page": {
        "nav_home": {
            "primary": (By.ID, "com.islam.khutba.qa:id/nav_home"),
            "backups": [(By.XPATH, "//*[@resource-id='com.islam.khutba.qa:id/nav_home']")]
        },
        "nav_khotba": {
            "primary": (By.ID, "com.islam.khutba.qa:id/nav_khotba"),
            "backups": [(By.XPATH, "//*[@resource-id='com.islam.khutba.qa:id/nav_khotba']")]
        },
        "nav_concepts": {
            "primary": (By.ID, "com.islam.khutba.qa:id/nav_concepts"),
            "backups": [(By.XPATH, "//*[@resource-id='com.islam.khutba.qa:id/nav_concepts']")]
        },
        "menu_button": {
            "primary": (By.ID, "com.islam.khutba.qa:id/btn_menu"),
            "backups": [(By.ACCESSIBILITY_ID, "Menu")],
        },
    },
    "khotba_page": {
        "khotba_list": {
            "primary": (By.ID, "com.islam.khutba.qa:id/rv_khotba"),
            "backups": [(By.CLASS_NAME, "androidx.recyclerview.widget.RecyclerView")]
        },
        "search_icon": {
            "primary": (By.ID, "com.islam.khutba.qa:id/btn_search"),
            "backups": [(By.ACCESSIBILITY_ID, "Search")],
        },
    },
    "concepts_page": {
        "concepts_list": {
            "primary": (By.ID, "com.islam.khutba.qa:id/rv_concepts"),
            "backups": [(By.CLASS_NAME, "androidx.recyclerview.widget.RecyclerView")]
        },
    },
    "reminders_page": {
        "reminders_list": {
            "primary": (By.ID, "com.islam.khutba.qa:id/rv_reminders"),
            "backups": [(By.CLASS_NAME, "androidx.recyclerview.widget.RecyclerView")]
        },
        "add_reminder_button": {
            "primary": (By.ID, "com.islam.khutba.qa:id/btn_add_reminder"),
            "backups": [(By.ACCESSIBILITY_ID, "Add reminder")],
        },
    },
    "favorites_page": {
        "favorites_list": {
            "primary": (By.ID, "com.islam.khutba.qa:id/rv_favorites"),
            "backups": [(By.CLASS_NAME, "androidx.recyclerview.widget.RecyclerView")]
        },
        "empty_state": {
            "primary": (By.ID, "com.islam.khutba.qa:id/tv_empty"),
            "backups": [(By.XPATH, "//*[contains(@text,'فارغ') or contains(@text,'Empty')]")],
        },
    },
    "settings_page": {
        "notifications_toggle": {
            "primary": (By.ID, "com.islam.khutba.qa:id/switch_notifications"),
            "backups": [(By.CLASS_NAME, "android.widget.Switch")]
        },
        "app_version": {
            "primary": (By.ID, "com.islam.khutba.qa:id/tv_version"),
            "backups": [(By.XPATH, "//*[contains(@resource-id,'version')]")]
        },
        "back_button": {
            "primary": (By.ID, "com.islam.khutba.qa:id/btn_back"),
            "backups": [(By.ACCESSIBILITY_ID, "Back")],
        },
    },
    "video_player_page": {
        "video_view": {
            "primary": (By.ID, "com.islam.khutba.qa:id/video_view"),
            "backups": [(By.CLASS_NAME, "android.widget.VideoView")]
        },
        "play_pause_button": {
            "primary": (By.ID, "com.islam.khutba.qa:id/btn_play_pause"),
            "backups": [(By.ACCESSIBILITY_ID, "Play")],
        },
    },
    "location_page": {
        "allow_location_button": {
            "primary": (By.ID, "com.islam.khutba.qa:id/btn_allow_location"),
            "backups": [(By.XPATH, "//*[contains(@text,'السماح') or contains(@text,'Allow')]")]
        },
        "skip_button": {
            "primary": (By.ID, "com.islam.khutba.qa:id/btn_skip"),
            "backups": [(By.XPATH, "//*[contains(@text,'تخطي') or contains(@text,'Skip')]")]
        },
    },
}