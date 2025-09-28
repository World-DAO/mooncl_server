#!/usr/bin/env python3
"""
合约调用测试脚本
用于测试 AiTextNFT 合约的各种功能
"""


import sys
import os
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from web3 import Web3
from app.utils.evm_client import evm_client
from app.config import settings


def test_connection():
    """测试区块链连接"""
    print("🔗 测试区块链连接...")
    try:
        # 检查连接状态
        if not evm_client.w3.is_connected():
            print("❌ 无法连接到区块链网络")
            return False

        # 获取最新区块号
        latest_block = evm_client.w3.eth.block_number
        print(f"✅ 连接成功！当前区块高度: {latest_block}")

        # 检查网络ID
        chain_id = evm_client.w3.eth.chain_id
        print(f"📡 网络ID: {chain_id}")

        # Celo Alfajores 测试网的 Chain ID 是 44787
        if chain_id == 44787:
            print("🌍 当前连接到 Celo Alfajores 测试网")
        elif chain_id == 42220:
            print("🌍 当前连接到 Celo 主网")
        else:
            print(f"⚠️  未知的 Celo 网络 (Chain ID: {chain_id})")

        return True
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False


def test_contract_deployment():
    """测试合约是否正确部署"""
    print("\n📋 测试合约部署状态...")
    try:
        if not settings.NFT_CONTRACT_ADDRESS:
            print("❌ 合约地址未配置")
            return False

        print(f"📍 合约地址: {settings.NFT_CONTRACT_ADDRESS}")

        # 检查合约代码
        code = evm_client.w3.eth.get_code(settings.NFT_CONTRACT_ADDRESS)
        if code == b"":
            print("❌ 合约地址无代码，可能未部署或地址错误")
            return False

        print("✅ 合约已正确部署到 Celo 网络")
        return True
    except Exception as e:
        print(f"❌ 合约检查失败: {e}")
        return False


def test_contract_read_functions():
    """测试合约只读函数"""
    print("\n📖 测试合约只读函数...")
    try:
        # 测试获取下一个ID
        try:
            next_id = evm_client.contract.functions.nextId().call()
            print(f"✅ 下一个Token ID: {next_id}")
        except Exception as e:
            print(f"⚠️  获取nextId失败: {e}")

        # 测试获取Market地址
        try:
            market_address = evm_client.get_market_address()
            if market_address:
                print(f"✅ Market地址: {market_address}")
            else:
                print("⚠️  Market地址未设置")
        except Exception as e:
            print(f"⚠️  获取Market地址失败: {e}")

        # 测试合约名称和符号
        try:
            name = evm_client.contract.functions.name().call()
            symbol = evm_client.contract.functions.symbol().call()
            print(f"✅ 合约名称: {name}")
            print(f"✅ 合约符号: {symbol}")
        except Exception as e:
            print(f"⚠️  获取合约基本信息失败: {e}")

        return True
    except Exception as e:
        print(f"❌ 只读函数测试失败: {e}")
        return False


def test_account_setup():
    """测试账户设置"""
    print("\n👤 测试账户设置...")
    try:
        if not settings.PRIVATE_KEY:
            print("❌ 私钥未配置")
            return False

        # 从私钥创建账户
        account = evm_client.w3.eth.account.from_key(settings.PRIVATE_KEY)
        print(f"✅ 账户地址: {account.address}")

        # 检查账户余额
        balance_wei = evm_client.w3.eth.get_balance(account.address)
        balance_celo = evm_client.w3.from_wei(balance_wei, "ether")
        print(f"💰 账户余额: {balance_celo:.6f} CELO")

        if balance_wei == 0:
            print("⚠️  账户余额为0，无法发送交易")
            print("💡 提示: 请从 Celo 水龙头获取测试代币")
            print("🚰 Alfajores 水龙头: https://faucet.celo.org/alfajores")
            return False

        return True
    except Exception as e:
        print(f"❌ 账户设置测试失败: {e}")
        return False


def test_gas_estimation():
    """测试Gas估算"""
    print("\n⛽ 测试Gas估算...")
    try:
        account = evm_client.w3.eth.account.from_key(settings.PRIVATE_KEY)

        # 模拟mintToWithContent调用进行Gas估算
        test_address = account.address
        test_content = "test content"
        test_uri = "data:application/json;base64,eyJ0ZXN0IjoidGVzdCJ9"

        # 估算Gas - 使用正确的方法
        gas_estimate = evm_client.contract.functions.mintToWithContent(
            test_address, test_uri, test_content.encode("utf-8")
        ).estimate_gas({"from": account.address})

        print(f"✅ 估算Gas用量: {gas_estimate}")

        # 获取当前Gas价格
        gas_price = evm_client.w3.eth.gas_price
        gas_price_gwei = evm_client.w3.from_wei(gas_price, "gwei")
        print(f"✅ 当前Gas价格: {gas_price_gwei:.2f} Gwei")

        # 计算交易成本
        tx_cost_wei = gas_estimate * gas_price
        tx_cost_celo = evm_client.w3.from_wei(tx_cost_wei, "ether")
        print(f"💸 预估交易成本: {tx_cost_celo:.6f} CELO")

        return True
    except Exception as e:
        print(f"❌ Gas估算失败: {e}")
        return False


