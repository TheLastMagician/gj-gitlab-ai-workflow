# 环境部署策略

判断是否把分支或 MR 部署到非生产环境时使用本参考资料。

## 默认模型

- 开发环境追求速度，可以自动部署。
- 共享测试环境追求稳定，需要人工确认。
- 生产环境不属于本 Skill，由发布治理负责。

## 共享测试环境必填记录

部署到共享测试环境前记录：

- 目标环境
- 来源分支或 MR
- commit SHA
- Pipeline URL 和状态
- 部署申请人
- 不同时的部署批准人
- 上一个已部署版本
- 回滚命令或回滚目标
- 预期 QA 负责人和测试窗口

部署后记录：

- 部署时间
- 已部署版本
- 部署 Job URL
- 冒烟结果
- QA 状态
- 是否需要把环境恢复到基线

## GitLab CI 模式

```yaml
stages:
  - policy
  - workflow
  - test
  - build
  - deploy
  - release

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
    - if: '$CI_COMMIT_BRANCH =~ /^release\\//'
  resource_group: test-env
  environment:
    name: test
  script:
    - ./scripts/deploy_test.sh
```

项目只有一个测试环境时，不要把每个 MR 分支自动部署到该环境。
