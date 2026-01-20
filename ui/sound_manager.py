"""
音效管理器
"""
import pygame
import os


class SoundManager:
    """音效管理器"""

    def __init__(self):
        """初始化音效管理器"""
        pygame.mixer.init()
        self.sounds = {}
        self.enabled = True
        self._create_sounds()

    def _create_sounds(self):
        """创建音效（使用程序生成的简单音效）"""
        # 由于没有音频文件，我们使用 pygame 的音频生成功能
        # 创建简单的音效
        try:
            # 移动音效 - 短促的咔哒声
            self.sounds['move'] = self._generate_click_sound(frequency=800, duration=0.1)

            # 吃子音效 - 较重的声音
            self.sounds['capture'] = self._generate_click_sound(frequency=400, duration=0.15)

            # 将军音效 - 警告声
            self.sounds['check'] = self._generate_beep_sound(frequency=1200, duration=0.2)

            # 胜利音效 - 上升音调
            self.sounds['win'] = self._generate_victory_sound()

        except Exception as e:
            print(f"音效初始化失败: {e}")
            self.enabled = False

    def _generate_click_sound(self, frequency=800, duration=0.1):
        """生成咔哒声"""
        sample_rate = 22050
        n_samples = int(round(duration * sample_rate))

        # 生成正弦波
        import numpy as np
        buf = np.zeros((n_samples, 2), dtype=np.int16)
        max_sample = 2 ** (16 - 1) - 1

        for i in range(n_samples):
            t = float(i) / sample_rate
            # 添加衰减
            amplitude = max_sample * 0.3 * (1 - t / duration)
            value = int(amplitude * np.sin(2 * np.pi * frequency * t))
            buf[i] = [value, value]

        sound = pygame.sndarray.make_sound(buf)
        return sound

    def _generate_beep_sound(self, frequency=1000, duration=0.2):
        """生成蜂鸣声"""
        sample_rate = 22050
        n_samples = int(round(duration * sample_rate))

        import numpy as np
        buf = np.zeros((n_samples, 2), dtype=np.int16)
        max_sample = 2 ** (16 - 1) - 1

        for i in range(n_samples):
            t = float(i) / sample_rate
            # 使用包络
            envelope = 0.5 if t < duration * 0.8 else 0.5 * (1 - (t - duration * 0.8) / (duration * 0.2))
            value = int(max_sample * envelope * np.sin(2 * np.pi * frequency * t))
            buf[i] = [value, value]

        sound = pygame.sndarray.make_sound(buf)
        return sound

    def _generate_victory_sound(self):
        """生成胜利音效"""
        sample_rate = 22050
        duration = 0.5
        n_samples = int(round(duration * sample_rate))

        import numpy as np
        buf = np.zeros((n_samples, 2), dtype=np.int16)
        max_sample = 2 ** (16 - 1) - 1

        # 上升音调
        for i in range(n_samples):
            t = float(i) / sample_rate
            frequency = 600 + 400 * (t / duration)  # 从600Hz上升到1000Hz
            amplitude = max_sample * 0.3 * (1 - t / duration)
            value = int(amplitude * np.sin(2 * np.pi * frequency * t))
            buf[i] = [value, value]

        sound = pygame.sndarray.make_sound(buf)
        return sound

    def play(self, sound_name):
        """
        播放音效

        Args:
            sound_name: 音效名称 ('move', 'capture', 'check', 'win')
        """
        if not self.enabled:
            return

        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"播放音效失败: {e}")

    def set_enabled(self, enabled):
        """设置是否启用音效"""
        self.enabled = enabled

    def is_enabled(self):
        """音效是否启用"""
        return self.enabled
