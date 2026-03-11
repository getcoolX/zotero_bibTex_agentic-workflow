# Zotero BibTeX Agentic Workflow

一个带前端页面的文献工作流：

- 导入文献：支持一次输入多篇论文信息（标题 / DOI / URL）
- 管理文献：查看与勾选文献
- 导入 Zotero：网页端管理 Zotero 参数并执行导入
- 导出引用：将选中文献导出为 ACM 风格 BibTeX（LaTeX）
- LLM 管理：内置 OpenAI / DeepSeek / Gemini / Qwen 配置模板，可在前端维护 API Key 和启用状态

## 运行

```bash
python app.py
```

打开 `http://localhost:8080`
