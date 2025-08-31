# start python uv

使用 uv 代替 conda 管理第三方包

## 安装环境

### 使用 uv 管理 python 开发环境

<https://docs.astral.sh/uv/>

Windows 安装

```shell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

macOS 安装

```shell
brew install uv
```

基本操作

```shell
# 安装 Python（如果系统上存在 Python 不会重复安装）
uv python install 3.12

# 查看可用和已安装的 Python 版本：
uv python list

# 创建新项目（pyproject.toml）
uv init
uv init project_name

# 安装依赖包（-v 查看调试信息）
uv add httpx
uv add httpx --index-url https://pypi.tuna.tsinghua.edu.cn/simple
uv add httpx --default-index https://pypi.tuna.tsinghua.edu.cn/simple
uv add "httpx>=0.20"
uv add "httpx @ git+https://github.com/encode/httpx"
uv add "jax; sys_platform == 'linux'"
uv add -r requirements.txt

# 删除依赖包
uv remove httpx

# 锁定依赖包（创建或更新 uv.lock）
uv lock

# 升级依赖包
uv lock --upgrade
uv lock --upgrade-package httpx
uv lock --upgrade-package <package>==<version>

# 手动同步
uv sync

# 运行
uv run example.py
uv run -- flask run -p 3000

# 导出依赖包（兼容 pip）
uv export --format requirements-txt

# 打包（dist/ 源代码版和二进制版）
uv build
uv build --sdist
uv build --wheel
```
