---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: 'e7ee3a9f-33cb-4d5a-93f6-ca7454f13ff1'
  PropagateID: 'e7ee3a9f-33cb-4d5a-93f6-ca7454f13ff1'
  ReservedCode1: 'f5694367-98a5-4414-8605-b04e68945024'
  ReservedCode2: 'f5694367-98a5-4414-8605-b04e68945024'
---

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

## 🎨 图标美化（Koolson/Qure，已自托管）

本配置的**全部策略组与任务脚本图标已内置**（Qure 图标固化到本仓库 `icons/` 目录，与配置同源，不依赖外部仓库可达性），导入即显示，无需额外订阅。

若想用更全的彩色/纯白图标订阅（可选）：

1. 打开 Quantumult X → 右下角**风车** → **其他设置** → **图标**
2. 图标订阅 URL 填入（彩色版）：

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

## 🚀 启动页去广告（菜鸟 / 喜马拉雅 / 闲鱼 / 迅雷 / 百度网盘 / 万年历 等）

配置内置 **App-Killers 合并重写包**（`rewrite-local/App-Killers.conf`），合并自两个活跃维护的规则库并全部本地化（内部 14 个 .js 脚本固化在本仓库 `scripts/`，无断流子资源）：

| App | 覆盖内容 |
|---|---|
| 菜鸟裹裹 | 开屏拦截 + 首页推广/角标/裹裹券（fmz200 深度规则 + 墨鱼启动页） |
| 喜马拉雅 | 开屏广告域 reject + 搜索热词/弹窗/直播角标/首页广告（fmz200 + 墨鱼） |
| 闲鱼 | 开屏 splash.ads + 信息流/搜索推荐/首页 banner（fmz200 2026-09 补齐） |
| 迅雷 | adsp/xlmc 等 16 广告域 reject + advert 素材/slots 接口 reject-200（fmz200 2026-09 补齐） |
| 百度网盘 | 活动弹窗/福利页/广告 CDN/开屏（fmz200 + 墨鱼） |
| 365日历(万年历) | 广告域拦截（fmz200） |
| 另含 200+ 国内 App | 12306/京东/小红书/美团/拼多多/58 等启动页（墨鱼 startingad） |

> ⚠️ 部分规则首次生效需**清除对应 App 的缓存**（或卸载重装后首次启动时拦截），App 会缓存已下载的广告素材。

### 🍎 系统级补充：iOS 27.2「限制动作数据」（2026-11 新增）

摇一摇/晃动跳转类开屏广告，苹果已在系统层出手，**建议与本配置叠加使用**：

1. 将 iPhone 升级到 **iOS 27.2 正式版**（2026-10-27 发布，此功能国行专属，需登录中国大陆区 Apple ID）
2. 设置 → 隐私与安全性 → 运动与健身 → **限制动作数据** → 右上角「编辑」
3. 把爱弹摇一摇广告的 App（百度网盘、闲鱼、喜马拉雅、菜鸟、迅雷等）逐一加入限制名单
4. 加入后 App 无法读取加速度计/陀螺仪数据，**晃动手机不会再触发广告跳转**

> ⚠️ 已知绕过：百度网盘 2026-11 被发现用 "no shake" 方式实现（不依赖传感器数据），官方称适配版本即将上线。此类顽固 App 仍需依赖本配置的 MITM 重写拦截。
>
> 💡 工具选型参考：Quantumult X 不支持对 **TCP 长连接** 做 MITM（如起点读书等 App 的广告走 TCP 连接，QX 拦不到）。顽固 App 若本配置仍拦不住，可考虑 Loon 或 Surge（均支持 TCP 连接解密，规则生态同样活跃，fmz200 仓库同时提供 Loon/Surge 格式）。

### 闲鱼/迅雷 2026-09 根治说明

两大 App 此前拦不住的根因与修复：
- **闲鱼**：上游合并源中无任何闲鱼规则（App-Killers 旧版闲鱼段为空）→ 新增 fmz200 XianYu.snippet（开屏 `idlecommerce.splash.ads` reject-dict + 22 条深度净化规则 + goofish.js 信息流脚本）
- **迅雷**：旧版三重放行（`xunlei.com/sandai.net` 整域直连 + MITM 整域负条目 + 无广告规则）→ 改为仅放行 3 个登录/业务接口，广告域 adsp/xlmc/ct.niu 等全部可拦截，MITM 负条目仅保留 id6.me

