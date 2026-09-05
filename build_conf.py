#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_conf.py
=============
把多个上游仓库的分流 + 重写 + 脚本整合到 QuantumultX_Profiles.conf。

设计目标
--------
1. 当前仓库: QuantumultX-Profile-CN, 自身就是"整合包"仓库
2. 本脚本就是 [filter_remote] / [rewrite_remote] / [mitm] / [task_local]
   四个段的真实"生成器"——版本控制里有显式版本、可复现。
3. 重新合成只需在本仓库根目录跑 `python build_conf.py`,
   不依赖任何外部 .conf 输入文件。

段位构造策略
------------
[general] [policy] [server] [server_remote] [dns] [filter_local] [rewrite_local] [server_local]
    → 全部按预设值直接构造 (git-tracked, 详见本文件 STABLE_* 字典)

[filter_remote]  (20 条)
    → hwind2021/QuantumultX-AdBlock-CN (国内精准, 5 条)
    → blackmatrix7/ios_rule_script (海外兜底, 15 条)

[rewrite_remote]  (7 条)
    → hwind2021/QuantumultX-AdBlock-CN (国内开屏/信息流/脚本去广告, 4 条)
    → blackmatrix7/ios_rule_script (综合重写 + HTTPS 升级, 3 条)

[mitm]            (168 域名)
    → enable=true, hostname 列表远程下载

[task_local]      (KOP-XIAO 模板基础 + hwind2021 拉新)

运行方式
--------
    python build_conf.py
    (会覆盖自身仓库的 QuantumultX_Profiles.conf)
"""

import datetime
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "QuantumultX_Profiles.conf"

# ---------- 本仓库自托管资源 ----------
SELF_OWNER = "hwind2021"
SELF_REPO = "QuantumultX-Profile-CN"
SELF_BASE_JD = f"https://cdn.jsdelivr.net/gh/{SELF_OWNER}/{SELF_REPO}@main"

# ============================================================
# 策略组图标: Qure 图标集 (https://github.com/Koolson/Qure, IconSet/ 目录)
# 已固化到本仓库 icons/ 目录自托管, 走 raw.githubusercontent.com 直链:
# 图标只在打开策略组面板时才异步加载, 此时 QX 必然已启动且挂有代理节点,
# GitHub 直链可正常访问, 无需经过 jsdelivr 中转。
# ============================================================
QURE_ICON = f"https://raw.githubusercontent.com/{SELF_OWNER}/{SELF_REPO}/main/icons"
ICON_DAILY = f"{QURE_ICON}/Daily.png"          # 每日任务/签到
ICON_ADBLACK = f"{QURE_ICON}/AdBlack.png"      # 去广告
ICON_ADVERTISING = f"{QURE_ICON}/Advertising.png"  # 广告拦截

# ===========================================================================
# 稳定参数 - 这些段在脚本里直接构造, 不依赖任何外部 .conf 文件
# ===========================================================================

GENERAL = """[general]
; ============================================================
; Quantumult X 主配置 v2 - 整合版通用参数
; ============================================================
server_check_url = http://cp.cloudflare.com/generate_204
server_check_timeout = 3000
resource_parser_url = https://cdn.jsdelivr.net/gh/KOP-XIAO/QuantumultX@master/Scripts/resource-parser.js
geo_location_checker = http://ip-api.com/json/?lang=zh-CN, https://cdn.jsdelivr.net/gh/KOP-XIAO/QuantumultX@master/Scripts/IP_API.js
; geoip_check_url = https://github.com/KOP-XIAO/QuantumultX/releases/download/resource/qqwry.dat

