"""
Locator Healing Logic.
Integrates with centralized locators.py and metrics_tracker.py.
"""
from appium.webdriver.common.appiumby import AppiumBy as By
from utils.logger import get_logger
from data.locators import LOCATOR_REGISTRY
from core.metrics_tracker import MetricsTracker

logger = get_logger(__name__)
metrics = MetricsTracker()

class LocatorHealer:
    @staticmethod
    def heal(driver, primary_locator, page_name=None, element_name=None):
        """
        Attempts to find an element using primary locator, 
        and falls back to backups defined in LOCATOR_REGISTRY.
        """
        # 1. Search in Registry for backups
        backups = []
        if page_name and element_name:
            entry = LOCATOR_REGISTRY.get(page_name, {}).get(element_name, {})
            backups = entry.get("backups", [])
        
        # 2. Heuristic Backups (if registry entry not found)
        if not backups:
            if primary_locator[0] == By.ACCESSIBILITY_ID:
                backups = [(By.XPATH, f"//*[@content-desc='{primary_locator[1]}']")]
            elif primary_locator[0] == By.ID:
                # By.ID already maps to resource-id internally; XPath duplicate is useless.
                # Try class-name partial match as a true alternative path.
                resource_id = primary_locator[1].split(":id/")[-1]
                backups = [(By.XPATH, f"//*[contains(@resource-id, '{resource_id}')]")]

        # 3. Execution Loop
        logger.warning(f"Primary locator {primary_locator} failed. Attempting healing for {page_name}.{element_name}...")
        
        for strategy, selector in backups:
            try:
                element = driver.find_element(strategy, selector)
                logger.info(f"✅ Healed! Found element using {strategy}: {selector}")
                
                # Log success metric
                metrics.log_healing_event(
                    page_name or "Unknown", 
                    element_name or "Unknown", 
                    primary_locator, 
                    (strategy, selector)
                )
                return element
            except Exception:
                continue
        
        # 4. Final Failure
        metrics.log_failure_event(
            page_name or "Unknown", 
            element_name or "Unknown", 
            primary_locator
        )
        raise Exception(f"Healing failed for {primary_locator}. All backups exhausted.")