def test_celo_specific_features():
    """测试 Celo 特定功能"""
    print("\n🌍 测试 Celo 特定功能...")
    try:
        # 检查网络信息
        chain_id = evm_client.w3.eth.chain_id

        celo_networks = {
            42220: ("Celo Mainnet", "https://celoscan.io"),
            44787: ("Celo Alfajores Testnet", "https://alfajores.celoscan.io"),
            11142220: ("Celo Sepolia Testnet", "https://sepolia.celoscan.io"),
        }

        network_name, explorer_url = celo_networks.get(
            chain_id, ("Unknown Celo Network", "")
        )

        print(f"✅ 连接到 {network_name}")
        if explorer_url:
            print(f"🔍 区块浏览器: {explorer_url}")

        # 检查 RPC 端点
        print(f"🌐 RPC 端点: {settings.EVM_RPC_URL}")

        return True
    except Exception as e:
        print(f"❌ Celo 特定功能测试失败: {e}")
        return False


def test_mint_nft():
    """测试铸造NFT（实际交易）"""
    print("\n🎨 测试铸造NFT...")

    # 询问用户是否要执行实际交易
    response = input(
        "⚠️  这将在 Celo 网络上执行实际的区块链交易并消耗Gas费用。是否继续？(y/N): "
    )
    if response.lower() != "y":
        print("⏭️  跳过实际交易测试")
        return True

    try:
        account = evm_client.w3.eth.account.from_key(settings.PRIVATE_KEY)

        # 测试数据
        test_content = "这是一个测试观点内容，用于验证在 Celo 网络上的 NFT 铸造功能"
        recipient_address = account.address

        print(f"📝 测试内容: {test_content}")
        print(f"📍 接收地址: {recipient_address}")

        # 执行铸造
        result = evm_client.mint_nft(
            opinion_id=999,  # 测试用ID
            content=test_content,
            recipient_address=recipient_address,
        )

        if result["success"]:
            print("✅ NFT 在 Celo 网络上铸造成功！")
            print(f"🔗 交易哈希: {result['transaction_hash']}")
            print(f"🎫 Token ID: {result['token_id']}")
            print(f"🔐 文本哈希: {result['text_hash']}")
            print(f"⛽ Gas消耗: {result['gas_used']}")

            # 提供 Celo 区块浏览器链接
            chain_id = evm_client.w3.eth.chain_id
            if chain_id == 44787:  # Alfajores 测试网
                explorer_url = (
                    f"https://alfajores.celoscan.io/tx/{result['transaction_hash']}"
                )
                print(f"🔍 Celoscan 链接: {explorer_url}")

            # 验证铸造结果
            if result["token_id"]:
                print("\n🔍 验证铸造结果...")

                # 检查Token URI
                token_uri = evm_client.get_nft_metadata(result["token_id"])
                if token_uri:
                    print(f"✅ Token URI: {token_uri[:100]}...")

                # 检查文本哈希
                stored_hash = evm_client.get_text_hash(result["token_id"])
                if stored_hash:
                    print(f"✅ 存储的文本哈希: {stored_hash}")

            return True
        else:
            print(f"❌ NFT铸造失败: {result['error']}")
            return False

    except Exception as e:
        print(f"❌ 铸造测试失败: {e}")
        return False


def test_celo_specific_features():
    """测试 Celo 特定功能"""
    print("\n🌍 测试 Celo 特定功能...")
    try:
        # 检查网络信息
        chain_id = evm_client.w3.eth.chain_id

        if chain_id == 44787:
            print("✅ 连接到 Celo Alfajores 测试网")
            print("🚰 水龙头地址: https://faucet.celo.org/alfajores")
            print("🔍 区块浏览器: https://alfajores.celoscan.io/")
        elif chain_id == 42220:
            print("✅ 连接到 Celo 主网")
            print("🔍 区块浏览器: https://celoscan.io/")
        else:
            print(f"⚠️  未知的网络 Chain ID: {chain_id}")

        # 检查 RPC 端点
        print(f"🌐 RPC 端点: {settings.EVM_RPC_URL}")

        return True
    except Exception as e:
        print(f"❌ Celo 特定功能测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🚀 开始 Celo 网络合约调用测试...\n")

    # 检查配置
    print("⚙️  检查配置...")
    if not settings.EVM_RPC_URL:
        print("❌ EVM_RPC_URL 未配置")
        return
    if not settings.NFT_CONTRACT_ADDRESS:
        print("❌ NFT_CONTRACT_ADDRESS 未配置")
        return
    if not settings.PRIVATE_KEY:
        print("❌ PRIVATE_KEY 未配置")
        return

    print("✅ 基本配置检查通过")
    print(f"🌐 RPC URL: {settings.EVM_RPC_URL}")
    print(f"📍 合约地址: {settings.NFT_CONTRACT_ADDRESS}\n")

    # 执行测试
    tests = [
        ("Celo 连接测试", test_connection),
        ("合约部署测试", test_contract_deployment),
        ("只读函数测试", test_contract_read_functions),
        ("账户设置测试", test_account_setup),
        ("Gas估算测试", test_gas_estimation),
        ("Celo 特定功能测试", test_celo_specific_features),
        ("NFT铸造测试", test_mint_nft),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}异常: {e}")
            results.append((test_name, False))

    # 输出测试结果汇总
    print("\n" + "=" * 50)
    print("📊 Celo 网络测试结果汇总:")
    print("=" * 50)

    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1

    print(f"\n总计: {passed}/{len(results)} 项测试通过")

    if passed == len(results):
        print("🎉 所有测试通过！Celo 网络合约调用配置正确。")
    else:
        print("⚠️  部分测试失败，请检查配置和网络连接。")
        print("\n💡 常见问题排查:")
        print("1. 确保 RPC URL 正确且可访问")
        print("2. 确保合约地址已正确部署到 Celo 网络")
        print("3. 确保账户有足够的 CELO 代币支付 Gas 费用")
        print("4. 如果是测试网，请从水龙头获取测试代币")


if __name__ == "__main__":
    main()
