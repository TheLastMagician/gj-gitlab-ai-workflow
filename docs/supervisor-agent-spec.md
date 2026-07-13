# 监督员 Agent 实现规格(Supervisor Agent Spec)

> 本文档是给外部实现者的规格说明。监督员是一个独立于本工作流包的外部
> agent/脚本,工作流仓库只约定它的行为边界、输入输出和检查清单。
> 实现语言、部署方式、是否使用 LLM 都由实现者决定。

## 定位

监督员是**只读观察者 + 催办者**。它定时扫描 GitLab 项目状态,产出摘要
和提醒。它不是执行者:发现问题后开 issue、发评论、@人,但**永不动手修**。

## 触发方式

- GitLab scheduled pipeline 或外部 cron,每日 1~2 次。
- 频率上限:每日 2 次。不做分钟级轮询(空转烧钱、无增量信息)。

## 权限边界(硬约束)

| 允许 | 禁止 |
| --- | --- |
| 只读 API:issues、MR、pipeline、milestone、仓库文件 | push 代码、改文件 |
| 创建/更新自己的摘要 issue | approve / merge / close 他人 issue 或 MR |
| 发评论、@成员 | 修改 label 以外的任何资源状态 |
| 给 issue/MR 加"催办"类 label(可选) | 触发部署或其它 pipeline |

GitLab token 配置:使用项目级 access token;纯读取只给 `read_api`,确实需要评论或
标签写入时才改用 `api`。绝不使用个人管理员 token。token 存 CI/CD masked/protected
变量,不落盘、不入库(遵循 `docs/gitlab-access.md` 和
`docs/standards/08-security-standard.md`)。

## 检查清单(基础版,纯 API 可实现,无需 LLM)

每次运行对项目做以下检查,命中则记入摘要:

1. **评审滞留**:open 状态且非 Draft 的 MR,最后活动距今 > 48h
   且无人 approve → 列出 MR、等待时长、指派的 reviewer。
2. **孤儿任务**:label 为 doing/in-progress 的 issue,无关联 MR
   且 > 48h 无更新 → 列出 issue 和 assignee。
3. **失败无人管**:默认分支或 open MR 的最新 pipeline 状态为 failed,
   且失败后无新提交、无相关评论 → 列出 pipeline 链接和触发者。
4. **临期 milestone**:active milestone 距 due date ≤ 3 天,
   列出未关闭 issue 数和清单。
5. **回写欠账**:最新 `docs/iterations/<迭代>/05-release.md` 非空
   (说明已发布)但 `docs/context/current-state.md` 未提及该迭代版本号
   → 提示回写未完成(逻辑同 `scripts/context_freshness_check.py`,
   可直接复用该脚本判断)。

## 检查清单(增强版,需要 LLM,可后续再加)

6. **文档与代码矛盾**:抽取 `docs/modules/*.md` 声明的业务规则,
   与最近合并 MR 的 diff 对照,发现描述不一致时提示(仅提示,
   由人判断哪边错)。
7. **摘要质量**:把基础版的结构化发现改写成简短可读的中文日报。

## 输出

1. **摘要 issue**:项目里维护一个固定的置顶 issue
   (title: `[监督员] 项目状态日报`,label: `supervisor-digest`)。
   每次运行把当日摘要作为**新评论**追加(不刷新 description,
   保留历史可追溯)。全部检查通过时也发一条"全绿"短评,证明自己活着。
2. **催办评论**:对命中检查 1~3 的具体 MR/issue,在其下追加一条评论
   @ 对应 owner。同一对象 72h 内不重复催办(用自身评论历史去重)。

### 摘要格式约定

```markdown
## 项目状态日报 <日期>

- 评审滞留:<n> 件
  - !<iid> <标题> — 等待 <小时>h,reviewer @<user>
- 孤儿任务:<n> 件
- 失败 pipeline:<n> 件
- 临期 milestone:<名称>,剩 <天> 天,未关闭 <n> 件
- 回写欠账:<有/无>

<全部为 0 时:今日全绿。>
```

## 与本工作流的接口(实现者需要知道的约定)

- 角色与 owner 名单:`.ai/project.yml` 的 `owners` 段。
- 高风险路径:`.ai/rule-map.yml`(检查 6 可用它决定优先扫哪些模块)。
- 回写判断:`scripts/context_freshness_check.py` 可直接调用,
  exit code 非 0 即"回写欠账"。
- AI 边界:`docs/standards/09-ai-development-boundary.md` 对监督员
  同样生效——它是"AI 起草提醒、人做决定"的一个实例。

## 验收标准

- [ ] 在无任何异常的项目上运行,只产生一条"全绿"评论,无其它写操作。
- [ ] 构造一个 48h 无评审的 MR,运行后摘要列出它且 reviewer 被 @。
- [ ] 72h 内重复运行,同一 MR 不被重复催办。
- [ ] 只读实例的 token 仅有 `read_api`;需要评论/标签的实例才使用 `api`,
      且尝试 push/merge 操作失败。
- [ ] 单次运行 GitLab API 调用次数有上限(建议 < 200),不做全量分页扫历史。