; ---- 以下均为 Quantumult X [general] 支持键 (对齐 KOP-XIAO 模板), 全部合法 ----
dns_exclusion_list = 1.0.0.1, 8.8.4.4, 8.8.8.8, 9.9.9.9, 149.112.112.112, 114.114.114.114, 114.114.115.115, 223.5.5.5, 223.6.6.6, 119.29.29.29, 119.28.28.28
udp_whitelist = 80, 443
fallback_udp_policy = direct
icmp_auto_reply = true
"""
# ============================================================
# 注意(给后续维护者): 不要往 [general] 里加 allow_when_vpn_disable /
#   allow_normal_when_vpn_disable / allow_wifi_access / allow_cellular_access /
#   tcp_force_through / udp_force_through / always_real_ip / bypass_* /
#   tcp_whitelist / wifi_white_list / cellular_white_list 等键 —— 这些是
#   Loon/Surge 风格, Quantumult X 不识别, 会报"配置文件语法错误"导入失败。
# ============================================================

POLICY_GROUPS = """[policy]
; ============================================================
; 策略组 - 2026 排布: 被引用的组先定义, 组组带 Koolson/Qure 图标
;
; ⚠️ 地区组必须用 server-tag-regex 正则匹配"订阅节点名"来定义
;    (机场节点名通常带 香港/HK/日本/JP 等关键词), 不能直接引用不存在的名字,
;    否则导入报"未知策略或节点"!
;
; ⚡ 极速测速 (url-latency-benchmark) - 定时自动测速选最快节点:
;   check-interval=600   每 600 秒(10 分钟)测速一次
;   alive-checking=true  即使策略空闲(无流量经过)也按间隔持续测速 ← 定时核心参数
;   tolerance=0          只要发现延迟更低的节点就立即切换(可调大如 100 防频繁切换)
;   依赖 [general] 的 server_check_url / server_check_timeout (已配置)
; ============================================================
static = 🇭🇰 香港节点, server-tag-regex=香港|🇭🇰|HK|Hong, img-url=%(ICON_HK)s
static = 🇯🇵 日本节点, server-tag-regex=日本|🇯🇵|JP|Japan, img-url=%(ICON_JP)s
static = 🇺🇸 美国节点, server-tag-regex=美国|🇺🇸|US|States, img-url=%(ICON_US)s
static = 🇸🇬 新加坡节点, server-tag-regex=新加坡|狮城|🇸🇬|SG|Singapore, img-url=%(ICON_SG)s
url-latency-benchmark = ⚡ 极速测速, server-tag-regex=^.*, check-interval=600, alive-checking=true, tolerance=0
static = 节点选择, ⚡ 极速测速, 🇭🇰 香港节点, 🇯🇵 日本节点, 🇺🇸 美国节点, 🇸🇬 新加坡节点, direct, reject, img-url=%(ICON_PROXY)s
static = 📺 Netflix, 节点选择, img-url=%(ICON_NETFLIX)s
static = 🎬 YouTube, 节点选择, img-url=%(ICON_YOUTUBE)s
; ---- 拦截类: 默认 reject, 误伤时可临时切 direct 排查 ----
static = Advertising, reject, direct, img-url=%(ICON_ADV)s
static = Privacy, reject, direct, img-url=%(ICON_PRIVACY)s
static = Hijacking, reject, direct, img-url=%(ICON_HIJACK)s
; ---- 国外类: 默认走节点选择 ----
static = Apple, direct, 节点选择, img-url=%(ICON_APPLE)s
static = Global, 节点选择, direct, img-url=%(ICON_GLOBAL)s
static = GlobalMedia, 节点选择, direct, img-url=%(ICON_GLOBALMEDIA)s
static = PrivateTracker, 节点选择, direct, img-url=%(ICON_PT)s
; ---- 国内类: 默认 direct ----
static = China, direct, 节点选择, img-url=%(ICON_CHINA)s
static = ChinaMedia, direct, 节点选择, img-url=%(ICON_CHINAMEDIA)s
static = ChinaASN, direct, 节点选择, img-url=%(ICON_CHINAASN)s
static = ChinaIPs, direct, 节点选择, img-url=%(ICON_CHINAIPS)s
static = 国内直连, direct, reject, img-url=%(ICON_DOMESTIC)s
""" % {
    "ICON_HK": f"{QURE_ICON}/HK.png",
    "ICON_JP": f"{QURE_ICON}/JP.png",
    "ICON_US": f"{QURE_ICON}/US.png",
    "ICON_SG": f"{QURE_ICON}/SG.png",
    "ICON_PROXY": f"{QURE_ICON}/Proxy.png",
    "ICON_NETFLIX": f"{QURE_ICON}/Netflix.png",
    "ICON_YOUTUBE": f"{QURE_ICON}/YouTube.png",
    "ICON_ADV": f"{QURE_ICON}/Advertising.png",
    "ICON_PRIVACY": f"{QURE_ICON}/AdBlack.png",
    "ICON_HIJACK": f"{QURE_ICON}/Hijacking.png",
    "ICON_APPLE": f"{QURE_ICON}/Apple.png",
    "ICON_GLOBAL": f"{QURE_ICON}/Global.png",
    "ICON_GLOBALMEDIA": f"{QURE_ICON}/GlobalMedia.png",
    "ICON_PT": f"{QURE_ICON}/Download.png",
    "ICON_CHINA": f"{QURE_ICON}/China.png",
    "ICON_CHINAMEDIA": f"{QURE_ICON}/DomesticMedia.png",
    "ICON_CHINAASN": f"{QURE_ICON}/China_Map.png",
    "ICON_CHINAIPS": f"{QURE_ICON}/Direct.png",
    "ICON_DOMESTIC": f"{QURE_ICON}/Domestic.png",
}

SERVER_REMOTE_PLACEHOLDER = """[server_remote]
; ⚠️⚠️⚠️ 必须填你自己的机场订阅链接 ⚠️⚠️⚠️
;
; 1. 登录你买的机场官网, 找到「我的订阅」/「订阅链接」
; 2. 复制形如 https://example.com/link/xxxxxx?clash=1 的链接
; 3. 替换下面示例的整段内容(注意保留最后的参数)
; 4. Quantumult X 主界面 → 底部「配置文件」→ 长按 → 更新配置
;
; 国内访问 (raw.githubusercontent.com 经常断流), 把 URL 替换成 jsdelivr CDN:
;   https://你的机场域名/link/...  →  https://cdn.jsdelivr.net/gh/<owner>/<repo>@<branch>/<path>
; ⚠️ 机场订阅一般不走 jsdelivr (机场通常 API/订阅链接直接给的就是机场自己的 CDN)
;     所以机场订阅保持原 URL 即可。
;
; ============= 把下面这一行换成你自己的机场订阅 =============
; https://你的机场域名/link/你的token, tag=📡 我的机场节点, update-interval=86400, opt-parser=true, enabled=true
"""

FILTER_LOCAL = """[filter_local]
; ==== 误伤修复白名单(本地规则优先于远程规则, 先于一切 REJECT 匹配) ====
; 迅雷: blackmatrix7 Advertising.list 误杀登录接口 api-u-ssl/api-shoulei-ssl
;       .xunlei.com → 登录一直失败, 整域直连修复
host-suffix, xunlei.com, direct
host-suffix, sandai.net, direct
; QQ同步助手: blackmatrix7 Privacy.list 误杀 id6.me(腾讯统一账号验证服务),
;   且同步 API 出境(走代理)时腾讯服务端判定境外 IP → 「该国家地区未开通服务」
host-suffix, id6.me, direct
host-suffix, sync.qq.com, direct
host-suffix, local, direct
host-suffix, lan, direct
# 兜底规则: 此为必需规则, 不在上述所有规则(远程+本地)中的剩余请求走这条
# 仅可修改对应策略组, 请勿删除 final
final, 节点选择
"""

REWRITE_LOCAL = """[rewrite_local]
; 本地重写（按需启用）
"""

DNS = """[dns]
; Quantumult X [dns] 使用可重复的 server= 声明上游 DNS（仅 IP，不能用 system 关键字）
server = 114.114.114.114
server = 223.5.5.5
server = 119.29.29.29
server = 119.28.28.28
server = 1.1.1.1
server = 8.8.8.8
"""

SERVER_LOCAL = """[server_local]
; 在这里填手动配置的本地节点（一般用不到）
"""

TASK_LOCAL_BASE = """[task_local]
; ============================================================
; KOP-XIAO 模板自带的常用签到脚本 (图标: Koolson/Qure)
; ============================================================
0 9 * * * https://raw.githubusercontent.com/chavyleung/scripts/master/chavyoleckey/quantumultx/chavyoleckey.qx.js, tag=ℹ️ 获取 Cookie, img-url=%(ICON_DAILY)s, enabled=false
""" % {"ICON_DAILY": ICON_DAILY}

# ===========================================================================
# 动态内容 - 来自上游仓库的规则
# ===========================================================================

HW_OWNER = "hwind2021"
HW_REPO = "QuantumultX-AdBlock-CN"
HW_BRANCH = "main"
HW_BASE_RAW = f"https://raw.githubusercontent.com/{HW_OWNER}/{HW_REPO}/{HW_BRANCH}"
HW_BASE_JD = f"https://cdn.jsdelivr.net/gh/{HW_OWNER}/{HW_REPO}@{HW_BRANCH}"

BM_OWNER = "blackmatrix7"
BM_REPO = "ios_rule_script"
BM_BRANCH = "master"
BM_BASE_JD = f"https://cdn.jsdelivr.net/gh/{BM_OWNER}/{BM_REPO}@{BM_BRANCH}"


def dual_url(path: str, owner: str, repo: str, branch: str) -> tuple[str, str]:
    raw = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
    jd = f"https://cdn.jsdelivr.net/gh/{owner}/{repo}@{branch}/{path}"
    return raw, jd


def fetch_text(url: str, timeout: int = 30) -> str | None:
    """简单 GET, 失败返回 None"""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "build-conf/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  ! WARN: GET {url} 失败: {e}")
        return None


# ---------- [filter_remote] ----------
def fmt_filter_hw(path: str, tag: str, fp: str | None = None) -> str:
    raw, _jd = dual_url(path, HW_OWNER, HW_REPO, HW_BRANCH)
    en = "true"
    fp_part = f", force-policy={fp}" if fp else ""
    return f"{raw}, tag={tag}, update-interval=86400, opt-parser=true, enabled={en}{fp_part}"


def fmt_filter_bm(path: str, tag: str, fp: str | None = None) -> str:
    url = f"{BM_BASE_JD}/{path}"
    en = "true"
    fp_part = f", force-policy={fp}" if fp else ""
    return f"{url}, tag={tag}, update-interval=86400, opt-parser=true, enabled={en}{fp_part}"


HW_FILTER_PATHS = [
    ("quantumultx/filter/AdBlock-Lite.list", "🚫 去广告(精简)", None),
    ("quantumultx/filter/Splash-Killer.list", "⛔ 开屏广告专项", None),
    ("quantumultx/filter/BlockHttpDNS.list", "🛡️ HTTPDNS 拦截", None),
    ("quantumultx/filter/AdBlock-Privacy.list", "🕵️ 隐私追踪拦截", None),
    ("quantumultx/filter/AdBlock-AntiHijack.list", "🚨 防运营商劫持", None),
]

BM_FILTER_PATHS = [
    # —— 排布原则 (QX 规则自上而下首条命中即生效): 专项/精确在前, 宽泛/兜底在后 ——
    # 1) 拦截类(REJECT)最优先, 防止被后面的宽泛规则截胡漏杀
    # 2) force-policy 专项组(Netflix/YouTube)必须排在 GlobalMedia 之前,
    #    否则泛流媒体规则先命中导致 force-policy 失效
    # 3) Apple/Direct 等直连专项排在 Global 之前, 保证苹果等域名可直连
    # 4) IP 级宽泛规则(ChinaASN/ChinaIPs)放最后兜底
    #
    # ⚠️ 每条都必须带 force-policy! 不带 force-policy 的规则会让 QX 启动时
    #    "自动补齐"同名策略组(成员仅 direct/proxy/reject, 无图标、默认不合理)。
    #    引用的组要么是 [policy] 已定义组, 要么是 direct/reject 内置策略。
    ("rule/QuantumultX/Advertising/Advertising.list", "⛔ 去广告(全量)", "Advertising"),
    ("rule/QuantumultX/Privacy/Privacy.list", "🛡️ 隐私追踪拦截", "Privacy"),
    ("rule/QuantumultX/Hijacking/Hijacking.list", "🚫 运营商劫持", "Hijacking"),
    ("rule/QuantumultX/Proxy/Proxy.list", "🌐 代理域名", "节点选择"),
    ("rule/QuantumultX/Netflix/Netflix.list", "📺 Netflix", "📺 Netflix"),
    ("rule/QuantumultX/YouTube/YouTube.list", "🎬 YouTube", "🎬 YouTube"),
    ("rule/QuantumultX/GlobalMedia/GlobalMedia.list", "🎬 国外流媒体", "GlobalMedia"),
    ("rule/QuantumultX/Apple/Apple.list", "🍎 Apple 服务", "Apple"),
    ("rule/QuantumultX/Direct/Direct.list", "🎯 直连域名", "direct"),
    ("rule/QuantumultX/PrivateTracker/PrivateTracker.list", "🔒 BT/PT 资源", "PrivateTracker"),
    ("rule/QuantumultX/Global/Global.list", "🌍 国外网站", "Global"),
    ("rule/QuantumultX/China/China.list", "🐼 国内网站", "China"),
    ("rule/QuantumultX/ChinaMedia/ChinaMedia.list", "📺 国内视频", "ChinaMedia"),
    ("rule/QuantumultX/ChinaASN/ChinaASN.list", "🇨🇳 国内 ASN IP", "ChinaASN"),
    ("rule/QuantumultX/ChinaIPs/ChinaIPs.list", "🇨🇳 国内 IP 池", "ChinaIPs"),
]


def build_filter_remote() -> str:
    lines = [
        "[filter_remote]",
        "; === hwind2021/QuantumultX-AdBlock-CN 国内化分流规则 (主用 5 条) ===",
        f"; 仓库: https://github.com/{HW_OWNER}/{HW_REPO}",
        "; ⚠️ 国内访问 raw.githubusercontent.com 经常断流, 替换 CDN 镜像方法:",
        ";   把 https://raw.githubusercontent.com/hwind2021/... 整段替换为",
        ";   https://cdn.jsdelivr.net/gh/hwind2021/...@main/ (路径其余部分不变)",
        "; ⚠️ Lite 与 Full 二选一, 此处默认启用 Lite (696 KB)",
        "",
    ]
    for path, tag, fp in HW_FILTER_PATHS:
        lines.append(fmt_filter_hw(path, tag, fp))
    lines.extend([
        "",
        "; === 广告 SDK 兜底拦截 (自建, 穿山甲/优量汇/快手联盟等备用域名) ===",
        "; 主域名被拦后 SDK 会切备用域名重新拉广告并缓存, 杀掉重启后直接展示缓存素材",
        "; (不走网络, 规则拦不到) —— 此列表堵死备用域名, 让 SDK 永远拉不到新广告",
        f"{SELF_BASE_JD}/filter/AdSDK-Fallback.list, tag=🧱 广告SDK兜底, update-interval=86400, opt-parser=false, enabled=true, force-policy=Advertising",
        "",
        "; === 以下 blackmatrix7/ios_rule_script 作为综合分流补充 ===",
        "; 优先级低于 hwind2021, 命中 hwind2021 的规则就会短路返回",
        "; 备注: blackmatrix7 与 hwind2021 部分规则重合, 但 blackmatrix7",
        ";       更全 (覆盖 IP-CIDR / ChinaASN 等), hwind2021 更精准 (针对国内开屏 SDK)",
        "",
    ])
    for path, tag, fp in BM_FILTER_PATHS:
        lines.append(fmt_filter_bm(path, tag, fp))
    return "\n".join(lines)


# ---------- [rewrite_remote] ----------
HW_REWRITE_PATHS = [
    ("quantumultx/rewrite/AdBlock-Splash.conf", "⛔ 开屏广告重写"),
    ("quantumultx/rewrite/AdBlock-Feed.conf", "📰 信息流广告重写"),
    ("quantumultx/rewrite/AdBlock-Script.conf", "📜 脚本型去广告"),
    ("quantumultx/rewrite/AdBlock-All.conf", "🔧 全部重写(综合)"),
]

BM_REWRITE_PATHS = [
    ("rewrite/QuantumultX/AllInOne/AllInOne.conf", "🔧 神机复写(综合)"),
    ("rewrite/QuantumultX/Advertising/Advertising.conf", "⛔ 神机复写(去广告)"),
    ("rewrite/QuantumultX/Upgrade/Upgrade.conf", "⬆️ HTTPS 升级"),
]

# ---------- 子资源本地化 ----------
# 重写 conf 内部引用的 .js 子资源 (raw/gist 国内断流, DivineEngine 已 404),
# 已固化到本仓库 scripts/ 目录, 引用统一走本仓库 jsdelivr, 消除"问题存在于子资源"。
# (SELF_OWNER/SELF_REPO/SELF_BASE_JD 已在文件头部定义)

SCRIPT_URL_MAP = {
    # 上游(死链/断流) → 本仓库 scripts/ 文件名
    "https://gist.githubusercontent.com/blackmatrix7/f5f780d0f56b319b6ad9848fd080bb18/raw/zheye.min.js": "zheye.min.js",
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/script/smzdm/smzdm_remove_ads.js": "smzdm_remove_ads.js",
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/script/startup/startup.js": "startup.js",
    "https://raw.githubusercontent.com/DivineEngine/Profiles/master/Surge/Rewrite/bstar.js": "bstar.js",
    # ---- App-Killers(启动页去广告合集)引用的脚本 ----
    "https://github.com/ddgksf2013/Scripts/raw/master/12306.js": "12306.js",
    "https://github.com/ddgksf2013/Scripts/raw/master/caixinads.js": "caixinads.js",
    "https://github.com/ddgksf2013/Scripts/raw/master/coolapk.js": "coolapk.js",
    "https://github.com/ddgksf2013/Scripts/raw/master/fly.js": "fly.js",
    "https://github.com/ddgksf2013/Scripts/raw/master/jd_json.js": "jd_json.js",
    "https://github.com/ddgksf2013/Scripts/raw/master/shunfeng_json.js": "shunfeng_json.js",
    # 注意: ddgksf 的 startup.js 与 bm7 的同名但内容不同, 单独命名
    "https://github.com/ddgksf2013/Scripts/raw/master/startup.js": "ddgksf-startup.js",
    "https://github.com/ddgksf2013/Scripts/raw/master/stay.js": "stay.js",
    "https://github.com/ddgksf2013/Scripts/raw/master/xiaohongshu.js": "xiaohongshu.js",
    "https://raw.githubusercontent.com/NobyDa/Script/master/Bahamut/BahamutAnimeAds.js": "BahamutAnimeAds.js",
    "https://raw.githubusercontent.com/deezertidal/private/master/js-backup/Script/xmly_json.js": "xmly_json.js",
    "https://raw.githubusercontent.com/zZPiglet/Task/master/asset/UnblockURLinWeChat.js": "UnblockURLinWeChat.js",
    "https://raw.githubusercontent.com/fmz200/wool_scripts/main/Scripts/cainiao/cainiao.js": "cainiao.js",
}

# 需要本地化的重写 conf: (上游 jsdelivr URL, 输出到本仓库 rewrite-local/ 的文件名)
LOCALIZED_REWRITE_SOURCES = [
    (f"{HW_BASE_JD}/quantumultx/rewrite/AdBlock-Script.conf", "AdBlock-Script.conf"),
    (f"{HW_BASE_JD}/quantumultx/rewrite/AdBlock-All.conf", "AdBlock-All.conf"),
    (f"{BM_BASE_JD}/rewrite/QuantumultX/AllInOne/AllInOne.conf", "AllInOne.conf"),
]


def build_localized_rewrites() -> list[str]:
    """拉上游重写 conf → 替换断流子资源 URL → 写入本仓库 rewrite-local/。"""
    outdir = ROOT / "rewrite-local"
    outdir.mkdir(exist_ok=True)
    written = []
    for url, name in LOCALIZED_REWRITE_SOURCES:
        text = fetch_text(url)
        if text is None:
            print(f"  - ⚠️ 上游重写拉取失败, 保留已有本地版: {name}")
            continue
        for old, fname in SCRIPT_URL_MAP.items():
            text = text.replace(old, f"{SELF_BASE_JD}/scripts/{fname}")
        (outdir / name).write_text(text, encoding="utf-8")
        written.append(name)
        print(f"  - 本地化重写已更新: rewrite-local/{name}")
    return written


# ---------- App-Killers: 启动页/App 专属去广告合并包 ----------
# 来源(均为活跃维护仓库, 拉取时有快照缓存到 sources/ 供离线兜底):
#   dee-startingad  : deezertidal/QuantumultX-Rewrite 通用启动页去广告(墨鱼维护, 200+ App,
#                     含菜鸟/百度网盘/12306/京东/小红书等开屏拦截)
#   fmz-cainiao     : fmz200/wool_scripts 菜鸟裹裹深度去广告(首页推广/角标/券)
#   fmz-ximalaya    : fmz200/wool_scripts 喜马拉雅深度去广告(搜索广告/弹窗/直播角标)
#   dee-xmlyad      : deezertidal 喜马拉雅开屏广告拦截(adse/adbehavior 域名 reject)
#   fmz-baidunetdisk: fmz200/wool_scripts 百度网盘去广告(活动弹窗/福利页/广告 CDN)
#   fmz-365calendar : fmz200/wool_scripts 365日历/万年历去广告
APP_KILLER_SOURCES = [
    ("https://cdn.jsdelivr.net/gh/deezertidal/QuantumultX-Rewrite@master/rewrite/startingad.conf", "dee-startingad"),
    ("https://cdn.jsdelivr.net/gh/fmz200/wool_scripts@main/QuantumultX/rewrite/split/partC/CaiNiaoGuoGuo.snippet", "fmz-cainiao"),
    ("https://cdn.jsdelivr.net/gh/fmz200/wool_scripts@main/QuantumultX/rewrite/split/partX/Ximalaya.snippet", "fmz-ximalaya"),
    ("https://cdn.jsdelivr.net/gh/deezertidal/QuantumultX-Rewrite@master/rewrite/xmlyad.conf", "dee-xmlyad"),
    ("https://cdn.jsdelivr.net/gh/fmz200/wool_scripts@main/QuantumultX/rewrite/split/partB/BaiduNetdisk.snippet", "fmz-baidunetdisk"),
    ("https://cdn.jsdelivr.net/gh/fmz200/wool_scripts@main/QuantumultX/rewrite/split/part3/365Calendar.snippet", "fmz-365calendar"),
]

# dee-xmlyad 的通配 hostname (*.xima*.* / *.xmcdn.*) 规范化为 QX 常规写法
APP_KILLER_HOST_EXTRA = ["*.ximalaya.com", "*.xmcdn.com"]


def build_app_killers() -> str | None:
    """合并多个上游去广告 snippet → rewrite-local/App-Killers.conf (js 全部本地化)。"""
    outdir = ROOT / "rewrite-local"
    outdir.mkdir(exist_ok=True)
    srcdir = ROOT / "sources"
    srcdir.mkdir(exist_ok=True)

    hosts: list[str] = []
    sections: list[tuple[str, list[str]]] = []
    for url, label in APP_KILLER_SOURCES:
        text = fetch_text(url)
        if text is None:
            cache = srcdir / f"{label}.conf"
            if cache.exists():
                text = cache.read_text(encoding="utf-8")
                print(f"  - ⚠️ 上游拉取失败, 使用本地快照: {label}")
            else:
                print(f"  - ⚠️ 跳过(拉取失败且无快照): {label}")
                continue
        (srcdir / f"{label}.conf").write_text(text, encoding="utf-8")
        # 先把全部断流 js 引用替换为本仓库 scripts/ 路径
        for old, fname in SCRIPT_URL_MAP.items():
            text = text.replace(old, f"{SELF_BASE_JD}/scripts/{fname}")
        body: list[str] = []
        for raw in text.splitlines():
            line = raw.strip()
            if not line or line.startswith("#!"):
                continue
            low = line.lower()
            if low.startswith("hostname"):
                # snippet 末尾的 hostname 行: 收集合并, 不原样保留
                val = line.split("=", 1)[1] if "=" in line else ""
                if label != "dee-xmlyad":  # xmly 的通配符用规范化覆盖
                    for h in val.replace(" ", ",").split(","):
                        h = h.strip()
                        if h and "example" not in h:
                            hosts.append(h)
                continue
            if "this-is-an-example" in line:
                continue  # fmz 365Calendar 里的占位行
            body.append(line)
        sections.append((label, body))
    hosts.extend(APP_KILLER_HOST_EXTRA)

    if not sections:
        print("  - ⚠️ App-Killers 无可用来源, 保留已有文件")
        return None

    # hostname 去重保序
    seen: set[str] = set()
    uniq: list[str] = []
    for h in hosts:
        if h.lower() not in seen:
            seen.add(h.lower())
            uniq.append(h)

    header = "\n".join([
        "; ============================================================",
        "; App-Killers 启动页 + App 专属去广告合并包 (本地化版)",
        f"; 由 build_conf.py 自动生成, 来源: {', '.join(l for l, _ in sections)}",
        f"; 生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "; 内部引用的全部 .js 已固化到本仓库 scripts/ (jsdelivr 分发), 无断流子资源",
        "; 覆盖: 菜鸟裹裹 / 喜马拉雅 / 百度网盘 / 365日历(万年历) 等 200+ App 启动页",
        "; ⚠️ 部分规则生效需清除对应 App 缓存或重装后首次启动拦截",
        "; ============================================================",
        "",
    ])
    body = ""
    for label, lines in sections:
        body += f"; ---- {label} ----\n" + "\n".join(lines) + "\n\n"
    mitm_line = "hostname = " + ", ".join(uniq)
    out = header + body + mitm_line + "\n"
    (outdir / "App-Killers.conf").write_text(out, encoding="utf-8")
    print(f"  - App-Killers.conf 已生成: {len(sections)} 个来源, {len(uniq)} 个 MITM host")
    return "App-Killers.conf"


def fmt_rewrite_hw(path: str, tag: str) -> str:
    raw, _jd = dual_url(path, HW_OWNER, HW_REPO, HW_BRANCH)
    return f"{raw}, tag={tag}, update-interval=86400, opt-parser=false, enabled=true"


def fmt_rewrite_bm(path: str, tag: str) -> str:
    url = f"{BM_BASE_JD}/{path}"
    return f"{url}, tag={tag}, update-interval=86400, opt-parser=false, enabled=true"


def build_rewrite_remote() -> str:
    lines = [
        "[rewrite_remote]",
        "; === App-Killers 启动页+App 专属去广告 (本仓库本地化合并包) ===",
        "; 菜鸟裹裹 / 喜马拉雅 / 百度网盘 / 365日历(万年历) 等开屏与内置广告,",
        "; 合并自 deezertidal(墨鱼) 与 fmz200 两个活跃规则库, 内部 .js 全部本地化",
        "",
        f"{SELF_BASE_JD}/rewrite-local/App-Killers.conf, tag=🚀 启动页去广告(菜鸟/喜马/网盘/万年历), update-interval=86400, opt-parser=false, enabled=true",
        "",
        "; === hwind2021/QuantumultX-AdBlock-CN 国内化重写规则 ===",
        f"; 仓库: https://github.com/{HW_OWNER}/{HW_REPO}",
        "; Splash: 针对国内 App 开屏广告 SDK 重写 (pangolin / snssdk / gdt)",
        "; Feed:   针对信息流广告接口重写",
        "; Script: 针对脚本型广告位重写",
        "; All:    Splash + Feed + Script 合并版, 与前三选其一",
        ";",
        "; ⚠️ Script / All / AllInOne 三条引用的是本仓库 rewrite-local/ 本地化版:",
        ";    上游 conf 内部的 .js 子资源全是 raw/gist 链接(国内断流, bstar.js 所在的",
        ";    DivineEngine 仓库已 404), 已将脚本固化到本仓库 scripts/ 并替换为 jsdelivr,",
        ";    否则 QX 报「N 个问题存在于子资源」。",
        "",
    ]
    for path, tag in HW_REWRITE_PATHS:
        # Script / All 用本地化版 (子资源已替换)
        fname = path.rsplit("/", 1)[-1]
        if fname in ("AdBlock-Script.conf", "AdBlock-All.conf"):
            lines.append(
                f"{SELF_BASE_JD}/rewrite-local/{fname}, tag={tag}, update-interval=86400, opt-parser=false, enabled=true"
            )
        else:
            lines.append(fmt_rewrite_hw(path, tag))
    lines.extend([
        "",
        "; === blackmatrix7 综合重写 (补充) ===",
        "",
    ])
    for path, tag in BM_REWRITE_PATHS:
        fname = path.rsplit("/", 1)[-1]
        if fname == "AllInOne.conf":
            lines.append(
                f"{SELF_BASE_JD}/rewrite-local/{fname}, tag={tag}, update-interval=86400, opt-parser=false, enabled=true"
            )
        else:
            lines.append(fmt_rewrite_bm(path, tag))
    return "\n".join(lines)


# ---------- [mitm] ----------
MITM_URL = f"{HW_BASE_JD}/quantumultx/mitm/MITM.list"


def load_mitm_hostnames() -> list[str]:
    print("  - 拉取 MITM.list ...")
    txt = fetch_text(MITM_URL)
    if txt is None:
        # fallback 用本仓库内置的 cached 列表
        cache = ROOT / "docs" / "_mitm_fallback.txt"
        if cache.exists():
            print(f"  - 使用本地缓存: {cache}")
            txt = cache.read_text(encoding="utf-8")
        else:
            print("  - ⚠️ MITM.list 拉取失败, [mitm] 段将为空")
            return []
    hosts = []
    for line in txt.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        hosts.append(s)
    seen = set()
    uniq = []
    for h in hosts:
        if h not in seen:
            seen.add(h)
            uniq.append(h)
    return uniq


def build_mitm(hosts: list[str]) -> str:
    if not hosts:
        return "[mitm]\nhostname ="
    # Quantumult X .conf 不支持反斜杠续行, hostname 必须放同一行
    return "[mitm]\nhostname = " + ", ".join(hosts)


# ---------- [task_local] ----------
def build_task_local() -> str:
    lines = [
        TASK_LOCAL_BASE.rstrip(),
        "",
        "; ============================================================",
        f"; 每日自动更新 hwind2021/{HW_REPO} 的脚本",
        "; ============================================================",
        f"0 4 * * * {HW_BASE_RAW}/quantumultx/script/splash-killer.js, tag=🔄 更新·开屏去广告脚本, img-url={ICON_ADBLACK}, enabled=true",
        f"0 4 * * * {HW_BASE_RAW}/quantumultx/script/feed-killer.js, tag=🔄 更新·信息流去广告脚本, img-url={ICON_ADVERTISING}, enabled=true",
        "",
    ]
    return "\n".join(lines)


# ===========================================================================
# 主流程
# ===========================================================================
def main() -> int:
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"[1/5] 拉 MITM.list ...")
    hosts = load_mitm_hostnames()

    print(f"[2/5] 构造 [filter_remote] ({len(HW_FILTER_PATHS) + len(BM_FILTER_PATHS)} 条) ...")
    sec_filter = build_filter_remote()

    print(f"[3/5] 构造 [rewrite_remote] ({len(HW_REWRITE_PATHS) + len(BM_REWRITE_PATHS)} 条) ...")
    build_localized_rewrites()  # 先本地化含断流子资源的重写 conf
    build_app_killers()  # 生成启动页/App 专属去广告合并包
    sec_rewrite = build_rewrite_remote()

    print(f"[4/5] 构造 [task_local] ...")
    sec_task = build_task_local()

    print(f"[5/5] 拼接 + 写出 ...")

    header = f"""; ============================================================
