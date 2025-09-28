from datetime import datetime


def calculate_opinion_price(content: str, created_at: datetime) -> float:
    """
    观点价格评估算法

    Args:
        content: 观点内容
        created_at: 创建时间

    Returns:
        评估价格
    """
    # 基础价格
    base_price = 0.01

    # 内容长度因子 (最大2倍)
    content_length_factor = min(len(content) / 100, 2.0)

    # 时间因子 (随时间递减，最小0.5倍)
    days_old = (datetime.utcnow() - created_at).days
    time_factor = max(0.5, 1 - (days_old * 0.01))

    # 计算最终价格
    final_price = base_price * content_length_factor * time_factor

    return round(final_price, 6)
