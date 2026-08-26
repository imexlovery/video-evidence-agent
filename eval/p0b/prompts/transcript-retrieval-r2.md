# P0-B transcript retrieval answer prompt v2

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

仅当当前 Top-5 足以支持问题所要求的事实时才返回 `ANSWERED`。答案只能覆盖
当前证据明确支持的内容；问题要求多个要点时，不能用一个已支持的部分代替缺失
的部分，也不能依据常识补齐。每个引用 ID 都必须来自当前 Top-5。

如果证据只表示“没有披露”“不方便透露”“不知道确切值”，或者没有给出问题
所要求的确切数字、日期、规模等事实，必须返回：

```json
{
  "status": "INSUFFICIENT_EVIDENCE",
  "answer": null,
  "citation_segment_ids": []
}
```

拒答时不要把“未披露”改写成猜测，也不要引用只证明“没有确切答案”的片段来
伪装成已回答。引用的原文、时间戳和最终引用结构由程序从当前源
`VideoSegment` 回填；不要自行编造 quote 或时间边界。
