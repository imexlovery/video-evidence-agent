# P0-B transcript retrieval answer prompt v1

你正在回答一个中文技术视频问题。你只能使用当前问题和当前提供的
character 2–4 gram TF-IDF Top-5 `VideoSegment`。不得读取完整 transcript、
Gold、答案要点、其他问题、其他结果或外部知识。

请返回且只返回一个 JSON 对象，键必须严格为：

```json
{
  "status": "ANSWERED" 或 "INSUFFICIENT_EVIDENCE",
  "answer": "简洁中文答案或 null",
  "citation_segment_ids": ["当前 Top-5 中的 segment_id"]
}
```

只有当前 Top-5 足以支持答案时才返回 `ANSWERED`，并且每个引用 ID 都必须
来自当前 Top-5。证据不足、问题询问当前片段未提供的事实，或无法可靠回答时，
返回：

```json
{
  "status": "INSUFFICIENT_EVIDENCE",
  "answer": null,
  "citation_segment_ids": []
}
```

引用的原文、时间戳和最终引用结构由程序从当前源 `VideoSegment` 回填；不要
自行编造 quote 或时间边界。
