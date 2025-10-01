import asyncio
import json
import logging
import hashlib
import requests
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class EigenCloudClient:
    """EigenCloud客户端"""

    def __init__(self):
        self.verification_endpoint = ""
        self.aggregator_endpoint = ""
        self.timeout = 300
        self.max_retries = 3
        self.enabled = True

    def _create_task_hash(self, content: str, timestamp: str) -> str:
        task_data = f"{content}:{timestamp}:{"MoonCL-AI-Evaluator"}"
        return hashlib.sha256(task_data.encode()).hexdigest()

    async def submit_verification_task(
        self, content: str, task_type: str = "ai_evaluation"
    ) -> Optional[str]:
        """提交验证任务到EigenCloud"""
        if not self.enabled:
            logger.info("EigenCloud未启用，跳过任务提交")
            return None

        timestamp = datetime.now(timezone.utc).isoformat()
        task_hash = self._create_task_hash(content, timestamp)

        task_data = {
            "task_id": task_hash,
            "task_type": task_type,
            "content": content,
            "timestamp": timestamp,
            "avs_name": "MoonCL-AI-Evaluator",
            "avs_version": "1.0.0",
            "consensus_threshold": 2,
            "timeout": self.timeout,
        }

        try:
            response = requests.post(
                f"{self.verification_endpoint}/submit",
                json=task_data,
                timeout=self.timeout,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            result = response.json()
            logger.info(f"任务提交成功: {task_hash}")
            return result.get("task_id", task_hash)
        except requests.exceptions.RequestException as e:
            logger.error(f"提交验证任务失败: {e}")
            return None
        except Exception as e:
            logger.error(f"提交任务时发生未知错误: {e}")
            return None

    async def get_verification_result(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取验证结果"""
        if not self.enabled:
            return None

        for attempt in range(self.max_retries):
            try:
                response = requests.get(
                    f"{self.verification_endpoint}/result/{task_id}",
                    timeout=self.timeout,
                    headers={"Accept": "application/json"},
                )
                response.raise_for_status()
                result = response.json()

                if result.get("status") == "completed":
                    logger.info(f"获取验证结果成功: {task_id}")
                    return result
                elif result.get("status") == "pending":
                    logger.info(f"任务仍在处理中: {task_id}, 等待重试...")
                    await asyncio.sleep(10)  # 等待10秒后重试
                    continue
                else:
                    logger.warning(f"任务状态异常: {result.get('status')}")
                    return None

            except requests.exceptions.RequestException as e:
                logger.error(
                    f"获取验证结果失败 (尝试 {attempt + 1}/{self.max_retries}): {e}"
                )
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(5)  # 等待5秒后重试
                continue
            except Exception as e:
                logger.error(f"获取结果时发生未知错误: {e}")
                return None

        logger.error(f"获取验证结果最终失败: {task_id}")
        return None

    async def aggregate_results(self, task_ids: List[str]) -> Optional[Dict[str, Any]]:
        """聚合多个验证结果"""
        if not self.enabled or not task_ids:
            return None

        try:
            response = requests.post(
                f"{self.aggregator_endpoint}/aggregate",
                json={
                    "task_ids": task_ids,
                    "consensus_threshold": 2,
                },
                timeout=self.timeout,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            result = response.json()
            logger.info(f"聚合结果成功: {len(task_ids)} 个任务")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"聚合结果失败: {e}")
            return None
        except Exception as e:
            logger.error(f"聚合时发生未知错误: {e}")
            return None

    async def submit_and_wait_for_result(
        self, content: str, task_type: str = "ai_evaluation"
    ) -> Optional[Dict[str, Any]]:
        """提交任务并等待结果"""
        task_id = await self.submit_verification_task(content, task_type)
        if not task_id:
            return None

        # 等待结果
        result = await self.get_verification_result(task_id)
        return result

    def health_check(self) -> bool:
        """健康检查"""
        if not self.enabled:
            return True

        try:
            response = requests.get(f"{self.verification_endpoint}/health", timeout=10)
            return response.status_code == 200
        except:
            return False


# 全局客户端实例
eigencloud_client = EigenCloudClient()
