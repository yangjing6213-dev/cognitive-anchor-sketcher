# IP Profiles

## Resolution

- 默认 `xiaohei`：读取 `references/xiaohei-ip.md`，原文保持不变。
- `用小黑` → `xiaohei`
- `用拓拓` → `tuotuo`
- `用星比` → `xingbi`
- `用拓拓与星比` → `tuotuo-xingbi`
- `用我的 IP/<slug>` → `project ip-profiles/<slug>/profile.md`

显式指定的 profile 缺失、未知或路径无效时必须阻塞生成，不得静默回退到 `xiaohei` 或其他 profile。未指定 IP 时才使用默认 `xiaohei`。

当用户选择“我的自定义 IP”而没有可用的 profile 时，先读取 `qa-dialogue-workflow.md`。必须先判断当前会话是否存在用户上传且可访问的参考图；未上传时不能只报“缺失”，而要停在 `CUSTOM_REFERENCE_PENDING` 并给出上传、改内置 IP、仅分析或取消等选项。

## Built-in Profiles

### TuoTuo (`tuotuo`)

视觉识别（来自用户参考图的文字化抽象，不直接复制原图）：蓝色圆角方头、顶部单个闪电形突起、黑色粗框方眼镜，蓝色圆润身体与短四肢；胸口保留简化的白色几何闪电标记。采用黑色主导手绘转译时，蓝色只作为确认后的次级识别色，轮廓、眼镜、动作线和主要文字仍为黑色。

- `silhouette`：方头、闪电突起、眼镜横向宽于头部，短而圆的四肢。
- `palette`：黑色主导；蓝色为次级识别色，白色只用于眼镜高光/胸口标记等小面积细节。
- `line_or_material`：黑色手绘轮廓与少量灰色速写线；不使用渐变、塑料高光或厚重阴影。
- `face_and_expression`：眼镜内保留简洁黑色弧形眼；表情克制、专注，不画写实五官。
- `forbidden`：不得省略闪电突起与眼镜而画成泛化机器人；不得让蓝色覆盖黑色主导规则。

拓拓负责把抽象内容变成可执行的系统动作：

- `system`：系统边界、组件关系、状态和约束。
- `tools`：工具、接口、载体、输入输出和操作对象。
- `execution`：步骤、动作、路径、分拣、搬运和落地过程。
- `judgment`：筛选、取舍、判断点、失败条件和结果。

### XingBi (`xingbi`)

视觉识别（来自用户参考图的文字化抽象，不直接复制原图）：黄色五角星轮廓、圆润短肢、白色手套与白色鞋，黑色弧形笑眼和张口笑表情；保持轻快、指向性强的星形剪影。采用黑色主导手绘转译时，黄色只作为确认后的次级识别色，黑色轮廓、表情和动作线优先。

- `silhouette`：五角星主体、短肢、白色手脚形成清晰外轮廓。
- `palette`：黑色主导；黄色为次级识别色，白色只用于手套/鞋和小面积表情细节。
- `line_or_material`：黑色手绘轮廓、少量灰色速写线和动作线；不使用渐变、塑料高光或厚重阴影。
- `face_and_expression`：黑色弧形笑眼与简洁张口笑；可夸张但保持友好，不变成表情包合集。
- `forbidden`：不得画成普通圆形吉祥物或多星堆叠；不得让黄色覆盖黑色主导规则。

星比负责把抽象内容变成可感知的方向与反馈：

- `inspiration`：隐喻、联想、反常识的视觉切口。
- `signals`：线索、异常、情绪点、提示和弱信号。
- `goals`：想达成的状态、方向、意图和终点。
- `feedback`：结果、回声、偏差、用户反应和下一步修正。

### Pair (`tuotuo-xingbi`)

拓拓与星比可以同时出现，但职责必须分开：拓拓承担系统动作和判断，星比承担灵感、信号、目标和反馈。不要让两个角色重复表达同一层信息；同一张图仍只保留一个核心动作、结构、状态或隐喻。

