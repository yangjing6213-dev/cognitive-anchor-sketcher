# Cognitive Anchor Sketcher

> 把文章里的一个关键认知，画成一张白底、手绘、能让人记住的正文配图。

[English README](README.en.md)

## 一、这个仓库是什么？

这是一个可以安装到 Codex 的 Skill，专门给中文文章、帖子、博客、Notion 文档、工作流文档和方法论做正文配图。

它的工作方式很简单，但不敷衍：先读懂文章，再捞出一个“认知锚点”——一个判断、一个动作、一个转折或一个隐喻——最后把它画成一张 16:9 横版手绘解释图。每张图只讲一件事，避免正文最后长成一面项目管理看板。

默认视觉 IP 是“小黑”：黑色实心、白点眼、细腿、空表情。小黑不是站在角落里负责卖萌的吉祥物，而是会认真参与系统运转的荒诞工作者。

## 二、适合谁用？

### 1、特别适合

- 写公众号、博客、知识库、Notion 或产品方法论，希望图和文字说的是同一件事的人。
- 想把抽象判断画得更具体，又不想把文章改造成 PPT 的内容创作者、产品设计师和 AI Builder。
- 需要统一画风和角色资产，同时希望每次生图前都先确认方向、画风、IP 和构图的人。
- 想使用小黑、拓拓、星比，或在获得授权后建立项目级自定义 IP 的团队和个人。

### 2、不适合

- 需要 PPTX、PDF、SVG、品牌 KV、商业海报或复杂架构图的项目。
- 想一次丢进几十张图、靠 API 静默批量出图的流水线。本 Skill 的生图入口是已登录 ChatGPT 的 Codex CLI 内置图片工具，不是 API-key 生成器。
- 没有参考图、来源或使用授权，却希望直接复制某个自定义 IP 的需求。

## 三、它会产出什么？

- 一份认知锚点分析：文章的核心判断、转折和适合视觉化的段落。
- 一份 shot list：每张图放在哪一段、表达什么、角色做什么、用什么构图和短批注。
- 按确认结果生成的单张 PNG 正文配图，默认 16:9、纯白背景、黑色手绘线稿，并保留少量有用的彩色提示。
- 两种可选画风：`minimal-line`（默认极简线稿）和 `emotion-doodle`（黑色主导的情绪涂鸦）。
- 多种 IP 组合：小黑、拓拓、星比、拓拓与星比，以及经过授权的项目级自定义 IP。

默认一篇文章规划 4–8 张图；内容短就少画几张，够用比热闹重要。

## 四、具有什么价值？

- **让抽象话变成动作。** 读者不用先读三遍方法论，先看见“到底发生了什么”。
- **让图文站在同一边。** 每张图只服务一个认知锚点，不拿装饰性插画抢正文的戏。
- **让风格可持续。** 画风与 IP 分开选择，小黑的既有形象保持不变，拓拓和星比也有各自的职责。
- **让生成过程可控。** QA 对话会逐项确认文章方向、画风、IP、授权、shot list、输出规格和生成模式，减少“图挺好看，但完全没说到点上”的情况。
- **让自定义 IP 有边界。** 参考图、草稿、授权范围和保存范围分开确认，避免把“我传了一张图”误当成“可以随便复制”。

## 五、示例效果

下面四张图是本项目的真实示例素材，均为 2048×1152（16:9）PNG。它们展示了从文章输入、认知锚点，到 QA 确认和风格/IP 选择的关键动作。示例图由项目作者提供并授权放入本仓库，画面中没有二维码、联系方式或本地路径。

### 01｜从文章里捞出一个认知锚点

![文章输入与认知锚点](docs/examples/01-article-input-anchor.png)

### 02｜把抽象判断变成一个可见动作

![认知锚点到动作](docs/examples/02-anchor-to-action.png)

### 03｜生成前先过 QA 闸门

![生成前 QA 闸门](docs/examples/03-qa-gate.png)

### 04｜画风与 IP 可以分别确认、自由组合

![画风与 IP 选择](docs/examples/04-style-ip-authorization.png)

## 六、安装方法

这是一个 Skill，不是需要编译的独立应用。安装时只需把 `cognitive-anchor-sketcher/` 子目录复制到 Codex 的 skills 目录。

### macOS / Linux

```bash
git clone https://github.com/yangjing6213-dev/cognitive-anchor-sketcher.git
cd cognitive-anchor-sketcher
mkdir -p "$HOME/.codex/skills"
cp -R ./cognitive-anchor-sketcher "$HOME/.codex/skills/"
```

### Windows PowerShell

```powershell
git clone https://github.com/yangjing6213-dev/cognitive-anchor-sketcher.git
Set-Location .\cognitive-anchor-sketcher
$skillsDir = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $HOME '.codex\skills' }
New-Item -ItemType Directory -Force -Path $skillsDir | Out-Null
Copy-Item -Recurse -Force .\cognitive-anchor-sketcher (Join-Path $skillsDir 'cognitive-anchor-sketcher')
```

重新打开 Codex 或刷新 Skill 列表后即可使用。运行 Skill 本身不需要额外的 Python、Node.js 或图片 API 依赖；仓库的自动合约测试使用 Python 3 标准库，真正生图时需要当前会话可用的 Codex CLI 内置图片工具和有效的 ChatGPT 登录状态。

仓库自带两道自动检查：`validate-skill.yml` 会运行 Python 标准库合约测试并校验 Skill 引用；`codeql.yml` 会扫描 GitHub Actions 工作流。它们在提交或 Pull Request 时自动运行，不需要额外配置密钥。

## 七、如何使用

