# 验证记录

版本：1.0｜核验日期：2026-11-13。作者：AI 酋长 Andy。

**完整内容、PDF、模板与网站已公开发布，GitHub Pages 部署及发布后 HTTP / SHA-256 验证已通过。** 以下分别保留内容检查、历史预览和本次正式网站的证据。

## 内容与来源

- 六个既有职业/商业项目只读查重，限定本项目增量；详见 [查重记录](research/DEDUP.md)。其他项目、个人主页、总导航和个人官网没有修改。
- 18 章主攻略、6 个独立职能入口、31 个地区条目；101 条来源记录、98 个唯一原始链接。
- 12 项地区资格规则独立复核；必要限定已合并，动态实施问题保留边界；详见 [事实复核](research/FACT-CHECK.md)。
- 六套完整教学模拟包含对应数据、操作、交付、验收、错误处理、参考解和评分。咨询与金融会计共 37 项计算检查通过，另四案脚本复算通过；20 份输入 CSV、96 行记录另有可打印数据页。
- 工作簿含 7 张工作表、7 个原生表格、23 个公式单元格。12 项计算与导出回读检查通过，公式错误扫描为 0；15 张预览均已实际查看。原生 Excel 桌面尚未测试。

## PDF 逐页验收

独立书册排版共 **180 页、39 个章节书签**。第一轮全书视觉检查后，已修复孤页、小表拆页、标题尾行和加粗标记。最终全部页面已渲染，文字越界扫描为 0。

最后一次修订仅调整第 2、180 页的正式网站与发布状态文字，两页已重新实际查看；其余 178 页与已逐页验收版本的整页 PNG 像素文件完全一致。完整审阅链见 `audit/pdf-review-final.json`、`audit/pdf-pages-label-map.json` 及引用记录。没有把机器扫描代替视觉审阅。

## 静态网站与下载包

- 已构建 53 个 HTML 页面，3,598 个内部引用和 117 个 Markdown 相对链接通过检查；提供职能筛选、全文搜索、目录、地区入口、案例及下载。相对链接、片段锚点、页面元信息、品牌链接、CSV/XLSX/ZIP 完整性与本地下载副本均由 `scripts/verify.py` 核对；具体计数见 `audit/static-validation.json`。
- `scripts/check_pages_links.py` 另按 GitHub Pages 的仓库子路径检查 HTML/CSS 引用、锚点和四项必需下载；报告见 `audit/github-pages-local-check.json`。该检查是离线模拟，不能证明已经部署。
- 源码 ZIP 避免递归，不包含它自己的 ZIP 副本。解压后发布脚本会重新打包并补齐 `dist/downloads/` 中的源码 ZIP 与校验摘要，再运行 Pages 检查；已按该步骤在独立临时目录实际解压、恢复并校验通过，见 `audit/archive-restore-check.json`；步骤见 [发布说明](PUBLISH.md)。
- 正文中的官网链接已加明确边界，修复中文标点被误包含进网址的问题。项目代码和页面表单不收集申请者简历或身份资料。

## 历史预览的浏览器验收

曾对预览副本实际访问首页、经营分析案例，测试职能筛选、全文搜索、微信复制、手机菜单与章节目录。四项预览下载已实际下载，均与当时部署版本的本地文件 SHA-256 一致。记录：`audit/site-preview-validation.json`。

桌面视口为 1363 × 936 CSS 像素；普通浏览器缩放形成 454 × 312、340 × 234 CSS 像素的窄视口，两种宽度均无页面横向溢出，宽表格在内部容器滚动。开发者工具受环境限制，未测试实体手机、触控或设备仿真。观测到的浏览器扩展错误已与站点脚本错误分开记录。

依据 [项目部署要求](DEPLOYMENT.md)，该预览不作为正式网站，不再继续发布。最终的官网链接修复、PDF 发布文字与重新打包的成品已在本地验证，未同步到该历史预览。不能将历史下载结果当作最终 GitHub Pages 下载验收。

## GitHub 与正式网站：已完成

唯一仓库：[AIPMAndy/chinese-international-student-business-jobs](https://github.com/AIPMAndy/chinese-international-student-business-jobs)。正式网站：[https://aipmandy.github.io/chinese-international-student-business-jobs/](https://aipmandy.github.io/chinese-international-student-business-jobs/)。

源码、PDF、工作簿、模板与案例包、静态网站均已推送至公开仓库。GitHub Pages 部署成功；本次发布后对首页、正文、CSS、JS、PDF、XLSX、模板 ZIP 和源码 ZIP 共 8 个实际 URL 检查，均返回 HTTP 200，且 SHA-256 与部署提交的 dist 文件一致。 [查看成功运行](https://github.com/AIPMAndy/chinese-international-student-business-jobs/actions/runs/43487152686)，对应提交 `dfb6ef5b37c2e50d506283d64886a7d85194c639`。该记录绑定此提交，后续更新以新的工作流结果为准。

此前 404 与未建仓状态是历史记录。本次远端校验确认 53 个 HTML、3,599 个引用及四份必需下载无错误。机器可读记录见 `audit/github-publication-status.json`；发布方法见 [PUBLISH.md](PUBLISH.md)。历史预览的手机测试不替代实体设备验收。

## 验收边界

- 官方网页会更新、岗位会关闭；研究样本不等于持续在招清单。脚本没有声称验证全部外部网页的实时可用性。
- 31 个地区入口深度不同，README 与各地区章逐项列出不足；不把局部样本外推成整个国家的招聘习惯。
- 所有案例与申请样例均为教学模拟，不是客户成果；评分不是雇主评分、通过率或 Offer 概率。
- 原生 Excel 桌面和实体手机尚未测试；GitHub Pages 工作流与本次线上文件检查已经执行并通过。

微信：AIPMAndy｜公众号：AI酋长Andy｜[个人官网](https://metaver.vip/)｜[公司官网](https://www.a6no1.cn/)
