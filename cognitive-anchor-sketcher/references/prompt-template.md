# 生图提示词模板

每张图单独生成。根据正文内容替换变量，不要把多张图拼在一起。

## 变量解析

- `{style_profile}`：未指定时使用 `minimal-line`；读取对应画风预设，风格只控制渲染语言。
- `{ip_profile}`：未指定时使用 `xiaohei`；读取对应 IP 档案，IP 决定角色身份、外形、性格、职责和允许动作。
- `{selected_characters}`：未指定时使用 `{ip_profile}` 的默认角色；`xiaohei` 的默认角色是“小黑”。
- 显式指定的风格或 IP 无法解析时必须阻塞生成，不得静默回退到默认值。

## QA 门禁

只有 `qa_state = GENERATION_READY` 时才能使用本模板。生成前先从 `qa-dialogue-workflow.md` 取得已确认摘要；若文章方向、画风、IP/授权、shot list、输出规格或生成模式仍是 pending，返回对应确认问题，不得写生图提示词或调用生图工具。

`{qa_summary}` 至少包含：

- 已确认的文章转化方向
- 已确认的画风与 IP
- 自定义 IP 的授权状态与允许范围（如适用）
- 已确认的当前图片核心认知与 shot list 位置
- 已确认的 16:9 输出规格与生成模式

```text
Generate one standalone 16:9 horizontal Chinese article illustration.
Canvas: 16:9 horizontal, 纯白背景.

Approved QA summary:
{qa_summary}

Selected style profile:
{style_profile}（未指定时为 `minimal-line`）

Apply the selected style profile as the source of truth for line quality, composition, color, whitespace, and text treatment. Do not import color or material constraints from another style profile. Keep the result clean and sparse, with no gradients, shadows, paper texture, complex background, commercial vector style, PPT infographic look, cute mascot poster, children's illustration, or realistic UI.

Selected IP profile:
{ip_profile}（未指定时为 `xiaohei`）

Selected characters:
{selected_characters}

Render the selected IP as the core action subject, not decoration. Follow the selected style profile's line, color, whitespace, and prohibition rules. Do not copy the reference image directly.
Use only the selected characters and the resolved IP profile. Preserve their defined silhouette, personality, roles, allowed actions, and forbidden traits. Do not replace them with 小黑 unless the selected IP is xiaohei.

Theme:
{正文配图主题}

Structure type:
{结构类型：Workflow / 系统局部 / 前后对比 / 角色状态 / 概念隐喻 / 方法分层 / 地图路线 / 小漫画分镜}

Core idea:
{这张图要表达的核心意思}

Composition:
{具体画面：当前所选角色在哪里、正在做什么、主要物件是什么、信息如何流动}

Suggested elements:
{元素1} / {元素2} / {元素3} / {元素4}

Chinese handwritten labels:
{标注词1} / {标注词2} / {标注词3} / {标注词4} / {可选标注词5}

Color use:
Follow the selected style profile's color rules. Do not force minimal-line's black/orange/red/blue scheme onto another style, especially `emotion-doodle`; retain black as its identity anchor and use only its documented accent-color limits.

Constraints:
One image explains only one core structure. Keep the main subject around 40%-60% of the canvas. Preserve at least 35% blank white space. Use at most 5-8 short handwritten Chinese labels. Do not write a title in the top-left corner. Do not write the structure type on the image. Do not make it a formal diagram, course slide, or dense explainer. Do not copy prior examples or reuse known case compositions unless explicitly requested; invent a fresh visual metaphor for this specific article. It should be clear but not instructional, interesting but not childish, strange but clean.
```

## 图像编辑提示

去掉左上角标题：

```text
Edit the provided image using style profile "{style_profile}" and IP profile "{ip_profile}". Remove only the handwritten title "{要删除的文字}" and its underline from the top-left corner. Fill that area with the same clean background required by the selected style profile. Preserve everything else exactly: {selected_characters}, labels, paths, line style, composition, aspect ratio, and image quality. Do not add any new text or objects or replace the selected characters.
```

增强怪诞感：

```text
Regenerate this illustration with the same core meaning and simple layout, using style profile "{style_profile}" and IP profile "{ip_profile}". Make {selected_characters} more central to the conceptual action: they should perform the strange work that explains the idea, not stand beside the diagram. Keep the selected IP recognizable, preserve its allowed actions, and do not make it cute or import another style profile's color rules.
```
