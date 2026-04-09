"""
短视频脚本 Converter — 从 Markdown 提取短视频脚本结构。

Usage:
    from video_converter import VideoConverter
    converter = VideoConverter()
    result = converter.convert(markdown_text)
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Shot:
    """单个镜头."""
    number: int
    title: str
    duration: Optional[str] = None
    script: str = ""           # 配音稿
    visual: str = ""           # 画面描述
    subtitle: str = ""         # 字幕参考


@dataclass
class VideoResult:
    """Result of a Markdown → 短视频脚本 conversion."""
    title: str
    shots: list[Shot] = field(default_factory=list)
    total_duration_est: str = ""   # 估算总时长
    music_suggestion: str = ""     # 配乐建议


class VideoConverter:
    """将 Markdown 提取为短视频脚本结构。"""

    def convert(self, markdown_text: str) -> VideoResult:
        """
        解析 Markdown 为短视频脚本。

        识别以下结构：
        - 开场钩子（3秒）
        - 分镜正文（镜头编号 + 画面 + 配音）
        - 结尾引导
        """
        lines = markdown_text.strip().split("\n")

        title = ""
        shots = []
        current_shot = None
        section = "body"

        for line in lines:
            line = line.strip()

            # 提取标题
            if line.startswith("# ") and not title:
                title = line[2:].strip()
                continue

            # 识别分镜标记
            if "镜头" in line or "shot" in line.lower():
                if current_shot:
                    shots.append(current_shot)
                shot_num = len(shots) + 1
                # 提取镜头标题
                shot_title = line.replace("镜头", "").replace("Shot", "").replace("shot", "").strip()
                current_shot = Shot(number=shot_num, title=shot_title)
                continue

            # 识别各字段
            if current_shot:
                if "画面" in line or "视频" in line or "镜头" in line:
                    current_shot.visual = line.split("：")[-1].split("：")[-1].strip()
                elif "配音" in line or "「" in line:
                    # 提取配音内容
                    script_content = line
                    for m in ["配音", "：", "「"]:
                        if m in script_content:
                            script_content = script_content.split(m, 1)[-1].strip()
                    script_content = script_content.strip("」").strip("「")
                    current_shot.script = script_content
                elif "时长" in line:
                    current_shot.duration = line.split("：")[-1].split("：")[-1].strip()
                elif "字幕" in line:
                    current_shot.subtitle = line.split("：")[-1].split("：")[-1].strip()
                elif line.startswith("-") or line.startswith("•"):
                    # bullet points as additional description
                    pass
                elif line and not line.startswith("#"):
                    # 如果没有明确字段，视为画面描述
                    if not current_shot.visual:
                        current_shot.visual = line

        if current_shot:
            shots.append(current_shot)

        # 估算总时长
        total_est = f"约{len(shots) * 10}秒" if shots else "约60秒"

        return VideoResult(
            title=title,
            shots=shots,
            total_duration_est=total_est,
        )
