# 示例演练参考

复盘输入：

- 演练记录：`examples/demo-run/00-run-log.md`
- 角色记录：`examples/demo-run/roles/`

关键经验：

1. API 项目标识不匹配是预检阻塞项。
2. 本地 Token helper 必须被忽略，不能进入开源包。
3. Skill 元数据生成后应立即校验。
4. QA 失败必须转为包含回归范围的 Bug Issue。
5. 首批 Skill 在第二次演练验证前保持草稿状态。
6. Windows 默认区域设置无法读取 UTF-8 中文 `SKILL.md` 时，生成元数据需传 `--name`。

长期上下文产物：

- `docs/context/current-state.md`
- `docs/modules/order.md`
- `.gj/context.yml`
