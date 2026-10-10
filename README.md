# hf-trending

Hugging Face's top 10 trending models — just the model ids, in Hugging
Face's order (`https://huggingface.co/api/models?sort=trendingScore&limit=10`),
fetched every hour into [`trending.json`](trending.json). Each data commit
announces what moved: models new to the top 10, models that left it, and
rank changes, so `git log` is the history.

Run by [`update.py`](update.py) from the hourly `update` workflow.