; Quantumult X 主界面配置 .conf  (整合 v2)
; 生成时间: {ts}
; 整合源:
;   1. KOP-XIAO/QuantumultX (主模板段位参考)
;        https://github.com/KOP-XIAO/QuantumultX
;   2. hwind2021/QuantumultX-AdBlock-CN (国内化分流 + 重写 + MITM, 用户自营仓库)
;        https://github.com/{HW_OWNER}/{HW_REPO}
;   3. blackmatrix7/ios_rule_script (综合分流 + 重写补充)
;        https://github.com/{BM_OWNER}/{BM_REPO}
;
; 集成要点:
;   1. [filter_remote]  hwind2021 5 条 + blackmatrix7 15 条
;   2. [rewrite_remote] hwind2021 4 条 + blackmatrix7 3 条
;   3. [mitm] 168 个广告 SDK hostname
;   4. [task_local] 每日 04:00 重新拉取 hwind2021 的 .js
;   5. [general] [policy] [dns] 等段位按通用稳定值固化
;
; ⚠️ 使用前必读:
;   - 必须先把 [server_remote] 填入你的机场订阅
;   - 国内访问 raw.githubusercontent.com 经常断流,
;     每条规则上面都有注释告诉怎么切 jsdelivr 镜像
;   - 首次配置后等节点列表拉取完成即可使用
; ============================================================

