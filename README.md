# 开发指南

为确保大家顺利地参与开发、提交代码和保持良好的协作流程，请务必阅读以下说明。

---

## 🔧 环境准备

### 1. 安装 Git

#### Windows
1. 访问 [Git 官网](https://git-scm.com/download/win) 下载并安装。
2. 安装时一路默认即可，推荐使用 Git Bash 作为命令行工具。

## 🧩 Git 配置（首次使用）

打开终端（Terminal 或 Git Bash），执行以下命令设置用户名和邮箱：

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

⚠️ 这两个值将出现在你的提交记录中。邮箱和github账号使用的相同。

---

## 🗃️ 克隆项目（首次下载项目）

```bash
git https://github.com/HelloWorldZTR/Vocabual.git
cd Vocabual
code .
```

或在 VS Code 中使用 `Ctrl + Shift + P` → 输入 `Git: Clone` → 粘贴仓库地址。

---

## 🔄 日常工作流程

请**不要直接在主分支 `main` 上开发**，每个人请使用**独立分支**进行开发。

### 1. 同步远程代码（每次开发前）

在终端中执行：

```bash
git pull origin main
```

或者在 VS Code 左侧源代码管理面板中点击“刷新”按钮。

![alt text](imgs/image.png)

### 2. 创建并切换到新分支

在终端中执行：

```bash
git checkout -b your-name/feature-name
```

也可以在 VS Code 左下角点击当前分支名 → 输入新分支名并回车。

![alt text](imgs/image-1.png)

---

## ✍️ 在 VS Code 中提交和推送修改

### 1. 打开 Git 面板

![alt text](imgs/image-2.png)

点击左侧活动栏中的 **源代码管理图标**（看起来像个 Y 字），或者使用快捷键：

```
Ctrl + Shift + G 
```

### 2. 查看修改文件

已修改的文件会显示在列表中。你可以右键 → `暂存更改`，或者点击文件名前的 `+` 图标。

### 3. 输入提交信息

在上方的“消息”框中写下本次提交的说明，例如：

```
添加登录组件
```

然后点击 ✓ 按钮进行提交。

### 4. 推送到远程分支

点击右上角的三点菜单 `...` → 选择 `Push`（推送）。  
首次推送新分支时，可能需要选择 `Push to...` → 远程分支名。

---

## 开发流程

如何开发UI， 以编辑recite界面为例

1. `recite.ui` 右键, `PYQT: Edit in Designer`
1. 在designer内完成页面编辑，`ctrl + s` 保存
1. `recite.ui` 右键, `PYQT: Compile Form`
1. 在`recite.ui`中，完成对应的槽函数的设置，并加入一些交互逻辑

如果需要大量使用`qfluentwidgets`组件建议直接手写，以`staticsFrame`为例

