"""
微博短文案 Converter — 将 Markdown 提取为微博文本。

Usage:
    from weibo_converter import WeiboConverter
    converter = WeiboConverter()
    result = converter.convert(markdown_text)
"""

from dataclasses import dataclass


@dataclass
class WeiboResult:
    """Result of a Markdown → 微博文本 conversion."""
    content: str    # 140字以内的正文
    tags: list[str]  # 话题标签列表


class WeiboConverter:
    """将 Markdown 提取为微博文本（140字以内）。"""

    MAX_LENGTH = 140

    def convert(self, markdown_text: str) -> WeiboResult:
        """
        提取 Markdown 为微博文本。

        注意：实际的内容精简（140字版本）由 LLM 完成。
        本 Converter 仅处理结构化提取。
        """
        lines = markdown_text.strip().split("\n")

        body_parts = []
        tags = []

        for line in lines:
            line = line.strip()

            # 跳过标题
            if line.startswith("# "):
                continue

            # 提取话题标签
            if line.startswith("#"):
                parts = line.split("#")
                for part in parts:
                    tag = part.strip()
                    if tag and len(tag) > 1:
                        tags.append(tag)
                continue

            # 跳过图片
            if line.startswith("![]") or line.startswith("[图片"):
                continue

            # 跳过引用块
            if line.startswith(">"):
                continue

            # 跳过空行
            if not line:
                continue

            body_parts.append(line)

        full_text = "".join(body_parts)

        return WeiboResult(
            content=full_text[:self.MAX_LENGTH],
            tags=tags,
        )
