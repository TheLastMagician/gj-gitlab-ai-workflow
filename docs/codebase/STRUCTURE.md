# 仓库结构

```text
.gj/                         当前项目的 AI 配置
.gj/doc-templates/           已安装的文档模板，不是项目事实
.gitlab/                     当前项目的 GitLab 模板
docs/context/                稳定的 AI 上下文
docs/codebase/               已确认的代码库地图
docs/product/                当前产品需求和交互事实
docs/technical/              当前方案、API、数据库和 ADR 事实
docs/modules/                模块知识
docs/qa/                     可复用测试计划和按 Tag 保存的测试证据
docs/releases/               按 Tag 保存的发布证据
examples/demo-project/       精简订单审批示例项目
examples/demo-run/           首次端到端演练产物
orchestrator/                Webhook 路由骨架
scripts/                     CI 和工具脚本
skills/                      八个跨 Agent 工作流 Skill
templates/                   安装到目标项目的可复用资产
```

文档模板安装在 `.gj/doc-templates/`；项目事实目录只在对应能力或边界存在时创建使用语义名
的文档。
