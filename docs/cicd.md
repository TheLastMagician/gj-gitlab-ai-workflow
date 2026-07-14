# CI/CD 流程

目标业务项目引用安装后的 `.gitlab/gj-workflow-ci.yml`。GJ Job 使用自己的 Python 镜像
和 GitLab 内置 `.pre`/`.post` 阶段，不会替换现有项目镜像、stage 和默认配置。

## 阶段

| 阶段 | Job | 作用 |
| --- | --- | --- |
| `.pre` | `policy_check` | 硬检查唯一 `flow::*` 标签、Standard/Hotfix Issue 关联、变更文件风险路径和新增秘密；MR 模板完整性只告警。 |
| `.pre` | 提醒型 `workflow_assets_check`、可选 `validate_role_map` | 报告工作流配置问题，不阻断普通 MR；上下文审计按需手工运行。 |
| `.pre` | `smoke_check` | 运行目标项目的冒烟测试命令。 |
| 项目自有 | `deploy_dev`、`deploy_test` | 可选的项目部署 Job；开发环境可自动部署，共享测试环境必须手工触发并加锁。 |
| `.pre` | `release_version_check` | 仅在 Tag Pipeline 要求合法 SemVer 和匹配的 ready/released 发布说明。 |
| `.post` | 提醒型 `release_dry_run` | 在 Tag 或手工默认分支 Pipeline 生成带版本信息的发布检查清单，供人确认。 |

## Runner 要求

示例应使用 Docker executor 的项目 Runner 和 `python:3.12-slim`。Windows shell Runner
曾暴露 GitLab Runner PowerShell 工作目录问题，因此推荐 Docker executor 以便稳定复现
目标项目校验。

## GitLab CE 门禁

- 保护默认分支并限制可以合并的人。
- 要求 Pipeline 成功后才能合并。
- 低风险 Fast MR 不要求额外审批人数。
- 高风险变更文件不能使用 `flow::fast`；必须有 Standard/Hotfix 证据和人工合并决定。
- CODEOWNERS 和可选 Approve 动作可以辅助审阅，但工作流以 GitLab 权限和合并记录为
  事实源。

如果 Docker Hub 访问受限，但本地已有 `python:3.12-slim`，按以下方式配置 Runner：

```toml
[runners.docker]
  image = "python:3.12-slim"
  pull_policy = "if-not-present"
```

## 预期 Pipeline

```text
MR 硬门禁：policy -> test
提醒 Job：workflow assets / release dry run
```

## 环境部署策略

部署脚本由项目决定，因此模板默认不部署。项目有真实部署命令后再添加部署 Job。

推荐默认规则：

- MR 分支只能自动部署到隔离的开发/评审环境。
- `develop` 或 `integration` 可以自动部署到开发环境。
- 共享 `test` 或 `staging` 必须使用 `when: manual`。
- 共享环境必须使用 `resource_group`，例如 `resource_group: test-env`。
- 每次共享测试部署都要记录分支、MR、commit SHA、Pipeline URL、部署人、上一版本、
  回滚目标和 QA 负责人。

示例：

```yaml
deploy_dev:
  stage: deploy
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'
    - if: '$CI_MERGE_REQUEST_IID'
  environment:
    name: dev/$CI_COMMIT_REF_SLUG
    auto_stop_in: 2 days
  script:
    - ./scripts/deploy_dev.sh

deploy_test:
  stage: deploy
  when: manual
  rules:
    - if: '$CI_COMMIT_BRANCH == "develop"'
    - if: '$CI_COMMIT_BRANCH =~ /^release\//'
  resource_group: test-env
  environment:
    name: test
  script:
    - ./scripts/deploy_test.sh
```

## 产物

- `build/release-dry-run.md`
