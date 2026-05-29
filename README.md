# KubeBlocks Artifacts

KubeBlocks 相关素材仓库。先以图片为主，图片旁边放配套文案和生成提示词，方便同事继续补图、改图、写文章或做传播材料。

仓库地址：<https://github.com/apecloud/kubeblocks-artifacts>

## 目录结构

```text
gallery/
  kubeblocks-intro/
    image.png          # 单张介绍图
    copy.md            # 配套文案
    prompt.md          # 生成提示词

  kubeblocks-website-series/
    contact-sheet.png  # 10 张图总览
    01-*.png           # 单张图片
    01-*.md            # 同名文案
    prompts.md         # 全部生成提示词
    topics.md          # 选题来源

  apemind-chunk-flow/
    image.png
    copy.md
    prompt.md

docs/
  xiaohei-generation-guide.md
```

这个结构的原则很简单：**图片和文案放在一起**。以后要加新素材，就在 `gallery/` 下建一个主题目录，把图片、文案、提示词放进去。

## 当前素材

### KubeBlocks 单图介绍

路径：`gallery/kubeblocks-intro/`

用“总控台”隐喻解释 KubeBlocks：在 Kubernetes 上，把多种数据库的备份、扩缩、故障切换和统一 API 收到一套控制里。

### KubeBlocks 官网主题 10 图

路径：`gallery/kubeblocks-website-series/`

基于 <https://kubeblocks.io/> 公开内容整理，覆盖：

1. 统一控制
2. 收束 Operator
3. 现代数据栈
4. Day-2 运维
5. 备份恢复
6. 可观测
7. 生命周期自动化
8. GitOps / IaC
9. Addon 接入
10. 生产规模

### ApeMind chunk 流程图

路径：`gallery/apemind-chunk-flow/`

这是小黑风格试验图，用“文档切片机”隐喻解释企业文档被解析、切块、进入统一知识片段库，再被语义检索、关键词检索和引用回答复用。

## 小黑风格来源

本仓库第一批图片参考了 Ian Xiaohei Illustrations：

<https://github.com/helloianneo/ian-xiaohei-illustrations>

这是一套 Codex Skill，适合生成 16:9 白底手绘中文正文配图。它的关键特征：

- 纯白背景
- 黑色手绘线稿
- 大量留白
- 少量红、橙、蓝中文短批注
- 小黑必须参与核心动作
- 不做正式架构图或 PPT 信息图

如果要继续生成同风格插画，先看：

- `docs/xiaohei-generation-guide.md`
- 已有主题目录里的 `prompt.md` / `prompts.md`

## 新增素材规范

建议每个新主题都这样放：

```text
gallery/<主题名>/
  image.png
  copy.md
  prompt.md
```

如果是一组图：

```text
gallery/<主题名>/
  contact-sheet.png
  01-xxx.png
  01-xxx.md
  02-xxx.png
  02-xxx.md
  prompts.md
  topics.md
```

文案建议写清楚：

- 这张图讲什么
- 适合放在哪里
- 图里哪些元素分别代表什么
- 生成或改图时要注意什么

## 公共仓库注意事项

这个仓库是 public 可见。提交前请确认：

- 没有内部账号、密钥、私有环境地址。
- 没有客户敏感信息。
- 没有未公开路线图或私有商业承诺。
- 图片里的品牌名、产品名和数字来自公开资料或已经确认可公开使用。

除非另有说明，仓库中的素材用于 ApeCloud / KubeBlocks 相关内容制作与团队协作。对外二次使用前请按公司口径确认。
