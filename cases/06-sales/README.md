# 案例 06：哪些商机值得推进，价值该怎样算？

**教学模拟。** 账户名称、需求、预算状态、金额和概率全部为合成数据，不是真实客户，也不代表任何公司招聘题。不得联系这些虚构账户。金额为 CU。版本日期：2026-11-13。

## 任务与输入

你在演练中负责一家虚构订单管理软件的销售推进。软件支持订单录入、状态跟踪和基础报表，不支持工资结算；外部系统集成必须进一步验证。Aster 的示例报价为每年 12,000、一次实施 2,000 CU。其他管线金额是题设记录，不代表已批准的真实报价。所有机会目前均未签约。

输入：[accounts.csv](accounts.csv)、[pipeline.csv](pipeline.csv)、[value_assumptions.csv](value_assumptions.csv)、[discovery_template.md](discovery_template.md)。表中每行分别是一个账户、一项机会或一个假设。机会表概率为作者指定的教学假设，未使用真实历史校准。金额口径是年度合同额，不是当季会计收入。

Aster 有 20 人，每人每周用 2 小时重复录单，一年工作 48 周，每小时容量价值假设为 25 CU。基准情景只兑现 60% 的可释放容量，保守情景 20%。这不是公司已经减少的现金支出。初始待验证假设还包括使用率、流程变化和培训投入。

## 操作与交付

输入：账户事实、未确认项、产品边界与机会记录。

操作：安排本周两次重点会议并说明优先级；写 8 个需求发现问题；算 Aster 的价值情景；清理不合格机会；写一次跟进邮件和下一步计划。

输出：账户卡、发现纪要、价值表、管线汇总和五分钟演示。建议训练时限 75 分钟，另加 15 分钟角色演练。

验收：事实与假设分开，未知预算保留未知，不承诺产品未验证的功能。年度合同额、加权管线、已签合同与收入分开表述。

错误处理：客户需求超出产品能力时，承认不适配或转交评估；关键人、预算或时间未知时，不凭兴趣打高概率。练习不需要真实触达、抓取个人信息或群发邮件。

## 参考答案一：分配有限时间

Birch 希望自动处理工资，而题设产品不支持，应从合格商机中移出，记录原因。不能为了达成管线目标把它留在合格总额中。

若你是推进现有机会的 AE，本周两次重点会议可给 Dune 与 Cedar：Dune 仍需确认合同、审批、采购时间与现有供应商切换条件；Cedar 需要技术人员与业务方一起验证集成，未经验证不能承诺。Aster 安排后续需求发现，先补预算和决策流程。若岗位是 SDR，优先研究 Aster 并将已在 AE 阶段的 Cedar/Dune 协同转交，也是合理答案。评分看角色一致性和证据，不要求机械照抄排序。

## 参考答案二：八个需求发现问题

1. 请走一遍最近一次从收到订单到录入系统的过程。
2. 哪个步骤最容易重复或出错？最近一次产生了什么影响？
3. 每周耗时的估计来自哪里，能否抽样核对？
4. 如果释放这些时间，团队会实际减少费用，还是处理更多订单？
5. 哪些系统必须连接，谁负责验证兼容性？
6. 使用者、预算负责人、最终审批人分别是谁？
7. 这项改变与其他项目相比有多优先，采购时间怎样决定？
8. 什么样的小试点能帮助你们决定继续，谁在什么时候看结果？

问题顺序可以随对话调整。对方不愿回答时，说明为什么需要信息，不用压力话术。记录“未知”比编造答案更有用。

## 参考答案三：价值情景

全年人工处理时间为 `20 × 2 × 48 = 1,920 小时`；对应容量价值 `1,920 × 25 = 48,000 CU`。首年软件与实施费用为 `12,000 + 2,000 = 14,000 CU`。

| 情景 | 可兑现容量价值 | 减首年费用后的情景价值 |
| --- | --- | --- |
| 基准 60% | 48,000 × 60% = 28,800 | 14,800 CU |
| 保守 20% | 48,000 × 20% = 9,600 | -4,400 CU |

