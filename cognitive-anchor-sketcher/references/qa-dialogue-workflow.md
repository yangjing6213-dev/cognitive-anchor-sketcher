# 用户确认式 QA 工作流

## 适用范围

任何要求生成、批量生成、改图，或以自定义 IP 生成正文配图的请求，都先进入本流程。用户只要分析、shot list 或提示词时，可在对应交付阶段结束，不调用生图工具。

即使用户说“直接生成”，也不能跳过关键确认。用户在原始请求中已明确给出的选择可以成为对应阶段的当前选项，但仍要展示该阶段的 3–5 个选项并让用户确认或改选；推荐值、默认值、沉默和模型推断都不算确认。

## 对话规则

- 一次只推进一个 `*_PENDING` 阶段；先问一个问题，再等待用户选择。
- 每个问题给 3–5 个互斥的业务选项，标出推荐项；用户也可以给出能明确映射到选项的自由文本。
- 所有阶段都接受：`修改`、`返回`、`取消`。这些是全局控制命令，不替代业务选项。
- 无法判断用户选择时，说明当前待确认项并重新给出选项；不能猜测。
- 在生成前和每次回退后，回显简短的已确认摘要。不要自动把会话摘要写入 workspace。

## 状态机

```text
INTAKE
  → DIRECTION_PENDING
  → STYLE_PENDING
  → IP_PENDING
      → CUSTOM_REFERENCE_PENDING
      → CUSTOM_DRAFT_PENDING
      → CUSTOM_AUTHORIZATION_PENDING
  → SHOT_LIST_PENDING
  → OUTPUT_SPEC_PENDING
  → GENERATION_CONFIRM_PENDING
  → GENERATION_READY
  → GENERATE
  → INTERNAL_QA
  → USER_REVIEW
  → DELIVERED | CANCELLED
```

`DIRECTION_PENDING`、`STYLE_PENDING`、`IP_PENDING`、`SHOT_LIST_PENDING`、`OUTPUT_SPEC_PENDING` 和 `GENERATION_CONFIRM_PENDING` 是生图前必经门。只有状态为 `GENERATION_READY` 时才可调用 `image_gen`。

## 会话记录

在回复中维护以下最小记录；仅当自定义 IP 已获授权时，才按 `ip-profiles.md` 写入项目档案。

```text
qa_state:
article_source:
article_direction:
style_profile:
ip_profile:
custom_profile_status:
authorization_status:
shot_list:
output_spec:
generation_mode:
```

## 阶段与选项

### `INTAKE`：缺少文章材料时

1. 粘贴文章全文（推荐）
2. 提供公开文章链接
3. 上传 Markdown、文档或截图
4. 提供标题、提纲和核心观点
5. 只做配图方向分析；本次到此结束，不生成图片

已有可靠文章材料时，记录来源并进入方向确认。

### `DIRECTION_PENDING`：文章转化方向

先用一句话概括文章，再询问：

1. 准确解释核心观点（推荐）
2. 强化“痛点 → 转折 → 结果”
3. 解释方法、流程或系统结构
4. 强化产品价值与使用场景
5. 用怪诞隐喻表达抽象认知

### `STYLE_PENDING`：画风

只提供当前已存在的预设或不生成的暂缓入口：

1. `minimal-line`：纯白、细黑手绘、冷静怪诞（推荐）
2. `emotion-doodle`：黑色主导、动作更强的情绪涂鸦
3. 先不锁定画风，只输出方案，稍后确认

用户要求新增或自定义画风时，先停在分析/方案阶段；未形成并确认可执行规则前，不得把它当作已有预设使用。

### `IP_PENDING`：IP 形象

1. 小黑 `xiaohei`（推荐）
2. 拓拓 `tuotuo`
3. 星比 `xingbi`
4. 拓拓与星比 `tuotuo-xingbi`
5. 我的自定义 IP

显式指定但不存在的画风或 IP/profile 必须阻塞，不得回退为默认值。

### `CUSTOM_REFERENCE_PENDING`：自定义 IP 但没有可用参考图

先检查当前会话中是否真的有用户上传且可访问的参考图。没有时暂停生成并询问：

1. 上传 IP 参考图（推荐）
2. 改用小黑
3. 返回选择其他内置 IP
4. 只分析我对 IP 的文字描述；本次到此结束，不生成图片
5. 取消本次任务

上传图本身不表示复制、保存或生成授权。

### `CUSTOM_DRAFT_PENDING`：已有参考图

