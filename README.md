# Clash 免费节点订阅

🤖 **全自动** | 每天自动抓取免费节点，生成固定订阅链接

## 📱 订阅链接

**固定订阅地址**（在 Clash 客户端导入）：

| 格式 | 订阅链接 |
|------|----------|
| **Clash** | `https://raw.githubusercontent.com/fork-svg/clash-node-subscription/main/nodes/clash.yaml` |
| **V2Ray** | `https://raw.githubusercontent.com/fork-svg/clash-node-subscription/main/nodes/v2ray.txt` |

**jsDelivr 加速**（推荐国内用户）：

| 格式 | 订阅链接 |
|------|----------|
| **Clash** | `https://gcore.jsdelivr.net/gh/fork-svg/clash-node-subscription@main/nodes/clash.yaml` |
| **V2Ray** | `https://gcore.jsdelivr.net/gh/fork-svg/clash-node-subscription@main/nodes/v2ray.txt` |

## 🔄 数据来源

节点数据来自：[Clash Free Node](https://clash-free-node.github.io/)

- 每天自动抓取最新免费节点
- 节点覆盖美国、新加坡、日本、香港等多个地区
- 节点可能随时失效，请定期更新订阅

## 📂 项目结构

```
clash-node-subscription/
├── README.md                          # 本文件
├── fetch_nodes.py                     # 抓取脚本
├── nodes/
│   ├── clash.yaml                     # 最新 Clash 配置
│   └── v2ray.txt                      # 最新 V2Ray 配置
└── .github/workflows/daily-fetch.yml  # GitHub Actions 自动任务
```

## 🚀 自动化说明

通过 GitHub Actions 实现全自动运行：

- **触发时间**: 每天 UTC 12:00（北京时间 20:00）
- **流程**: 抓取 → 验证 → 更新节点文件 → 自动提交
- **手动触发**: Actions 页面 → Daily Node Fetch → Run workflow

## 📖 使用方法

### Clash 客户端

1. 打开 Clash / Clash Verge / Clash Meta
2. 点击"配置" → "从 URL 添加"
3. 粘贴上面的 Clash 订阅链接
4. 点击"更新"获取最新节点

### V2Ray 客户端

1. 打开 V2RayN / V2RayNG
2. 点击"订阅" → "添加订阅"
3. 粘贴上面的 V2Ray 订阅链接
4. 点击"更新"获取最新节点

## ⚠️ 注意事项

- 免费节点不稳定，可能随时失效
- 建议定期手动测试节点可用性
- 如有条件，推荐使用付费机场获得更稳定的服务

## 🛠️ 本地使用

```bash
# 手动抓取今天的节点
python3 fetch_nodes.py
```

---

*由 GitHub Actions 自动维护*
