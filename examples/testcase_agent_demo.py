#!/usr/bin/env python3
"""A small local demo for turning a feature request into QA test ideas.

This demo does not call an LLM yet. It keeps the repository runnable without
API keys and shows the workflow that can later be replaced by an AI Agent.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass


DEFAULT_REQUIREMENT = "商城支持购买月卡，支付成功后立即发放奖励，重复购买需要延长有效期"


@dataclass
class TestPlan:
    requirement: str
    functional_points: list[str]
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
        boundary_cases=boundary_cases,
        risks=risks,
        regression_suggestions=regression_suggestions,
    )


def print_section(title: str, items: list[str]) -> None:
    print(f"\n## {title}")
    for index, item in enumerate(items, start=1):
        print(f"{index}. {item}")


def main() -> None:
    requirement = " ".join(sys.argv[1:]).strip() or DEFAULT_REQUIREMENT
    plan = generate_test_plan(requirement)

    print("# 测试用例生成 Agent Demo")
    print(f"\n需求：{plan.requirement}")
    print_section("功能测试点", plan.functional_points)
    print_section("边界场景", plan.boundary_cases)
    print_section("风险清单", plan.risks)
    print_section("回归建议", plan.regression_suggestions)


if __name__ == "__main__":
    main()
