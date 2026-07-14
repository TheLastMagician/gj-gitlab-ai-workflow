# 示例演练参考

Release Issue #7 包含：

- 工作流骨架。
- GitLab 模板。
- AI 配置。
- CI/CD Pipeline。
- 示例项目。
- 草稿 Skill。

发布验证最终在 Pipeline #19842 成功：

- policy.
- validate.
- test.
- package.
- release.

Runner 经验：

- 优先使用 Docker executor。
- 本地已有 Python 镜像且 Docker Hub 访问受阻时，使用
  `pull_policy = "if-not-present"`。
