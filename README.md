<div align="center">

# Quantumult X · 国内化主配置 (Profile-CN)

**Quantumult X 主界面订阅用的完整 `.conf` 主配置 · 集成 hwind2021 国内精准规则 + blackmatrix7 兜底分流 + 黑猫/KOP-XIAO 节点模板**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Maintained](https://img.shields.io/badge/Maintained-yes-green.svg)](https://github.com/hwind2021/QuantumultX-Profile-CN/commits/main)
[![Source](https://img.shields.io/badge/Upstream-KOP--XIAO%2FQuantumultX-blue)](https://github.com/KOP-XIAO/QuantumultX)

</div>

---

## 📌 这是什么

Quantumult X 主界面底部**「配置文件」→「从 URL 下载」**用的 `.conf` 完整主配置，
把多个 GitHub 仓库（自有规则集 + 第三方分流 + 上游模板）的资源，
整合成**一个文件导入即用**的主配置。

- 用户只需**填一行机场订阅**（`[server_remote]` 段）即可正常连接
- 所有分流、重写、定时任务通过远程订阅自动拉取，按预设策略分发
- 不需要再单独维护十几条订阅链接

## ✨ 相对其它方案的优势

| 维度 | 主流做法 | 本仓库做法 |
|---|---|---|
| 主配置来源 | 各处拼凑、零散 | **一个 .conf 走完** |
| 分流来源 | 单一源，失效就空 | 国内精准 (hwind2021) + 兜底 (blackmatrix7) |
| 重写来源 | 单一源 | 4 条专项重写 (All/Feed/Splash/Script) |
| MITM 名单 | 自己维护 | 整合自 hwind2021 168 个广告域名 |
| 开屏广告 | 不支持 | ✅ 集成 `splash-killer.js` 实时拦截 |
| 信息流广告 | 不支持 | ✅ 集成 `feed-killer.js` 清理 |
| 自动更新 | 无 | ✅ Actions 每周拉上游重构并提交 |

## 🚀 5 分钟接入 iOS Quantumult X

订阅 URL（任选，国内用 jsdelivr 镜像）：

```
# GitHub raw（海外）
https://raw.githubusercontent.com/hwind2021/QuantumultX-Profile-CN/main/QuantumultX_Profiles.conf

# jsdelivr CDN（推荐国内）
https://cdn.jsdelivr.net/gh/hwind2021/QuantumultX-Profile-CN@main/QuantumultX_Profiles.conf
```

### 步骤

1. **编辑配置文件**（第一次必须做一次）：用编辑器打开 `QuantumultX_Profiles.conf`
   - 找到第 N 行 `[server_remote]` 段
   - **替换**示例注释行为你的机场订阅 URL（保留 `, tag=…` 那个参数行即可）
   - 保存
2. **上传到 iOS**（任选其一）：
   - 用 iCloud Drive 把文件放到「Quantumult X」目录
   - 或用「文件」App 推到 `On My iPhone → Quantumult X → Profiles`
3. **打开 Quantumult X**：
   - 底部「配置文件」→ 长按 →「从 URL 链接下载」
   - 粘贴上面的 jsdelivr URL → 确认
   - 等 5~10 秒，节点列表会自动拉取
4. **首次启用 MITM**：
   - 设置 → HTTPS 解密 → 生成密钥 → 安装 CA 描述文件 → 信任
   - 开启「HTTPS 解密」
5. **连上**：底部「首页」→ 选个节点 → 启动 VPN

> ⚠️ 如果最后出现「节点为空」，回到第 1 步检查 `[server_remote]` 的订阅 URL 是否正确填入。

## 🧩 段位结构

主配置包含以下段位（可在 `.conf` 文件里直接查看）：

```
[general]                  # 全局参数（已配置：geosite/ss_check/DNS 等）
[server]                   # 本地节点（空）
[server_remote]            # ★ 你的机场订阅（要手动填）
[policy]                   # 策略组（自动选择 / 故障转移 / 节点订阅 / 各国分流 / 流媒体 / AI）
[policy_url]               # 远程策略组备份
[filter_local] / [filter_remote]   # 分流规则（20 条）
[rewrite_local] / [rewrite_remote] # 重写规则（7 条）
[server_local]
[task_local]               # 定时任务（含 splash-killer.js / feed-killer.js 每日拉取）
[mitm]                     # 168 个广告 SDK hostname（需开启 HTTPS 解密）
```

## 🎨 图标美化（Koolson/Qure）

本配置内置了 [Koolson/Qure](https://github.com/Koolson/Qure) 图标集引用（任务脚本图标已全部替换）。
如需**策略组也带图标**，在 Quantumult X 里一键订阅图标：

1. 打开 Quantumult X → 右下角**风车** → **其他设置** → **图标**
2. 图标订阅 URL 填入（彩色版，含 Netflix/YouTube/香港/日本等全部策略组图标）：

```
https://cdn.jsdelivr.net/gh/Koolson/Qure@master/Other/QureColor.json
```

纯白极简版（PROXY 订阅推荐）：

```
https://cdn.jsdelivr.net/gh/Koolson/Qure@master/Other/Quremini.json
```

## ⚡ 定时自动测速（选最快节点）

配置内置策略组 **⚡ 极速测速**（`url-latency-benchmark` 类型），填入机场订阅后自动生效：

| 参数 | 值 | 说明 |
|---|---|---|
| `check-interval` | 600 秒 | 每 10 分钟自动测速一轮 |
| `alive-checking` | true | **空闲时也定时测速**（核心参数，关掉就变成"有流量才测"） |
| `tolerance` | 0 | 发现更快节点立即切换；想防抖可改成 100 |

使用方式：主界面 → 策略 → **节点选择** → 切到 **⚡ 极速测速** 即可。
依赖 `[general]` 的 `server_check_url`（已配置为 `cp.cloudflare.com/generate_204`，无需修改）。

## 🔗 集成的资源

| 段位 | 来源 | 数量 | 说明 |
|---|---|---|---|
| `[filter_remote]` | hwind2021 + blackmatrix7 | 20 条 | 国内精准 + 海外兜底 |
| `[rewrite_remote]` | hwind2021 + blackmatrix7 | 7 条 | All/Feed/Splash/Script/Upgrade 等 |
| `[mitm]` | hwind2021 | 168 域名 | 广告 SDK 与开屏追踪 |
| `[task_local]` | hwind2021 + 自有 | 多条 | 每日自动拉取 .js 脚本 |

完整来源清单见 [docs/sources.md](docs/sources.md)。

## 🔄 自动更新机制

本仓库使用 GitHub Actions 维护：

- **每周** 04:00 (UTC+8) 自动跑 `auto-update.yml`：
  1. 拉上游 KOP-XIAO 的模板段位
  2. 拉 hwind2021 / blackmatrix7 的最新规则文件
  3. 跑 `build_conf.py` 重新生成 `QuantumultX_Profiles.conf`
  4. 校验段位齐全、URL 可达
  5. 若变更则自动 commit（**不会**修改你的机场订阅行）

也可以手动触发：`Actions` → `Auto-update QuantumultX profile` → `Run workflow`

## 🛠 本地重新构建

如果你想自己重新合成：

```bash
git clone https://github.com/hwind2021/QuantumultX-Profile-CN
cd QuantumultX-Profile-CN
python build_conf.py
```

`build_conf.py` 会：
- 重新下载 hwind2021/blackmatrix7 的最新 `.list` / `.conf`
- 重新解析段位
- 输出新的 `QuantumultX_Profiles.conf`
- 上游变更时自动同步 KOP-XIAO 模板

## ❓ 常见问题

**Q1：装上后所有网站都走「代理」没法访问国内？**
A：检查 `[filter_remote]` 里 `China/China.list` 是否被启用（默认开启）。如果还是不行，可能 `[policy]` 里的「节点订阅」组没匹配上。

**Q2：开屏广告没拦掉？**
A：`splash-killer.js` 走 MITM，去设置 → HTTPS 解密 → 信任 CA。

**Q3：机场订阅改怎么填？**
A：登录机场官网 → 我的订阅 → 复制 URL，替换 `[server_remote]` 注释示例行。

**Q4：能否去掉开屏广告脚本？**
A：编辑 `.conf` 把 `splash-killer.js / feed-killer.js` 相关的 `[task_local]` 行注释掉（行首加 `;`），下次开机就不跑了。

## 📄 License

MIT — 详见 [LICENSE](LICENSE)。

## 🙏 致谢

- 上游模板：[KOP-XIAO/QuantumultX](https://github.com/KOP-XIAO/QuantumultX) — Quantumult X 配置骨架
- 国内精准分流：[hwind2021/QuantumultX-AdBlock-CN](https://github.com/hwind2021/QuantumultX-AdBlock-CN)
- 海外兜底规则：[blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)
- QX 脚本：[chavyleung/scripts](https://github.com/chavyleung/scripts)

## 🔗 配套订阅链接（可选单独使用）

如果想脱离主配置分别订阅各段位，原始链接见 [docs/sources.md](docs/sources.md)。