"""

    sections = [
        header,
        GENERAL, "",
        sec_filter, "",
        sec_rewrite, "",
        POLICY_GROUPS, "",
        SERVER_REMOTE_PLACEHOLDER, "",
        FILTER_LOCAL, "",
        REWRITE_LOCAL, "",
        DNS, "",
        SERVER_LOCAL, "",
        sec_task, "",
        build_mitm(hosts), "",
    ]
    final = "\n".join(sections)

    must_have = [
        "[general]", "[server_remote]", "[policy]",
        "[filter_remote]", "[rewrite_remote]", "[mitm]",
        "[task_local]", "[filter_local]", "[rewrite_local]",
        "[dns]", "[server_local]",
    ]
    missing = [s for s in must_have if s not in final]
    if missing:
        print(f"❌ 缺失段位: {missing}", file=sys.stderr)
        return 1

    # 计算 .conf 中 .list 数量
    n_list = len(re.findall(r"^\S*\.list", final, re.MULTILINE))
    n_conf = len(re.findall(r"^\S*\.conf", final, re.MULTILINE))
    n_task = len(re.findall(r"^\d+\s+\d+\s+\*\s+\*\s+\*", final, re.MULTILINE))

    OUT.write_text(final, encoding="utf-8")
    size = OUT.stat().st_size
    print(f"\n✅ 已生成: {OUT}")
    print(f"   大小: {size:,} bytes")
    print(f"   filter_remote 总条目: {n_list}")
    print(f"   rewrite_remote 总条目: {n_conf}")
    print(f"   task_local 总条目: {n_task}")
    print(f"   mitm hostname: {len(hosts)} 条")
    print(f"   段位完整性: {len(must_have)}/{len(must_have)} ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
