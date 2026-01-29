# Virtual Patient Training App

Streamlit app for massage therapy student training. Students work through patient cases: interview → assessments → treatment planning → home care → ongoing plan → feedback.

## Architecture

- `app.py` - main Streamlit app, stage routing, AI integration
- `cases/` - patient cases as individual .py files exporting `CASE` dict
- Case loader dynamically imports all cases from `cases/` folder

## Case Structure

Each case file exports a `CASE` dict with:
- `id`, `name`, `summary`, `avatar` - display info
- `intake` - patient intake form data
- `details` - full case info (fed to AI as system prompt)
- `assessments` - ROM tests, special tests, other tests with results
- `feedback_criteria` - rubric for AI evaluation

## Adding New Cases

1. Create `cases/new_case.py`
2. Export `CASE` dict following `tennis_elbow.py` structure
3. App auto-loads it

## Key Files

- `Notes for Revisions.md` - design decisions, program flow
- `Feature Feedback.md` - testing feedback log

## Tech

- Streamlit for UI
- Anthropic API (claude-sonnet-4-5-20250929) for patient sim + evaluation
- API key in `.streamlit/secrets.toml`
