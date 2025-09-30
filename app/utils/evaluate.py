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
        self.operators = [
            {"address": "0x1234...op1", "stake": 100.0, "reputation": 0.95},
            {"address": "0x5678...op2", "stake": 150.0, "reputation": 0.92},
            {"address": "0x9abc...op3", "stake": 200.0, "reputation": 0.98},
        ]
        self._initialize_client()

    def _initialize_client(self):
        """初始化客户端"""
        if not OPENAI_AVAILABLE:
            return

        try:
            if settings.OPENAI_API_KEY:
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                logger.info("EigenLayer AI评估器初始化成功")
            else:
                logger.info("AI评估未启用或缺少API Key，使用传统算法")
        except Exception as e:
            logger.error(f"EigenLayer AI评估器初始化失败: {e}")

    async def _single_operator_evaluate(
        self, content: str, operator: Dict
    ) -> Optional[Dict[str, Any]]:
        """单个操作员执行AI评估"""
        if not self.client:
            return None

        try:
            prompt = f"""
            作为EigenLayer操作员，分析以下NFT内容的价值：

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
                    {
                        "role": "system",
                        "content": f"你是EigenLayer网络中的操作员 {operator['address']}，负责提供可验证的NFT评估。",
                    },
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

                # 验证和标准化数据
                price = float(evaluation.get("suggested_price_eth", 0.01))
                evaluation["suggested_price_eth"] = max(0.001, min(price, 1.0))

                # 添加操作员信息和签名
                evaluation["operator"] = {
                    "address": operator["address"],
                    "stake": operator["stake"],
                    "reputation": operator["reputation"],
                }

                # 创建简化的操作员签名
                evaluation["signature"] = self._create_operator_signature(
                    operator["address"], content, evaluation["suggested_price_eth"]
                )

                evaluation["evaluated_at"] = datetime.now().isoformat()
                return evaluation

        except Exception as e:
            logger.error(f"操作员 {operator['address']} 评估失败: {e}")
            return None

    def _create_operator_signature(
        self, operator_address: str, content: str, price: float
    ) -> str:
        """创建操作员签名"""
        data = (
            f"{operator_address}{content}{price}{datetime.now().strftime('%Y-%m-%d')}"
        )
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    async def evaluate_content_with_consensus(
        self, content: str
    ) -> Optional[Dict[str, Any]]:
        """通过EigenLayer操作员共识评估内容"""
        if not self.client:
            return None

        try:
            # 并行执行多个操作员的评估
            evaluation_tasks = [
                self._single_operator_evaluate(content, operator)
                for operator in self.operators
            ]

            results = await asyncio.gather(*evaluation_tasks, return_exceptions=True)

            # 过滤有效结果
            valid_results = [
                r for r in results if isinstance(r, dict) and "suggested_price_eth" in r
            ]

            if len(valid_results) < 2:
                logger.warning("EigenLayer共识失败，操作员评估结果不足")
                return None

            # 计算加权共识（基于质押量和声誉）
            consensus_result = self._calculate_weighted_consensus(valid_results)

            # 添加EigenLayer验证信息
            consensus_result.update(
                {
                    "evaluation_method": "eigen_consensus",
                    "consensus_participants": len(valid_results),
                    "total_stake": sum(r["operator"]["stake"] for r in valid_results),
                    "avg_reputation": sum(
                        r["operator"]["reputation"] for r in valid_results
                    )
                    / len(valid_results),
                    "eigen_verified": True,
                    "verification_proof": {
                        "operator_signatures": [r["signature"] for r in valid_results],
                        "consensus_algorithm": "stake_weighted_average",
                        "slashing_conditions": "price_deviation > 50%",
                    },
                }
            )

            logger.info(
                f"EigenLayer共识评估完成: {consensus_result['suggested_price_eth']} ETH"
            )
            return consensus_result

        except Exception as e:
            logger.error(f"EigenLayer共识评估失败: {e}")
            return None

    def _calculate_weighted_consensus(self, results: list) -> Dict[str, Any]:
        """计算基于质押量的加权共识"""
        total_stake = sum(r["operator"]["stake"] for r in results)

        # 加权平均计算各项指标
        weighted_scores = {}
        for key in [
            "creativity_score",
            "artistic_value",
            "rarity_score",
            "emotional_impact",
            "market_potential",
            "suggested_price_eth",
        ]:
            weighted_sum = sum(r.get(key, 0) * r["operator"]["stake"] for r in results)
            weighted_scores[key] = weighted_sum / total_stake

        # 计算总分
        weighted_scores["overall_score"] = (
            weighted_scores["creativity_score"]
            + weighted_scores["artistic_value"]
            + weighted_scores["rarity_score"]
            + weighted_scores["emotional_impact"]
            + weighted_scores["market_potential"]
        ) / 5

        # 合并推理
        reasoning_parts = [
            r.get("reasoning", "") for r in results if r.get("reasoning")
        ]
        weighted_scores["reasoning"] = (
            f"EigenLayer共识评估（{len(results)}个操作员）: "
            + "; ".join(reasoning_parts[:2])
        )

        return weighted_scores


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
