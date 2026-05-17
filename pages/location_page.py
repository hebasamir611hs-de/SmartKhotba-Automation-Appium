"""
LocationPage — Location permission / selection screen (LocationActivity).
"""
from appium.webdriver.common.appiumby import AppiumBy as By
from pages.base_page import BasePage


class LocationPage(BasePage):
    """Location access screen — request permission or select location manually."""

    PAGE_NAME = "location_page"

    # ─── Locators ────────────────────────────────────────────────
    ALLOW_LOCATION_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_allow_location")
    SKIP_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_skip")
    SEARCH_FIELD = (By.ID, "com.islam.khutba.qa:id/et_search_location")
    LOCATION_LIST = (By.ID, "com.islam.khutba.qa:id/rv_locations")

    # System permission dialog
    PERMISSION_ALLOW = (By.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button")
    PERMISSION_DENY = (By.ID, "com.android.permissioncontroller:id/permission_deny_button")
    PERMISSION_ALLOW_ONCE = (By.ID, "com.android.permissioncontroller:id/permission_allow_one_time_button")

    # ─── Actions ─────────────────────────────────────────────────

    def is_location_screen_displayed(self) -> bool:
        return self.is_displayed(self.ALLOW_LOCATION_BUTTON, timeout=10) or \
               self.is_displayed(self.SKIP_BUTTON, timeout=3)

    def allow_location(self):
        """Tap allow location then handle system permission dialog."""
        self.click(self.ALLOW_LOCATION_BUTTON)
        self._handle_system_permission(allow=True)

    def skip_location(self):
        """Skip location permission."""
        self.click(self.SKIP_BUTTON)

    def search_location(self, query: str):
        """Search for a location manually."""
        self.type_text(self.SEARCH_FIELD, query)

    def select_location_by_text(self, location_name: str):
        """Select a location from search results."""
        locator = (By.XPATH, f"//*[contains(@text, '{location_name}')]")
        self.click(locator)

    def _handle_system_permission(self, allow: bool = True):
        """Handle Android system permission dialog."""
        if allow:
            if self.is_displayed(self.PERMISSION_ALLOW, timeout=5):
                self.click(self.PERMISSION_ALLOW)
        else:
            if self.is_displayed(self.PERMISSION_DENY, timeout=5):
                self.click(self.PERMISSION_DENY)