## Orthogonal Style Selection

IP profile 与风格 preset 是两个独立维度：

- IP profile 决定角色身份、外形、性格、职责和可用动作。
- style preset 决定构图、线条或材质、色彩处理、留白和文字处理。
- 先解析风格，再解析 IP；不得因风格选择改变 IP 身份。
- 未指定风格时使用项目默认风格；未指定 IP 时使用默认 `xiaohei`。
- 显式 profile 或显式风格无法解析时分别阻塞，不用另一个维度的默认值掩盖错误。

## Project-local Custom Profile

自定义 IP 只允许走以下流程：

项目级布局可包含可选的 `ip-profiles/<slug>/references/` 目录；其中只能放入用户明确允许复制的参考图。未获此项明确许可的参考只能被引用或分析，不能复制到该目录。该目录属于当前用户项目的本地资料，默认不得进入本 Skill 的公开发行包或 Git 发布清单。

1. `upload/reference`：接收或引用用户提供的参考，并记录来源。
2. `draft`：自动提炼的草稿只存在于当前会话或临时上下文，状态为 `draft_unconfirmed`；确认前不得写入 `profile.md` 或 `provenance.md`。
3. `user confirmation`：用户明确确认 profile、使用范围和授权状态。
4. `save`：用户确认或修改后，才创建 `project ip-profiles/<slug>/profile.md` 和 `provenance.md`，并同步写入完整 provenance。

草稿可以用于讨论和分析，但不能用于生成。上传或引用本身不等于授权，也不等于允许复制。

### QA 入口与保存时点

- 已上传参考图：先提炼仅在会话中存在的 `draft_unconfirmed` 草稿，再让用户确认外形、动作、使用范围和授权状态。
- 未上传参考图：按 `qa-dialogue-workflow.md` 提醒上传；不得根据“我的 IP”这一说法虚构 profile。
- 只有用户明确选择项目级 `user_authorized` 后，才能创建 `profile.md` 和 `provenance.md`；用户没有允许复制时，记录非识别性来源说明与可得 SHA-256，但不得把原参考图复制到 `references/`。
- 用户选择仅分析时，状态是 `analysis_only`；不得生成、保存 profile 或复制参考图。

## Profile Fields

每个 `profile.md` 必须定义以下字段：

- `slug`
- `display_name`
- `characters`
- `silhouette`
- `palette`
- `line_or_material`
- `face_and_expression`
- `personality_and_roles`
- `allowed_actions`
- `forbidden`
- `source_reference`（使用非识别性说明，不记录可识别个人或设备的信息）
- `reference_mode`

`source_reference` 说明参考来源，`reference_mode` 说明允许的参考方式，例如 `analysis_only` 或用户明确限定的授权使用范围。字段缺失或无法判断时，profile 不可用于生成。

## Provenance

每个项目本地 profile 必须附带 `provenance.md`，并记录：

- `source_reference`
- `reference_mode`
- `sha256`（可获得时必填）
- `confirmed_at`
- `confirmation_source`（固定为 `user_confirmed`，不记录个人身份）
- `authorization_status`

`authorization_status` 必须明确为以下状态之一：

- `missing` / `unknown`：来源或授权缺失、未知；阻塞分析后的生成。
- `draft_unconfirmed`：草稿尚未获用户确认；阻塞生成。
- `analysis_only`：只允许分析和提炼抽象特征，不得复制参考内容；阻塞以该参考为基础的生成。
- `user_authorized`：允许按用户明确确认的范围使用；只允许使用该范围。

任何状态不明确、互相矛盾或超出授权范围的 profile 都必须阻塞。不得把 `analysis_only` 或 `draft_unconfirmed` 解释成 `user_authorized`。

## Emotion-doodle Priority

情绪涂鸦场景以黑色主导的身份识别优先。用户确认前，忽略候选 profile 的 identity colors；确认后颜色仍只作为次要辅助，不得压过黑色主体、轮廓和表情识别。