### 只做分析和配图规划

```text
Use $cognitive-anchor-sketcher
先不要生图。请分析这篇中文文章的认知锚点，给我一份 5 张左右的 shot list。
每张图写清楚段落位置、核心意思、结构类型、IP 动作和中文批注建议。
```

### 按确认式 QA 生成配图

```text
Use $cognitive-anchor-sketcher
请为下面的中文文章生成正文配图，先按 QA 流程逐项确认文章方向、画风、IP、shot list 和输出规格，再开始生成。
```

每个确认问题只推进一个阶段，并提供 3–5 个选项。你可以直接回复选项编号，也可以用能明确对应某个选项的自然语言回答。

### 选择画风和 IP

```text
画风：emotion-doodle
IP：拓拓与星比
要求：16:9、纯白背景、黑色主导手绘线稿、少量彩色中文批注。
```

画风和 IP 是两个独立维度：画风决定线条、留白和颜色处理；IP 决定角色长什么样、负责什么动作。选了情绪涂鸦，不会把小黑偷偷换成别的角色。

### 使用自定义 IP

```text
使用我的自定义 IP。请先检查我是否上传参考图；如果没有，先提醒我上传。
如果已有参考图，先输出仅供确认的草稿，再确认使用范围、保存范围和必要授权，不要直接生成。
```

没有参考图、草稿未确认或授权范围不清时，流程会停在门禁处，不会默默猜一个“差不多的 IP”。

## 八、项目工作流程

```text
文章输入
  → 方向确认
  → 画风确认
  → IP / 授权确认
  → 认知锚点与 shot list
  → 输出规格与生成模式
  → 最终确认
  → 单张生成
  → 内部视觉 QA
  → 用户验收与保存
```

1. 读取文章或用户提供的材料，找出认知转折，而不是给每段文字平均撒芝麻。
2. 依次确认文章转化方向、画风、IP、授权范围、shot list、图片数量和输出规格。
3. 每张图只设计一个核心判断、流程、结构、状态或隐喻；所选角色必须参与核心动作。
4. 通过确认后逐张调用 Codex CLI 当前会话暴露的内置图片工具。
5. 生成后检查白底、留白、角色参与、批注数量和“像不像 PPT”等问题，交给用户验收。
6. 用户接受后，才把副本保存到本地项目的 `assets/<article-slug>-illustrations/`；原始生成文件不移动、不覆盖。

## 九、项目目录结构

```text
.
├── README.md
├── README.en.md
├── LICENSE
├── NOTICE.md
├── tests/
│   └── test_skill_contract.py
├── .github/
│   └── workflows/
│       ├── codeql.yml
│       └── validate-skill.yml
├── docs/
│   └── examples/
│       ├── 01-article-input-anchor.png
│       ├── 02-anchor-to-action.png
│       ├── 03-qa-gate.png
│       └── 04-style-ip-authorization.png
└── cognitive-anchor-sketcher/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    └── references/
        ├── codex-cli-generation.md
        ├── composition-patterns.md
        ├── ip-profiles.md
        ├── prompt-template.md
        ├── qa-checklist.md
        ├── qa-dialogue-workflow.md
        ├── style-dna.md
        ├── style-presets.md
        └── xiaohei-ip.md
```

真正需要安装的是 `cognitive-anchor-sketcher/`。`docs/examples/` 只是公开示例，不参与运行；本地生成目录、自定义 IP 档案和审计报告按 `.gitignore` 规则留在本地。

## 十、注意事项

- **先确认，再生图。** 生成、改图和批量生成都必须走 QA 门禁；“直接生成”不是跳过确认的暗号。
- **小黑保持原样。** 未指定 IP 时使用原来的小黑档案；拓拓、星比和组合 IP 只在用户明确选择后出场。
- **黑色是主角。** 两种画风都以黑色线稿为主，蓝、黄、橙等颜色只作少量识别或动作提示，不让颜色把画面变成彩色海报。
- **不要提交密钥。** Skill 不读取或使用 `OPENAI_API_KEY`、`CODEX_API_KEY`，不调用 Images API、SDK 或其他图片供应商。
- **自定义 IP 要有权利。** 上传参考图不等于获得复制授权；只有用户明确确认的范围，才会建立项目级 profile。
- **人工验收不可省。** AI 参与生成的图片应由使用者检查内容、版权、文字和发布场景后再对外使用。
- **示例图不代表固定模板。** 它们用于校准风格密度和角色参与方式，不要求每次照抄“传送带、拉线或盖章”等旧构图。
- **自动检查是护栏，不是替身。** CI 和 CodeQL 能抓住一部分结构与安全问题，但不会替你判断文章是否真的说清楚，也不会替代发布前人工复核。

## 十一、相关项目

无。

## 十二、关于作者

### Enhe（恩禾）

产品设计师 · 一人公司实践者 · AI Builder

用 AI 打造一个人公司。

- GitHub：[yangjing6213-dev](https://github.com/yangjing6213-dev)
- X/Twitter：[@Amenenhe_ai](https://x.com/Amenenhe_ai)
- 网站：[www.enhe-tech.com.cn](https://www.enhe-tech.com.cn/)
- 微信：`Hu-Amen`
- 邮箱：`amen.enhe@gmail.com`

## 十三、继续探索

这个项目是作者用 AI 搭建的个人生成系统里的一个工具。如果你也在用 AI 做内容、知识库、工作流或产品化，可以访问 [www.enhe-tech.com.cn](https://www.enhe-tech.com.cn/) 查看更多资料。

## 许可证

本项目采用 MIT License，详见 [LICENSE](LICENSE)。
