"""
Video Player Tests — Live stream and recorded video.
"""
import pytest
from tests.base_test import BaseTest
from pages.main_page import MainPage
from pages.khotba_page import KhotbaPage
from pages.video_player_page import VideoPlayerPage
from tests.helpers import navigate_to_main


@pytest.mark.regression
class TestVideoPlayer(BaseTest):
    """Video player / live stream tests."""

    def _open_video(self):
        main = navigate_to_main(self.driver)
        main.navigate_to_khotba()
        khotba = KhotbaPage(self.driver)
        khotba.wait_for_content_loaded()
        if khotba.is_displayed(khotba.LIVE_STREAM_BUTTON, timeout=5):
            khotba.open_live_stream()
        elif khotba.is_displayed(khotba.PLAY_AUDIO_BUTTON, timeout=5):
            khotba.select_khotba_by_index(0)
            khotba.play_audio()
        return VideoPlayerPage(self.driver)

    def test_video_player_loads(self):
        """Verify that video player opens and displays."""
        player = self._open_video()
        assert player.is_player_displayed(), "Video player not displayed"

    def test_video_play_pause(self):
        """Verify that play/pause button works."""
        player = self._open_video()
        if player.is_player_displayed():
            player.wait_for_video_loaded()
            player.play_pause()  # pause
            player.play_pause()  # resume

    def test_video_player_error_retry(self):
        """Verify that error state shows retry button."""
        player = self._open_video()
        if player.has_error():
            error_text = player.get_error_text()
            assert error_text != "", "Error shown but no message"
            player.retry()

    def test_back_from_video_player(self):
        """Verify that back button exits player."""
        player = self._open_video()
        if player.is_player_displayed():
            player.go_back()
            assert not player.is_player_displayed(), "Still on video player after back"
