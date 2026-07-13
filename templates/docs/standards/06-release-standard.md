# Release Standard

上下文分层、文件拆分和加载预算见 `12-context-governance.md`;本文件定义发布与
迭代关闭时由人确认的回写标准。

- List included Issues and MRs.
- Confirm testing result, configuration changes, database changes, rollback plan,
  monitoring, and post-release validation.
- Confirm whether the release was validated on an isolated dev/review environment
  or a shared test/staging environment.
- For shared test/staging, confirm human deployment approval, environment lock,
  deployed commit SHA, previous version, and rollback target.

## 文档回写清单

迭代产生的持久事实应在迭代关闭前合并进长效文档。由 `gj-close-loop` 提醒、
发布责任人人工确认；`context_freshness_check` 可按需运行，但不作为默认 CI 门禁：

- [ ] `docs/context/current-state.md` 已覆盖重写,反映当前迭代版本的事实
      (不追加变更历史,git 历史即归档)。
- [ ] 涉及模块的 `docs/modules/*.md` 已更新为当前完整规则。
- [ ] 本迭代 `ai-context-summary.md` 已写成且非空。
- [ ] `.gj/context.yml` 的 `recent_iteration_summaries` 已修剪:
      只保留最新一轮,旧条目移除(上限见 `max_recent_summaries_per_module`)。
- [ ] Retro 已回答:"长效文档里有什么已过时或没人读?" 过时内容直接删除。

## 文档生命周期规则

- **长效文档**(`docs/context/`、`docs/modules/`、`docs/standards/`、
  `docs/product/`、`docs/technical/`、`docs/qa/`):原地覆盖,
  永远描述"当前为真",数量恒定。AI 默认只读白名单
  `.gj/context.yml` 列出的部分。
- **迭代文档**(`docs/iterations/<迭代>/`、`docs/releases/<版本>.md`):
  一次写成,迭代结束冻结归档,默认不读;
  唯一例外是最近一轮 `ai-context-summary.md`。
- **过时内容直接删除**,不做"已废弃/superseded"标记,git 历史即归档。
- **小改动**(SmallChange):不建迭代目录,但若改动触碰业务规则,
  必须在同一 MR 内更新对应模块文档——回写纪律不因改动小而豁免。
- GitLab Issue/MR 评论记录讨论过程;仓库文档记录稳定结论。
  重要的产品、技术、测试、发布决策不允许只活在评论里,
  评论与仓库文档冲突时,以人工确认后的仓库文档为准。

## 必备文档(按需创建,路径为默认约定)

| 文档 | 默认路径 | 需要的时机 |
| --- | --- | --- |
| PRD | `docs/product/requirements/<feature>.md` | 新功能、行为/权限/金额/流程规则或验收标准变化 |
| 产品设计 | `docs/product/designs/<feature>.md` | UX、交互、页面状态、文案、权限可见性、错误处理有讲究时 |
| 原型记录 | `docs/product/prototypes/<feature>.md` | 存在 Figma/Axure/截图/可点击 demo 时 |
| 技术方案 | `docs/technical/solutions/<feature>.md` | 架构、接口、数据、权限、兼容、灰度或回滚需要决策时 |
| 测试计划 | `docs/qa/test-plans/<feature>.md` | 验收/回归/权限/失败路径覆盖不平凡时 |
| 测试报告 | `docs/qa/test-reports/<feature>.md` | QA 执行过验证或发现失败时 |
| 发布说明 | `docs/releases/<version>.md` | 用户可见行为、运维、灰度或回滚信息变化时 |
| 迭代摘要 | `docs/iterations/<迭代>/ai-context-summary.md` | milestone 或重要工作流结束时 |

## Definition Of Ready(进入方案设计前)

- PRD 存在,或需求 Issue 明确说明为何不需要 PRD。
- 验收标准可测试且包含反例。
- 非目标已声明。
- 产品负责人确认已记录。
- UX/设计/原型需求已链接或明确标记不需要。

## Definition Of Done(变更完成前)

- 持久结论已进仓库文档,不是只在 GitLab 评论里。
- MR 描述的"文档影响"段已填写(已更新什么/为何不需要/后续 Issue)。
- 相关文档在同一 MR 更新,或链接了后续文档 Issue。
- 长期 AI 上下文变化时,`docs/context/`、`docs/modules/` 或
  `ai-context-summary.md` 已更新。
