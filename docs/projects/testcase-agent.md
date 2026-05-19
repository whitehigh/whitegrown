# 测试用例生成 Agent

## 项目目标

将需求文档或功能描述转换为测试点、测试用例、边界场景和风险清单，减少测试用例初稿编写成本。

## 输入

- 功能需求描述或需求文档
- 业务模块名称
- 平台或地区信息
- 已知规则和限制

## 输出

- 功能测试点
- 正向用例
- 异常用例
- 边界场景
- 风险清单
- 回归建议

## Agent 工作流

1. 理解需求目标
2. 拆解功能链路
3. 识别关键状态和数据变化
4. 生成测试点和边界条件
5. 输出结构化测试清单
6. 等待人工确认和补充

## 当前 demo 能力

- 支持直接输入需求文本
- 支持通过 `--file` 读取 `.md` / `.txt` 需求文档
- 支持 Markdown 输出，适合人工阅读
- 支持 JSON 输出，适合接入 Web 页面、CI 或测试管理平台
- 针对商城、支付、充值、登录、跨服、月卡等关键词生成更贴近游戏测试的检查点

## 适用场景

- 商城、支付、登录、跨服匹配等复杂功能
- 版本迭代前的测试设计
- 新人测试工程师用例初稿生成
- 回归测试范围梳理

## 运行 Demo

```bash
python3 examples/testcase_agent_demo.py "商城支持购买月卡，支付成功后立即发放奖励，重复购买需要延长有效期"
```

从需求文档读取：

```bash
python3 examples/testcase_agent_demo.py --file examples/sample_requirement.md
```

输出 JSON：

```bash
python3 examples/testcase_agent_demo.py --file examples/sample_requirement.md --format json
```
