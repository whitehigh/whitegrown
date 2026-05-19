#!/usr/bin/env python3
"""Turn a requirement document into QA test points, cases, risks, and boundaries.

This demo does not call an LLM yet. It keeps the repository runnable without
API keys and shows the workflow that can later be replaced by an AI Agent.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path


DEFAULT_REQUIREMENT = "商城支持购买月卡，支付成功后立即发放奖励，重复购买需要延长有效期"


@dataclass
class TestPlan:
    requirement: str
    functional_points: list[str]
    test_cases: list[dict[str, str]]
    boundary_cases: list[str]
    risks: list[str]
    regression_suggestions: list[str]


def generate_test_plan(requirement: str) -> TestPlan:
    keywords = {
        "支付": ["支付成功发货", "支付取消", "支付失败", "重复支付", "弱网支付回调"],
        "充值": ["到账校验", "订单状态", "补单流程", "金额档位", "渠道差异"],
        "登录": ["正常登录", "Token 过期", "切换账号", "第三方授权失败", "游客账号绑定"],
        "跨服": ["匹配成功", "匹配超时", "跨服断线重连", "数据同步", "赛季结算"],
        "商城": ["商品展示", "库存限制", "价格校验", "购买限制", "奖励发放"],
        "月卡": ["首次购买", "重复购买", "有效期延长", "每日领取", "过期处理"],
    }

    functional_points: list[str] = []
    for key, points in keywords.items():
        if key in requirement:
            functional_points.extend(points)

    if not functional_points:
        functional_points = ["主流程验证", "异常流程验证", "数据落库校验", "前后端显示一致性"]

    test_cases = [
        {
            "id": "TC-001",
            "title": "主流程验证",
            "precondition": "账号状态正常，功能入口可见，服务端配置已生效",
            "steps": "进入功能入口，按需求完成一次完整操作，观察客户端提示和服务端数据变化",
            "expected": "操作成功，客户端提示正确，奖励、订单或状态数据与需求一致",
        },
        {
            "id": "TC-002",
            "title": "异常流程验证",
            "precondition": "账号状态正常，准备异常输入、弱网或中断条件",
            "steps": "在关键步骤触发取消、失败、断线重连或重复点击",
            "expected": "系统不产生脏数据，不重复发放奖励，错误提示清晰，可继续恢复或重试",
        },
        {
            "id": "TC-003",
            "title": "数据一致性验证",
            "precondition": "具备客户端、后台或数据库验证条件",
            "steps": "完成操作后核对客户端展示、订单状态、资产变化和数据库记录",
            "expected": "前端展示、服务端状态、数据库字段保持一致",
        },
    ]

    if "月卡" in requirement:
        test_cases.append(
            {
                "id": "TC-004",
                "title": "月卡重复购买有效期验证",
                "precondition": "账号已拥有未过期月卡",
                "steps": "再次购买同类型月卡，查看有效期变化和每日奖励状态",
                "expected": "有效期按规则延长，每日奖励状态不重置或异常丢失",
            }
        )

    if "支付" in requirement or "充值" in requirement:
        test_cases.append(
            {
                "id": "TC-005",
                "title": "支付回调与补单验证",
                "precondition": "准备正常支付、支付失败、回调延迟等支付环境",
                "steps": "分别触发支付成功、取消、失败和回调延迟，检查订单与发货状态",
                "expected": "订单状态流转正确，支付成功后奖励到账，失败或取消不发货，补单流程可追踪",
            }
        )

    boundary_cases = [
        "用户余额不足或支付中断时，订单状态应保持一致",
        "重复点击、重复请求、网络重连后不应重复发放奖励",
        "跨天、跨月、服务器时间变化时，有效期计算应正确",
        "客户端显示、服务端数据和数据库记录应一致",
    ]

    risks = [
        "支付回调延迟可能导致到账状态不一致",
        "重复购买可能造成有效期覆盖而不是累加",
        "配置表错误可能导致商品价格或奖励异常",
        "海外渠道或地区配置差异可能导致发布后问题",
    ]

    regression_suggestions = [
        "回归商城入口、商品详情、购买确认、支付结果页",
        "校验订单表、用户资产表、月卡有效期字段",
        "覆盖 Android / iOS、正式包 / 测试包、不同渠道包",
        "补充失败重试、补单、退款或取消支付场景",
    ]

    return TestPlan(
        requirement=requirement,
        functional_points=functional_points,
        test_cases=test_cases,
        boundary_cases=boundary_cases,
        risks=risks,
        regression_suggestions=regression_suggestions,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate QA test ideas from a requirement document.")
    parser.add_argument("requirement", nargs="*", help="需求文本。如果传入 --file，则这里可省略。")
    parser.add_argument("--file", "-f", help="从需求文档读取文本，支持 .txt / .md。")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="输出格式。")
    return parser.parse_args()


def read_requirement(args: argparse.Namespace) -> str:
    if args.file:
        return Path(args.file).read_text(encoding="utf-8").strip()

    return " ".join(args.requirement).strip() or DEFAULT_REQUIREMENT


def print_section(title: str, items: list[str]) -> None:
    print(f"\n## {title}")
    for index, item in enumerate(items, start=1):
        print(f"{index}. {item}")


def print_test_cases(test_cases: list[dict[str, str]]) -> None:
    print("\n## 测试用例")
    for case in test_cases:
        print(f"\n### {case['id']} {case['title']}")
        print(f"- 前置条件：{case['precondition']}")
        print(f"- 操作步骤：{case['steps']}")
        print(f"- 预期结果：{case['expected']}")


def main() -> None:
    args = parse_args()
    plan = generate_test_plan(read_requirement(args))

    if args.format == "json":
        print(json.dumps(asdict(plan), ensure_ascii=False, indent=2))
        return

    print("# 测试用例生成 Agent Demo")
    print(f"\n需求：{plan.requirement}")
    print_section("功能测试点", plan.functional_points)
    print_test_cases(plan.test_cases)
    print_section("边界场景", plan.boundary_cases)
    print_section("风险清单", plan.risks)
    print_section("回归建议", plan.regression_suggestions)


if __name__ == "__main__":
    main()
