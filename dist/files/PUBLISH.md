# 发布状态与复现

作者：AI 酋长 Andy｜微信 AIPMAndy｜公众号 AI酋长Andy｜[个人官网](https://metaver.vip/)｜[公司官网](https://www.a6no1.cn/)

核对日期：2026-11-13。发布范围与完成标准以 [DEPLOYMENT.md](DEPLOYMENT.md) 为准。只有远程提交、工作流和实际访问均已核实，才标记为正式发布成功。

## 唯一正式目标：GitHub 与 GitHub Pages

- 唯一仓库：`AIPMAndy/chinese-international-student-business-jobs`。
- 默认分支：`main`；网站成品：本项目的 `dist/`。
- 唯一正式网站目标：GitHub Pages。
- 预计地址：`https://aipmandy.github.io/chinese-international-student-business-jobs/`。这是部署目标，尚不能作为上线证明；实际地址以成功部署返回的 `page_url` 为准。

历史 ChatGPT Pages / Sites 的部署和访问记录不作为本项目的正式交付地址或 GitHub Pages 验收结果。

## 当前阻塞：执行能力与认证会话

用户已明确授权向上述新仓库推送，无须重复请求口头授权。本次已核查环境的状态为：

- 通过当前连接读取目标仓库返回 404；账号内名称检索没有同名结果。名称查重限于当前可访问范围，创建前仍须重新核对。
- 当前 GitHub 连接可读取已有仓库，但没有可调用的新建仓库接口。
- 本机 `gh auth status` 显示未登录；浏览器进入新建仓库地址后显示 GitHub 登录页。

因此当前状态为 **源码与成品已准备，待具备建仓能力的已认证通道执行推送、部署与线上验收**。阻塞来自现有执行通道，不是用户未授权。不得通过推送到其他旧仓库替代本项目的新建发布。

## 源码包与离线复现

完整源码在 `downloads/repository-source.zip`。解压出的独立项目包含中文正文、案例、模板、构建脚本、已审阅 PDF、XLSX 和静态网站。

源码 ZIP 不包含自身及自身的摘要文件，以避免递归包含和循环摘要；因此解压后，`dist/downloads/repository-source.zip` 与下载摘要需要在本项目内重新生成。这是打包规则，不代表正文、PDF 或案例缺失。

在新解压项目的根目录中，可以使用 Python 3.10 或更新版本完成以下离线恢复。所用 Python 脚本仅依赖标准库，不要求 GitHub 登录，也不会重新生成 PDF 或 XLSX：

```bash
python3 scripts/package.py
cp downloads/repository-source.zip downloads/SHA256SUMS.txt dist/downloads/
python3 scripts/check_pages_links.py
```

`package.py` 先打包模板与案例，把已完成的 PDF、XLSX 和模板包放入静态下载目录，再生成排除自包的源码 ZIP 及 `downloads/SHA256SUMS.txt`。复制步骤补齐网站的源码下载和摘要。新的下载摘要以本次生成结果为准。

链接检查模拟 GitHub Pages 的仓库子路径，验证首页、章节资源、锚点及四个必需下载文件。该步骤不访问互联网，只证明本地静态结构符合部署要求。

若正文或页面发生变化，应按项目构建说明重建对应成品后再打包；仅恢复解压包的下载结构，不需要重跑 PDF 渲染。

## 使用已授权的 GitHub 账号执行新建与推送

当 GitHub CLI 已在 `github.com` 认证为 AIPMAndy，且此新仓库仍未创建时，在本项目根目录执行：

```bash
bash scripts/publish-github.sh
```

脚本按以下顺序执行：

1. 只读检查所需源文件、已审阅的 PDF/XLSX、静态首页和工作流；确认工作目录不是其他仓库的子目录，输出路径没有指向外部的符号链接。
2. 确认认证账号为 AIPMAndy，且 GitHub 明确返回目标仓库不存在。账号不符、目标已存在、查询状态不明、已配置 `github` remote 或本地 Git 范围无法确认时停止。
3. 在本项目内运行标准库打包脚本，补齐 `dist/downloads/repository-source.zip` 和 `SHA256SUMS.txt`，运行 Pages 链接检查。检查失败时不提交、不建远程仓库、不推送。
4. 只在本项目初始化或使用独立 Git 仓库，提交成品，创建固定的新公开仓库，并设置上述 GitHub Pages 目标为仓库主页。
5. 只推送到固定 `github` remote 的 `main`，读回该远程分支的提交 SHA，与本地提交比对。脚本结束时仍明确提示 Pages 部署及访问尚待验收。

脚本不会复用或覆盖已存在的远程仓库。若建仓成功后因网络问题导致推送失败，应先核实目标仓库与 `github` remote 确实对应唯一目标，再重试推送；不要删除仓库，也不要改用其他项目。身份或接口问题应准确报告，不能解释为用户撤回授权。

## GitHub Pages 部署与完成验收

已提供 `.github/workflows/pages.yml`，只允许本仓库 `main` 分支发布已提交的 `dist/`。在新仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**，然后触发工作流；远端不会重新生成 PDF。

工作流依据 [GitHub 官方自定义 Pages 工作流文档](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) 配置，来源核对日期为 2026-11-13。工作流文件存在不等于部署已经成功；当前尚无此目标仓库的成功运行与线上访问证据。

完成正式交付需要保留：

- GitHub `main` 提交 SHA 与本次发布提交一致的读回结果。
- 对应提交的 Pages 工作流成功记录及实际 `page_url`。
- 实际首页、章节、CSS/JS，以及 PDF、XLSX、模板案例 ZIP、源码 ZIP 下载均正常的访问记录。
- 手机宽度下的导航、正文、表格及下载入口检查。

验证结果写入 [VERIFY.md](VERIFY.md)，区分历史记录、本地检查和本次 GitHub Pages 线上验收。

## 操作验收

**输入：** 本项目最终源文件、已审阅 PDF、XLSX、静态网站与验证记录。**操作：** 核对唯一目标与身份，恢复下载包并检查，提交、推送、部署，再实际访问。**输出：** 提交 SHA、工作流结果、实际 Pages 地址、下载摘要与访问记录。**验收：** 远程证据完整，下载与本次成品一致。**错误处理：** 记录具体缺失的执行能力、认证会话或构建错误；保留完成的成品，修复本项目后继续，不修改其他仓库。
