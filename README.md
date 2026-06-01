# 基于 Grover 搜索的量子强化学习算法介绍

本项目是武汉大学《量子信息与量子计算基础》结课作业，使用 Manim 制作视频动画，主题为：

- 经典强化学习中的动作选择瓶颈
- 量子叠加与 Grover 搜索如何加速动作搜索
- 与 TD / SARSA / Q-Learning 的结合思路

## 目录结构

- demo1.py ~ demo10.py: 各章节动画脚本

## 一、环境配置（Windows 本地）

### 1. 安装基础工具

请先安装：
- Miniconda 或 Anaconda
- FFmpeg
- MiKTeX 或 TeX Live（用于 MathTex / LaTeX 公式渲染）
说明：
- 如果没有 FFmpeg，Manim 无法正常编码输出视频。
- 如果没有 LaTeX 发行版，含公式的场景可能报错。

### 2. 创建并激活 Conda 环境

在项目根目录打开 PowerShell：

```powershell
conda create -n Manim python=3.10 -y
conda activate Manim
```

### 3. 安装 Manim 与依赖

```powershell
pip install -U pip
pip install manim numpy
```

验证安装：

```powershell
manim --version
```

如果能显示版本号，说明安装成功。

## 二、如何在本地生成视频

### 1. 渲染单个场景

命令格式：

```powershell
manim -pql <脚本名.py> <场景类名>
```

参数说明：

- -p: 渲染后自动预览
- -ql: 低清快速预览（开发调试推荐）

示例：

```powershell
manim -pql demo10.py FinalSummaryCredits
```

### 2. 更高质量导出

中等质量：

```powershell
manim -pqm demo10.py FinalSummaryCredits
```

高质量：

```powershell
manim -pqh demo10.py FinalSummaryCredits
```

### 3. 批量渲染各章节

你可以按章节顺序执行：

```powershell
manim -pql demo1.py OpeningGridworld
manim -pql demo2.py MonteCarloIntroLong
manim -pql demo3.py TDLearningIntro
manim -pql demo4.py SarsaQLearningCompare
manim -pql demo5.py ClassicalBottleneck
```

其余章节同理：

```powershell
manim -pql demo6.py <SceneName>
manim -pql demo7.py <SceneName>
manim -pql demo8.py <SceneName>
manim -pql demo9.py <SceneName>
manim -pql demo10.py FinalSummaryCredits
```

提示：demo6~demo9 的具体场景类名请在对应 .py 文件中查看 class 定义。

## 三、输出文件位置

Manim 默认输出到：

- media/videos/<脚本名>/<分辨率目录>/

例如：

- media/videos/demo10/480p15/

最终 mp4 会在对应目录下生成。

## 四、常见问题

### 1. manim 命令找不到

- 确认已执行 conda activate Manim
- 在当前环境重新安装 manim: pip install manim

### 2. 公式渲染报错（LaTeX 相关）

- 安装 MiKTeX 或 TeX Live
- 安装后重开终端再试

### 3. 中文字体显示异常

本项目默认使用 SimSun。若系统缺少该字体，可将脚本中的：

- font_cn = "SimSun"

替换为系统可用中文字体（如 微软雅黑 等）。

### 4. 渲染速度慢

- 开发阶段优先用 -ql
- 仅在最终导出时使用 -qm / -qh
