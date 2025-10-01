import asyncio
import json
import logging
import hashlib
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


class EigenVerifiableAIEvaluator:
    """基于EigenLayer的可验证AI评估器"""

    def __init__(self):
        self.client = None
        self.operators = []
        self.eigencloud_client = None
        self.settings = None
        self._initialized = False

    def _initialize(self):
        """延迟初始化，避免循环导入"""
        if self._initialized:
            return

        try:
            from app.config import settings
            from app.utils.eigencloud_client import eigencloud_client

            self.settings = settings
            self.operators = settings.OPERATORS_LIST
            self.eigencloud_client = eigencloud_client
            self._initialize_client()
            self._initialized = True
            logger.info("EigenVerifiableAIEvaluator初始化完成")
        except Exception as e:
            logger.error(f"EigenVerifiableAIEvaluator初始化失败: {e}")
            self._initialized = True

    def _initialize_client(self):
        """初始化OpenAI客户端"""
        if not OPENAI_AVAILABLE:
            return

        try:
            if self.settings and self.settings.OPENAI_API_KEY:
                self.client = OpenAI(api_key=self.settings.OPENAI_API_KEY)
                logger.info("OpenAI客户端初始化成功")
            else:
                logger.info("AI评估未启用或缺少API Key，使用传统算法")
        except Exception as e:
            logger.error(f"OpenAI客户端初始化失败: {e}")

    async def _single_operator_evaluate(
        self, content: str, operator: Dict
    ) -> Optional[Dict[str, Any]]:
        """单个操作员执行AI评估"""
        self._initialize()

        if not self.client:
            return

        try:
            if self.eigencloud_client and self.settings.DEVKIT_ENABLED:
                task_result = await self.eigencloud_client.submit_and_wait_for_result(
                    content, "ai_evaluation"
                )

                if task_result and task_result.get("status") == "completed":
                    evaluation_data = task_result.get("result", {})
                    price = evaluation_data.get("price", 0.0)

                    return {
                        "operator_address": operator["address"],
                        "price": price,
                        "confidence": evaluation_data.get("confidence", 0.8),
                        "reasoning": evaluation_data.get(
                            "reasoning", "EigenCloud验证评估"
                        ),
                        "timestamp": datetime.now().isoformat(),
                        "signature": self._create_operator_signature(
                            operator["address"], content, price
                        ),
                        "task_id": task_result.get("task_id"),
                        "verification_proof": task_result.get("proof"),
                    }

            return

        except Exception as e:
            return

    def _extract_price_from_response(self, response: str) -> float:
        """从AI响应中提取价格"""
        import re

        # 查找数字模式
        price_patterns = [
            r"(\d+\.?\d*)\s*ETH",
            r"(\d+\.?\d*)\s*eth",
            r"价格.*?(\d+\.?\d*)",
            r"估价.*?(\d+\.?\d*)",
            r"(\d+\.?\d*)",
        ]

        for pattern in price_patterns:
            matches = re.findall(pattern, response)
            if matches:
                try:
                    price = float(matches[0])
                    return min(max(price, 0.001), 10.0)
                except ValueError:
                    continue

        return 0.01

    def _create_operator_signature(
        self, operator_address: str, content: str, price: float
    ) -> str:
        """创建操作员签名"""
        data = f"{operator_address}:{content}:{price}:{datetime.now().date()}"
        return hashlib.sha256(data.encode()).hexdigest()

    async def evaluate_content_with_consensus(
        self, content: str
    ) -> Optional[Dict[str, Any]]:
        """使用共识机制评估内容"""
        self._initialize()

        if not self.operators:
            logger.error("没有可用的操作员")
            return None

        logger.info(f"开始EigenLayer可验证评估，操作员数量: {len(self.operators)}")

        # 检查EigenCloud健康状态
        if (
            self.settings
            and self.settings.DEVKIT_ENABLED
            and self.eigencloud_client
            and not self.eigencloud_client.health_check()
        ):
            logger.warning("EigenCloud服务不可用，使用本地评估")

        # 并行执行所有操作员的评估
        tasks = [
            self._single_operator_evaluate(content, operator)
            for operator in self.operators
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 过滤有效结果
        valid_results = []
        for result in results:
            if isinstance(result, dict) and result is not None:
                valid_results.append(result)
            elif isinstance(result, Exception):
                logger.error(f"操作员评估异常: {result}")

        consensus_threshold = self.settings.CONSENSUS_THRESHOLD if self.settings else 2
        if len(valid_results) < consensus_threshold:
            logger.error(
                f"有效评估结果不足，需要至少 {consensus_threshold} 个，实际获得 {len(valid_results)} 个"
            )
            return None

        # 计算加权共识
        consensus_result = self._calculate_weighted_consensus(valid_results)

        return {
            "consensus_price": consensus_result["price"],
            "confidence": consensus_result["confidence"],
            "operator_count": len(valid_results),
            "consensus_threshold": consensus_threshold,
            "individual_results": valid_results,
            "consensus_reasoning": consensus_result["reasoning"],
            "verification_timestamp": datetime.now().isoformat(),
            "avs_name": "MoonCL-AI-Evaluator",
            "avs_version": "1.0.0",
            "eigencloud_enabled": (
                self.settings.DEVKIT_ENABLED if self.settings else False
            ),
        }

    def _calculate_weighted_consensus(self, results: list) -> Dict[str, Any]:
        """计算加权共识结果"""
        if not results:
            return {"price": 0.0, "confidence": 0.0, "reasoning": "无有效结果"}

        total_weight = 0
        weighted_price = 0
        weighted_confidence = 0
        reasoning_parts = []

        for result in results:
            # 根据操作员声誉计算权重
            operator_addr = result["operator_address"]
            operator = next(
                (op for op in self.operators if op["address"] == operator_addr), None
            )

            if operator:
                weight = operator.get("stake", 1.0) * operator.get("reputation", 0.8)
            else:
                weight = 1.0

            total_weight += weight
            weighted_price += result["price"] * weight
            weighted_confidence += result.get("confidence", 0.8) * weight

            reasoning_parts.append(
                f"操作员 {operator_addr[:10]}...: {result['price']} ETH"
            )

        if total_weight == 0:
            return {"price": 0.0, "confidence": 0.0, "reasoning": "权重计算错误"}

        final_price = weighted_price / total_weight
        final_confidence = weighted_confidence / total_weight

        # 检查价格偏差
        prices = [r["price"] for r in results]
        max_price = max(prices)
        min_price = min(prices)

        max_deviation = self.settings.MAX_PRICE_DEVIATION if self.settings else 0.3
        if max_price > 0:
            price_deviation = (max_price - min_price) / max_price
            if price_deviation > max_deviation:
                logger.warning(f"价格偏差过大: {price_deviation:.2%}")
                final_confidence *= 0.8  # 降低置信度

        reasoning = f"基于 {len(results)} 个操作员的加权共识: " + "; ".join(
            reasoning_parts
        )

        return {
            "price": round(final_price, 6),
            "confidence": round(final_confidence, 3),
            "reasoning": reasoning,
        }


class AIEvaluator:
    """AI评估器"""

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
            start_idx = content_response.find("{")
            end_idx = content_response.rfind("}") + 1

            if start_idx != -1 and end_idx != 0:
                json_str = content_response[start_idx:end_idx]
                evaluation = json.loads(json_str)

                price = float(evaluation.get("suggested_price_eth", 0.01))
                evaluation["suggested_price_eth"] = max(0.001, min(price, 1.0))
                evaluation["evaluation_method"] = "ai_agent"
                evaluation["evaluated_at"] = datetime.now().isoformat()

                return evaluation

        except Exception as e:
            logger.error(f"AI评估失败: {e}")

        return None


# 全局实例
_ai_evaluator = AIEvaluator()
_eigen_ai_evaluator = EigenVerifiableAIEvaluator()


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


async def calculate_price(content: str, use_eigen: bool = True) -> float:
    """
    智能价格评估算法

    Args:
        content: 要评估的内容
        use_eigen: 是否使用EigenLayer可验证评估（默认True）
    """
    try:
        if use_eigen:
            # 优先使用EigenLayer可验证评估
            eigen_result = await _eigen_ai_evaluator.evaluate_content_with_consensus(
                content
            )
            if eigen_result and "suggested_price_eth" in eigen_result:
                logger.info(
                    f"EigenLayer可验证评估成功: {eigen_result['suggested_price_eth']} ETH"
                )
                logger.info(
                    f"共识参与者: {eigen_result['consensus_participants']}, 总质押: {eigen_result['total_stake']} ETH"
                )
                return float(eigen_result["suggested_price_eth"])
            else:
                logger.warning("EigenLayer评估失败，回退到传统AI评估")

        # 回退到原有的AI评估
        ai_result = await _ai_evaluator.evaluate_content_ai(content)
        if ai_result and "suggested_price_eth" in ai_result:
            logger.info(f"传统AI评估成功: {ai_result['suggested_price_eth']} ETH")
            return float(ai_result["suggested_price_eth"])

    except Exception as e:
        logger.error(f"价格评估失败: {e}")

    # 最后回退到传统算法
    traditional_price = calculate_price_traditional(content)
    logger.info(f"使用传统算法评估: {traditional_price} ETH")
    return traditional_price


async def get_verifiable_evaluation(content: str) -> Optional[Dict[str, Any]]:
    """
    获取完整的EigenLayer可验证评估结果
    """
    try:
        return await _eigen_ai_evaluator.evaluate_content_with_consensus(content)
    except Exception as e:
        logger.error(f"获取可验证评估失败: {e}")
        return None