仅按题设成本，收支临界兑现比例为 `14,000 / 48,000 = 29.17%`。真实判断还需计入培训、内部实施、数据迁移、维护与风险等遗漏成本。即使情景价值为正，也不能声称必然为客户节省同额现金。建议先测真实基线与试点后变化，确认释放工时如何转成客户认可的价值。

## 参考答案四：清理销售管线

原始年度合同额记录合计 `12,000 + 18,000 + 24,000 + 10,000 = 64,000 CU`。移除不合格 Birch 后，合格机会为 46,000 CU。

用题设阶段概率计算：`12,000 × 0.4 + 24,000 × 0.6 + 10,000 × 0.8 = 27,200 CU`。假设季度目标以年度合同额计为 100,000，则合格未加权覆盖为 0.46 倍，概率加权为 0.272 倍。

这些数值是教学汇总，不是承诺成交或收入预测。真实预测要检查概率是否校准、机会是否相关、采购期是否匹配和下一步是否有客户确认。Dune 仍未签约，所以不能把它作为已完成业绩。

## 跟进邮件示例

这是对角色演练的示例文字，未发送给任何人：

“感谢今天的讨论。我的理解是，团队希望减少重复录单，同时保持现有订单流程稳定。我们仍需核对每周耗时、集成要求和审批流程。如果您认可，下一步可以由运营同事提供一份脱敏流程样本，我们与技术同事共同确认试点范围，再讨论是否值得继续。时间与参与人以双方确认为准。”

English version: “Thank you for the discussion. My understanding is that your team wants to reduce duplicate order entry without disrupting the current workflow. We still need to validate the time baseline, integration requirements and approval process. If useful, the next step could be a review of an anonymized workflow sample with your operations team and our technical colleague, followed by agreement on a limited pilot.”

## 评分标准（100 分）

| 项目 | 分值 | 得分依据 |
| --- | --- | --- |
| 账户选择与适配 | 20 | 能移除不适合机会；优先级与角色一致 |
| 需求发现 | 25 | 提问能验证问题、影响、决策与下一步 |
| 价值计算与边界 | 20 | 算式正确，区分容量价值与现金节约 |
| 管线纪律 | 20 | 口径正确；不把概率或未签机会当收入 |
| 表达与跟进 | 15 | 简洁准确，有责任和待确认项，不制造承诺 |

70 分表示主要训练完成；85 分以上表示判断与表达较完整。它不是成交概率或招聘评分。虚构客户回答、预算或业绩须先更正再评分。

## 面试追问

如果客户说“太贵”，你先问什么？如果只有使用者愿意见你而审批人未参与，怎样推进？如果竞争者便宜一半，哪些价值假设需要重算？如果试点没有节省时间，你如何决定停止？如果经理要求把所有机会都填到 80%，你会怎样呈现真实记录？

## 中英文申请样例

完成后可写：“个人 B2B 销售练习（教学模拟）：研究四个虚构账户，设计需求发现问题，按产品适配性清理管线，并测算容量价值与首年费用的敏感性。全部为模拟，未发生真实客户触达或成交。”

English project bullet: “Independent B2B sales simulation: researched four fictional accounts, designed discovery questions, removed a poor-fit opportunity, and tested a value hypothesis against first-year cost. No real customer outreach, signed contract or revenue.”

中文申请段落：“我希望从初级销售开发或相关商业岗位起步。练习展示了我如何研究客户、确认需求、承认不适配并记录下一步。我目前没有可证明的真实成交业绩，因此没有将模拟管线写成收入，希望进一步学习贵团队的资格标准与客户协作方式。”

English application excerpt: “I am seeking an early-career sales-development role. My attached simulation shows account research, discovery, qualification and disciplined follow-up. I do not present simulated pipeline as sales results, and I would be keen to learn your team's qualification standards and customer processes.”

作者：AI 酋长 Andy。微信 AIPMAndy；公众号 AI酋长Andy；<https://metaver.vip/>；<https://www.a6no1.cn/>。