只提炼抽象特征，生成临时 profile 草稿；不要临摹、抠图、保存 profile 或调用生图工具。展示草稿后询问：

1. 接受草稿，继续确认授权（推荐）
2. 修改外形、颜色、表情或可执行动作
3. 替换参考图后重新提炼
4. 仅分析参考图，不用于生成
5. 放弃自定义 IP，返回内置 IP

### `CUSTOM_AUTHORIZATION_PENDING`：授权与保存范围

清晰重述来源、草稿、使用范围和是否复制参考图，并要求用户确认其拥有或已获得使用该参考/IP 的必要权利，然后询问：

1. 我确认拥有必要权利；授权本项目生成并保存 profile，不复制参考图（推荐）
2. 我确认拥有必要权利；授权本项目生成、保存 profile，并复制参考图到当前项目本地的 `ip-profiles/<slug>/references/`
3. 修改授权范围或 profile 草稿
4. 仅分析，不生成也不保存 profile
5. 改用内置 IP

只有选项 1 或 2 且权利确认清晰，才能把 `authorization_status` 设为 `user_authorized`。权利不明、第三方许可不清或用户拒绝确认时，状态保持 `unknown` 或 `analysis_only`，不得生成或保存项目 profile。随后才可创建 `profile.md`、`provenance.md`，并在可读取时记录 SHA-256。选项 2 之外不得复制参考图。自定义档案仅保存于当前项目本地，默认不得纳入本 Skill 的公开发行包。`missing`、`unknown`、`draft_unconfirmed`、`analysis_only` 一律不能生成。

### `SHOT_LIST_PENDING`：认知锚点与数量

先给出推荐的段落位置、每图核心认知、构图、角色动作和短批注，再询问：

1. 确认推荐 shot list（推荐）
2. 调整图片数量或段落位置
3. 标记“先生成第一张试稿”，仍继续确认输出规格与最终生成门
4. 只交付 shot list / 提示词，不生成图片
5. 返回修改文章转化方向

### `OUTPUT_SPEC_PENDING`：输出规格

无论用户在原始请求中是否已给出输出规格，都要回显当前选择并询问：

1. 16:9 PNG、纯白、中文短批注、保存到项目资产目录（推荐）
2. 16:9 PNG、纯白、无图内中文文字
3. 只交付可复制提示词；本次到此结束，不生成图片
4. 说明其他输出约束；仍须符合本 Skill 的 16:9 正文配图边界

### `GENERATION_CONFIRM_PENDING`：最终确认

先展示摘要：文章方向、画风、IP/授权状态、图片数、每图核心认知、输出规格与保存路径。然后询问：

1. 按当前方案生成全部图片（推荐）
2. 只生成第一张试稿
3. 返回修改 shot list 或输出规格
4. 仅保留方案与提示词，不生成图片
5. 取消生成

选项 1 或 2 才将状态设为 `GENERATION_READY`。

### `USER_REVIEW`：生成后的用户验收

先按 `qa-checklist.md` 完成内部视觉 QA，再附上结果和图片预览，询问：

1. 接受全部图片（推荐）
2. 指定图片重新生成
3. 只修改中文批注、留白或构图
4. 返回修改画风或 IP；先选择回到画风阶段还是 IP 阶段，再重新展示对应的 3–5 个选项
5. 保留当前版本并结束

选项 2 或 3 只针对指定图片；保留其余已确认选择。先回显该图的变更、输出规格和保存路径，再回到 `GENERATION_CONFIRM_PENDING` 给出最终确认菜单。只有用户再次确认生成后，才设为 `GENERATION_READY` 并调用生图工具。

未得到用户对重生成或编辑的明确选择时，不要静默重复调用生图工具。

## 回退与失效

| 用户变更 | 保留 | 必须重新确认 |
| --- | --- | --- |
| 文章方向 | 文章来源 | shot list、输出规格、生成确认 |
| 画风 | 文章方向、IP | shot list 适配、输出规格、生成确认 |
| 内置 IP | 文章方向、画风 | 角色动作、shot list、输出规格、生成确认 |
| 自定义 IP 参考或授权 | 文章方向、画风 | 自定义草稿、授权、shot list、输出规格、生成确认 |
| 图片数量或输出规格 | 上游内容 | 生成确认 |
| 某张图片的视觉问题 | 所有已锁定上游选择 | 该图的变更、输出规格与生成确认 |

不删除已生成资产；重生成用新版本文件，除非用户明确要求替换。
