# Cognitive Anchor Sketcher

> 把中文文章里的一个认知锚点，变成一张白底、手绘、清晰而有记忆点的正文配图。

`cognitive-anchor-sketcher` 是一个 Codex Skill，用于中文文章、帖子、博客、Notion 文档、工作流文档和方法论内容的正文配图设计与生成。

它不是通用插画提示词，也不是 PPT 信息图模板。Skill 会先理解文章中的判断、流程、结构、状态或隐喻，再把其中一个核心认知动作转译成 16:9 横版手绘解释图。

## 核心能力

- 从文章中提炼认知锚点，不平均堆图。
- 每张图只表达一个核心动作、结构、状态或隐喻。
- 默认使用“小黑”IP：黑色实心、白点眼、细腿、空表情；角色必须参与核心动作。
- 支持 `minimal-line` 与 `emotion-doodle` 两种画风预设。
- 支持小黑、拓拓、星比、拓拓与星比，以及经过授权的项目级自定义 IP。
- 生成前执行确认式 QA：文章方向、画风、IP、授权、shot list、输出规格和生成模式逐项确认。
- 生图只使用已通过 ChatGPT 登录的 Codex CLI 及其内置图片生成工具；不使用 API 密钥、Images API 或其他提供商回退。
- 生成后按 QA 清单检查留白、角色参与、中文批注、白底和非 PPT 感，并等待用户验收。

## 输出边界

默认输出：

- 16:9 横版正文配图方案和 shot list。
- 每张图的段落位置、核心意思、结构类型、角色动作、元素和短批注建议。
- 按用户确认的规格生成单张 PNG；保留工具返回的原始文件，用户接受后再无覆盖地复制到 `assets/<article-slug>-illustrations/`。

不负责：

- PPTX、PDF、Keynote、SVG 或可编辑矢量源文件。
- 商业海报、品牌 KV、复杂架构图或大段文字信息图。
- 未经确认的自定义 IP 复制、保存或生成。

## 安装

在仓库页面复制 HTTPS 地址后运行：

```bash
git clone <repository-url>
cd cognitive-anchor-sketcher
```

将 `cognitive-anchor-sketcher/` 复制到 Codex 的 Skill 目录：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ./cognitive-anchor-sketcher "${CODEX_HOME:-$HOME/.codex}/skills/"
```

安装后，在 Codex 中调用：

```text
Use $cognitive-anchor-sketcher 为这篇中文文章设计正文配图。
```

## 生图环境

生图后端唯一允许使用已通过 ChatGPT 登录的 Codex CLI，以及当前 Codex 会话实际暴露的内置图片生成工具。不需要也不得提供、读取或使用 `OPENAI_API_KEY`、`CODEX_API_KEY`；本 Skill 不调用 Images API、`image_gen.py`、SDK，也不回退到其他图片提供商。非 CLI 宿主按执行契约桥接时，还需要本机官方 Codex CLI 及其运行时依赖（PowerShell 或 POSIX 示例会先做来源和版本检查）。

- 当前已经是 Codex CLI 会话且内置图片生成工具可用时，直接调用，不再启动 Codex。
- 明确处于非 CLI 宿主时，完成版本与 ChatGPT 登录状态预检后，最多用一次 `codex exec --ephemeral` 桥接；桥接进程不得再次启动 Codex。
- CLI、ChatGPT 登录、内置工具、生成结果或工具返回的输出文件任一不可用时，立即停止并报告恢复步骤，不自动重试或回退。

PowerShell、POSIX shell 的安全桥接方式、输出路径与失败处理详见 [`codex-cli-generation.md`](cognitive-anchor-sketcher/references/codex-cli-generation.md)。原始生成目录 `.codex/generated_images/` 只保留在本地，并已加入本仓库忽略规则。

## 使用示例

只做配图规划：

```text
Use $cognitive-anchor-sketcher 先不要生图。
请分析下面这篇文章的认知锚点，输出 5 张左右的 shot list。
每张图写清楚段落位置、核心意思、结构类型、IP 动作和中文标注建议。
```

生成正文配图：

```text
Use $cognitive-anchor-sketcher 为下面的中文文章生成正文配图。
请按 QA 流程逐项确认文章方向、画风、IP、shot list 和输出规格后再生成。
```

选择画风或 IP：

```text
画风：emotion-doodle
IP：拓拓与星比
要求：16:9、纯白背景、黑色主导手绘线稿、少量彩色批注。
```

自定义 IP：

```text
使用我的自定义 IP。先检查我是否上传参考图；没有参考图时先提醒上传，
有参考图时先输出草稿并确认授权范围，不要直接生成。
```

## QA 流程

生图或改图请求必须依次经过：

1. 文章材料与转化方向确认。
2. 画风确认：`minimal-line`、`emotion-doodle` 或暂不锁定。
3. IP 确认：小黑、拓拓、星比、组合或自定义 IP。
4. 自定义 IP 分支：检查参考图、提炼草稿、确认使用范围和必要权利。
5. shot list 与图片数量确认。
6. 输出规格与生成模式确认。
7. 用户最终确认后，才进入生成。

每个阶段一次只询问一个问题，并提供 3–5 个选项。用户选择修改或返回时，只让受影响的下游阶段重新确认。

## 目录结构

```text
.
├── README.md
├── LICENSE
├── NOTICE.md
└── cognitive-anchor-sketcher/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    └── references/
        ├── composition-patterns.md
        ├── codex-cli-generation.md
        ├── ip-profiles.md
        ├── prompt-template.md
        ├── qa-checklist.md
        ├── qa-dialogue-workflow.md
        ├── style-dna.md
        ├── style-presets.md
        └── xiaohei-ip.md
```

真正需要安装到 Codex 的是 `cognitive-anchor-sketcher/` 子目录。

## 开源与隐私边界

- 仓库不包含私人资料、浏览器记录、历史文章、生成配图或外部项目源码。
- 示例图不是运行依赖；本次最小发行版不包含示例图片。
- 自定义 IP 参考图只有在用户明确确认必要权利和保存范围后，才允许建立项目级档案。
- 项目级自定义 IP 档案属于用户本地内容，默认不纳入开源仓库或发布清单。
- `.codex/generated_images/` 中的原始生成文件只保留在本地；用户接受的副本也不得覆盖现有资产。
- 不要把 Token、密钥、Cookie、私有数据或本地报告复制到仓库。

## 许可证

MIT License，详见 [LICENSE](LICENSE)。
