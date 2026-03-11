# Zotero BibTeX Agentic Workflow

一个带前端页面的文献工作流：

- 导入文献：支持一次输入多篇论文信息（标题 / DOI / URL）
- 管理文献：查看与勾选文献
- 导入 Zotero：网页端管理 Zotero 参数并执行导入
- 导出引用：将选中文献导出为 ACM 风格 BibTeX（LaTeX）
- LLM 管理：内置 OpenAI / DeepSeek / Gemini / Qwen 配置模板，可在前端维护 API Key 和启用状态

## 配置说明（先 example，后 local）

仓库仅保留模板文件（不含真实密钥）：

- `config/llms.example.json`
- `config/zotero.example.json`

运行时真实配置使用本地文件：

- `config/llms.local.json`
- `config/zotero.local.json`

首次启动时，后端会在检测到 `.local.json` 不存在时自动从对应的 `.example.json` 复制初始化。
你也可以手动先复制：

```bash
cp config/llms.example.json config/llms.local.json
cp config/zotero.example.json config/zotero.local.json
```

然后打开页面填写 API key 并点击“保存配置”。

> `*.local.json` 已加入 `.gitignore`，不会进入版本库。

## 运行

```bash
python app.py
```

打开 `http://localhost:8080`
