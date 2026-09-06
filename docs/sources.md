---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: '60f5e094-352c-4d42-a088-ba21049e2c1f'
  PropagateID: '60f5e094-352c-4d42-a088-ba21049e2c1f'
  ReservedCode1: '57009ed0-1939-41da-9b54-7d8f05855d73'
  ReservedCode2: '57009ed0-1939-41da-9b54-7d8f05855d73'
---

# 资源来源清单

本仓库的 `QuantumultX_Profiles.conf` 整合了以下来源（按段位分组）。

## ⚠️ 国内访问建议

GitHub raw 在国内经常断流（HTTP 000 / DNS 污染），推荐把以下 URL 中的：
```
https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>
```
替换为：
```
https://cdn.jsdelivr.net/gh/<owner>/<repo>@<branch>/<path>
```
**注意路径末尾无 `.git`、分支名前加 `@`**。

---

## 📚 [filter_remote]（20 条）

### hwind2021/QuantumultX-AdBlock-CN · main 分支 · 国内精准

| URL | 说明 |
|---|---|
| `quantumultx/filter/AdBlock-Lite.list` | 去广告（精简，约 22 万行） |
| `quantumultx/filter/AdBlock-AntiHijack.list` | 防运营商劫持 |
| `quantumultx/filter/AdBlock-Privacy.list` | 隐私追踪拦截 |
| `quantumultx/filter/BlockHttpDNS.list` | HTTP DNS 拦截 |
| `quantumultx/filter/Splash-Killer.list` | 开屏广告专项 |

### blackmatrix7/ios_rule_script · master 分支 · 海外兜底

| URL | 说明 |
|---|---|
| `rule/QuantumultX/Advertising/Advertising.list` | 去广告全量 |
| `rule/QuantumultX/Privacy/Privacy.list` | 隐私追踪 |
| `rule/QuantumultX/Hijacking/Hijacking.list` | 劫持拦截 |
| `rule/QuantumultX/Proxy/Proxy.list` | 代理域名 |
| `rule/QuantumultX/Direct/Direct.list` | 直连域名 |
| `rule/QuantumultX/Global/Global.list` | 国外通用 |
| `rule/QuantumultX/GlobalMedia/GlobalMedia.list` | 国外流媒体 |
| `rule/QuantumultX/PrivateTracker/PrivateTracker.list` | BT/PT |
| `rule/QuantumultX/China/China.list` | 国内通用 |
| `rule/QuantumultX/ChinaMedia/ChinaMedia.list` | 国内视频 |
| `rule/QuantumultX/ChinaASN/ChinaASN.list` | 国内 ASN |
| `rule/QuantumultX/ChinaIPs/ChinaIPs.list` | 国内 IP 池 |
| `rule/QuantumultX/Apple/Apple.list` | Apple 服务 |
| `rule/QuantumultX/Netflix/Netflix.list` | Netflix 锁定 |
| `rule/QuantumultX/YouTube/YouTube.list` | YouTube 锁定 |

## ✍️ [rewrite_remote]（8 条）

### App-Killers 合并包（本仓库本地化，8 个来源）

| 来源 | 说明 |
|---|---|
| `deezertidal/QuantumultX-Rewrite` startingad.conf | 200+ App 通用启动页去广告（墨鱼） |
| `fmz200/wool_scripts` CaiNiaoGuoGuo.snippet | 菜鸟裹裹深度去广告 |
| `fmz200/wool_scripts` Ximalaya.snippet | 喜马拉雅深度去广告 |
| `deezertidal/QuantumultX-Rewrite` xmlyad.conf | 喜马拉雅开屏广告域 reject |
| `fmz200/wool_scripts` BaiduNetdisk.snippet | 百度网盘去广告 |
| `fmz200/wool_scripts` 365Calendar.snippet | 365日历/万年历去广告 |
| `fmz200/wool_scripts` XianYu.snippet | 闲鱼去广告（2026-09 新增） |
| `fmz200/wool_scripts` Thunder.snippet | 迅雷去广告（2026-09 新增） |

内部脚本引用已本地化到本仓库 `scripts/`（含 goofish.js，原 ishowshu/qx）。

### hwind2021/QuantumultX-AdBlock-CN

| 文件 | 说明 |
|---|---|
| `AdBlock-All.conf` | 综合去广告重写（4 合 1） |
| `AdBlock-Feed.conf` | 信息流广告重写 |
| `AdBlock-Splash.conf` | 开屏 SDK 重写 |
| `AdBlock-Script.conf` | 脚本型去广告 |

### blackmatrix7/ios_rule_script

| 文件 | 说明 |
|---|---|
| `rewrite/QuantumultX/AllInOne/AllInOne.conf` | 神机复写综合 |
| `rewrite/QuantumultX/Advertising/Advertising.conf` | 复写去广告 |
| `rewrite/QuantumultX/Upgrade/Upgrade.conf` | HTTPS 升级 |

## 🔓 [mitm]

- 启用 hostname：`enable = true`
- 168 个广告 SDK 域名取自 `hwind2021/QuantumultX-AdBlock-CN/quantumultx/mitm/MITM.list`
- 用例：抖音/快手/淘宝/京东/B 站/QQ/百度等 App 的开屏广告拦截与信息流清理

## ⏰ [task_local]

- 每日 04:00 拉取 `splash-killer.js`、`feed-killer.js`（hwind2021）
- 其他 KOP-XIAO 模板自带的定时任务

> AI生成