## 🛡️ 误伤修复白名单（迅雷 / QQ同步助手）

`[filter_local]` 顶部内置直连白名单（本地规则优先于远程 REJECT）：

| 域名 | 原因 |
|---|---|
| `api-u-ssl.xunlei.com` | blackmatrix7 Advertising 误杀迅雷登录接口 → 精确放行 |
| `api-shoulei-ssl.xunlei.com` | 迅雷业务接口（与广告 slots 接口同域，广告路径由 URL 级重写精确拦截） |
| `hub5emu.wap.sandai.net` | 迅雷登录业务接口 |
| `id6.me` | blackmatrix7 Privacy 误杀腾讯统一账号验证服务（QQ同步助手登录用） |
| `sync.qq.com` | QQ同步助手 API 出境（走代理）时腾讯判定境外 IP → 「该国家地区未开通服务」 |

> ⚠️ QX 需使用**规则分流**模式。若切到「全部代理」模式，QQ同步助手等国产 App 仍会判定境外 IP。
>
> ⚠️ 若迅雷登录再次异常，临时回退方案：编辑 `.conf` 在上述迅雷三行前后恢复旧整域直连
> `host-suffix, xunlei.com, direct` / `host-suffix, sandai.net, direct`（代价：迅雷广告回到不拦截状态）。

### 🔁 2026-11 迭代记录（上游规则巡检 + 脚本升级）

| 变更 | 说明 |
|---|---|
| `goofish.js` 升级 2026-08-14 → **2026-10-24 版** | 上游树先生适配闲鱼新版界面（顶部回收按钮动态图 `rightTagImage` 置空、首页圈子列表清理、个人页工具栏简化） |
| 修复菜鸟 amdc 规则误剔除 | 9 月根治时只豁免了闲鱼源的 amdc 广告下发拦截，菜鸟源被黑名单误杀，本次补上 |
| AdSDK-Fallback.list 新增 `fc-video.cdn.bcebos.com` | 百度网盘视频流广告素材 CDN，分流级 REJECT（无需 MITM，无证书校验风险） |
| 上游巡检结论 | fmz200 五大 App snippet、墨鱼 startingad 与 9 月基线完全一致；规则生态稳定，App 广告接口近期未变化 |

### 🚨 2026-11-14 系统性修复（"各种开屏都拦不住"的根因）

**根因**：主配置里 5 条核心广告分流列表（去广告精简 / 开屏专项 / HTTPDNS 拦截 / 隐私 / 防劫持）此前走 `raw.githubusercontent.com` 直链——国内拉取失败时 QX 静默降级继续运行，**手机上广告域名列表整体缺失**，表现为所有 App 开屏广告全量放行。

| 变更 | 说明 |
|---|---|
| 5 条 hwind 核心分流列表 raw → **jsdelivr** | 消除国内拉取失败；上游每日自动更新（BlockHttpDNS 当天 08:49 仍在更新） |
| task_local 脚本拉取 raw → jsdelivr | splash-killer.js / feed-killer.js 每日 04:00 拉取不再断流 |
| AdSDK-Fallback 新增 pangle.cn / pangle.io / pangleglobal.com | 穿山甲海外主域兜底 |
| AdSDK-Fallback 新增 tanx.com / alimama.com | 阿里妈妈/汇川广告交易域（纯广告域，无正常业务） |

> 📱 **生效前提（设备端三步，缺一不可）**：
> 1. QX 配置文件长按 → 更新；到「分流」页确认 5 条列表**行数 > 0 且无红色报错**
> 2. 设置 → HTTPS 解密 → 证书状态正常；iOS 系统设置 → 通用 → 关于本机 → 证书信任设置 → QX CA **开关开启**（iOS 大版本升级后此开关常被重置，需复查）
> 3. 目标 App **卸载重装**（清掉已缓存的开屏素材，缓存广告不走网络、规则拦不到）

## 🔗 集成的资源

| 段位 | 来源 | 数量 | 说明 |
|---|---|---|---|
| `[filter_remote]` | hwind2021 + blackmatrix7 | 20 条 | 国内精准 + 海外兜底 |
| `[rewrite_remote]` | hwind2021 + blackmatrix7 + deezertidal + fmz200 | 8 条 | 含 App-Killers 本地化合并包 |
| `[mitm]` | hwind2021 + App-Killers | 168 + 250 域名 | 广告 SDK 与开屏追踪 |
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

> AI生成