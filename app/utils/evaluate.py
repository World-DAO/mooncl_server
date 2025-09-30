import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from app.config import settings

logger = logging.getLogger(__name__)

try:
    from openai import OpenAI

    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI库未安装，将使用传统估价算法")


class AIEvaluator:
    """AI智能估价器"""

    def __init__(self):
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """初始化AI客户端"""
        if not OPENAI_AVAILABLE:
            return

        try:
            if settings.OPENAI_API_KEY:
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                logger.info("AI评估器初始化成功")
            else:
                logger.info("AI评估未启用或缺少API Key，使用传统算法")
        except Exception as e:
            logger.error(f"AI评估器初始化失败: {e}")

    async def evaluate_content_ai(self, content: str) -> Optional[Dict[str, Any]]:
        """使用AI评估内容价值"""
        if not self.client:
            return None

        try:
            prompt = f"""
            作为NFT内容评估专家，分析以下文本的价值：

            内容: "{content}"

            从以下维度评估（1-10分）：
            1. 创意性: 原创性和创新程度
            2. 艺术价值: 文学或艺术表现力  
            3. 稀有性: 独特性和稀缺性
            4. 情感共鸣: 能否引起情感共鸣
            5. 市场潜力: NFT市场潜在价值

            返回JSON格式：
            {{
                "creativity_score": 分数,
                "artistic_value": 分数,
                "rarity_score": 分数,
                "emotional_impact": 分数,
                "market_potential": 分数,
                "overall_score": 总分,
                "suggested_price_eth": 建议价格(0.001-1.0 ETH),
                "reasoning": "评估理由"
            }}
            """

            # 使用新版本OpenAI API
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是专业的NFT内容评估专家。"},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=400,
                temperature=0.7,
            )

            content_response = response.choices[0].message.content

            # 解析JSON响应
            start_idx = content_response.find("{")
            end_idx = content_response.rfind("}") + 1

            if start_idx != -1 and end_idx != 0:
                json_str = content_response[start_idx:end_idx]
                evaluation = json.loads(json_str)

                # 验证和标准化数据
                price = float(evaluation.get("suggested_price_eth", 0.01))
                evaluation["suggested_price_eth"] = max(0.001, min(price, 1.0))
                evaluation["evaluation_method"] = "ai_agent"
                evaluation["evaluated_at"] = datetime.now().isoformat()

                return evaluation

        except Exception as e:
            logger.error(f"AI评估失败: {e}")

        return None


# 全局AI评估器实例
_ai_evaluator = AIEvaluator()


def calculate_price_traditional(content: str) -> float:
    """传统价格评估算法"""
    # 基础价格
    base_price = 0.01

    # 内容长度因子 (最大5倍)
    length_factor = min(len(content) / 100, 5.0)

    # 简单的内容质量评估
    quality_factor = 1.0

    # 检查是否包含特殊字符或表情符号
    if any(ord(char) > 127 for char in content):
        quality_factor += 0.2

    # 检查内容复杂度（单词数量）
    word_count = len(content.split())
    if word_count > 10:
        quality_factor += 0.3

    # 计算最终价格
    final_price = base_price * length_factor * quality_factor

    return round(min(final_price, 1.0), 6)


async def calculate_price(content: str) -> float:
    """
    智能价格评估算法
    """
    try:
        # AI评估
        ai_result = await _ai_evaluator.evaluate_content_ai(content)
        if ai_result and "suggested_price_eth" in ai_result:
            logger.info(f"AI评估成功: {ai_result['suggested_price_eth']} ETH")
            return float(ai_result["suggested_price_eth"])

    except Exception as e:
        logger.error(f"价格评估失败: {e}")
        return 0.01
