<div align="center">
  <h1>ReposSync</h1>
  <span><a href="./README.md">English</a> | 中文</span>
</div>

## ⚡ 简介

**ReposSync是一个仓库批量同步工具，具有以下特点：**

- 轻量级使用：仅需配置一个Github Token和仓库列表即可使用。
- 兼容性：支持多个源端同步到Github，简化配置和调度。
- 批量同步：支持将多个源仓库同步到目标仓库。

## 🚀 快速开始

```sh
pip install -r requirements.txt
```

### 配置

1. 复制一个 `.env.example` 文件为 `.env`
2. 登录到你的 GitHub 账户，进入 GitHub Settings。
3. 点击 "Developer settings" -> "Personal access tokens" -> "Tokens (classic)" -> "Generate new token"。
4. 选择所需的权限：`repo`，生成一个令牌并保存好它。
5. 编辑 `.env` 文件，配置你的Github Token
6. 编辑 `repos.yaml` 文件

```yaml
source:
  plat_url: https://git.xxx.com # 源端仓库地址
  username: skylertong # 源端仓库用户名
dest:
  plat_url: https://github.com # 目的端仓库地址
  username: t8y2 # 目的端仓库用户名
base_dir: D:\\testrepos # 本地仓库存放路径
repo_list:
  - source_repo_name: repo-1 # 第1个源端仓库名称
    dest_repo_name: repo-1 # 第2个目的端仓库名称（可选字段，不填默认和源仓库名称一致）
    branch: main # 分支
    private: false # 是否为私有仓库（可选，默认为true即隐私仓库）
  - source_repo_name: repo-2 # 第2个源端仓库名称
    branch: main # 分支
```

### 运行ReposSync

```shell
python main.py
```
然后程序就会自动化运行了~

## ✔️ 运行截图

后面补充

## 💕 感谢 Star

项目获取 star 不易，如果你喜欢这个项目的话，欢迎支持一个 star！这是作者持续维护的唯一动力

## 🔨 后续开发计划
- [ ] 支持更多的源端平台和目标平台如Gitee\GitLab等
- [ ] 提供前端界面, 附加诸多仓库基础功能
- [ ] 源端仓库列表扫描
- [ ] 仓库批量删除功能
- [ ] 仓库批量重命名功能 

欢迎提交Issues和PR，感谢您的支持！
