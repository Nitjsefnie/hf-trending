> **Archived 2026-10-12.** The Hugging Face trending tracker now lives in
> [Nitjsefnie/ai-researcher](https://github.com/Nitjsefnie/ai-researcher)
> (workflow `hf-trending.yml`, ai-researcher#256). This repository's history is
> kept read-only as the record up to that point.

# hf-trending

Hugging Face's top 10 trending models — just the model ids, in Hugging
Face's order (`https://huggingface.co/api/models?sort=trendingScore&limit=10`),
fetched every hour into [`trending.json`](trending.json). Each data commit
announces what moved: models new to the top 10, models that left it, and
rank changes, so `git log` is the history.

Run by [`update.py`](update.py) from the hourly `update` workflow.
