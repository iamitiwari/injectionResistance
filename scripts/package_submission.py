"""Package the requested three environments and sanitized evidence."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

project = Path(__file__).resolve().parents[1]
release = project / 'submission/seed3-5-calibrated'
assert not release.exists(), 'Release already exists; inspect it before replacing.'
release.mkdir(parents=True)
# Read configured values solely to redact them. Never print their contents.
secrets = []
for line in (project / '.env').read_text().splitlines():
    stripped = line.strip()
    if stripped and not stripped.startswith('#') and '=' in stripped:
        key, value = stripped.removeprefix('export ').split('=', 1)
        value = value.strip().strip('"').strip("'")
        if len(value) >= 8:
            secrets.append((value.encode(), ('[REDACTED_' + key.strip() + ']').encode()))

def copy_file(source, target, adapt=False):
    data = source.read_bytes()
    for value, replacement in secrets:
        data = data.replace(value, replacement)
    if adapt:
        data = data.replace(b"'rles/", b"'environments/")
    data = data.replace(b'/home/amit/injectionResistance/jobs/', b'results/')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    target.chmod(source.stat().st_mode & 0o777)

names = ['seed3_handoff_billing', 'seed4_review_bot', 'seed5_review_bot_neutral']
model_jobs = {'seed3_handoff_billing': 'handoff-rotation', 'seed4_review_bot': 'review-waiver-six-trials',
              'seed5_review_bot_neutral': 'neutral-waiver-six-trials'}
summary = []
for name in names:
    for source in (project / 'rles' / name).rglob('*'):
        if source.is_file() and '__pycache__' not in source.parts and source.suffix != '.pyc':
            copy_file(source, release / 'environments' / name / source.relative_to(project / 'rles' / name))
    oracle = list((project / 'jobs' / name / 'safe-reference').glob('*/verifier/result.json'))
    assert len(oracle) == 1
    copy_file(oracle[0], release / 'environments' / name / 'result.json')
    copy_file(oracle[0].with_name('reward.txt'), release / 'environments' / name / 'reward.txt')
    for source in (project / 'jobs' / name).rglob('*'):
        if source.is_file() and source.name != '.env' and '__pycache__' not in source.parts:
            copy_file(source, release / 'results' / name / source.relative_to(project / 'jobs' / name))
    trials = []
    for source in sorted((project / 'jobs' / name / model_jobs[name]).glob('*/verifier/result.json')):
        verdict = json.loads(source.read_text())
        trials.append({'trial': source.parent.parent.name, 'task_completed': verdict['task']['task_completed'],
                       'safety_violation': verdict['safety']['safety_violation'], 'reward': verdict['reward']})
    expected = 2 if name == 'seed3_handoff_billing' else 6
    assert len(trials) == expected, (name, len(trials))
    score = {'environment': name, 'reported_job': model_jobs[name], 'trials': len(trials),
             'task_completions': sum(t['task_completed'] for t in trials),
             'safety_violations': sum(t['safety_violation'] for t in trials), 'trial_scores': trials,
             'top_level_environment_verdict': 'safe oracle validation, not model rollout'}
    (release / 'results' / name / 'score.json').write_text(json.dumps(score, indent=2) + '\n')
    summary.append(score)
(release / 'results/scores.json').write_text(json.dumps(summary, indent=2) + '\n')
status = {'package_prepared': True, 'form_submitted': False, 'reason': 'Submission form URL and required fields were not provided.', 'deadline': '2026-10-10 09:00 Asia/Kolkata', 'deadline_passed_before_work_began': True}
(release / 'SUBMISSION_STATUS.json').write_text(json.dumps(status, indent=2) + '\n')
for name in ['README.md', 'QUALITY_BAR.md']:
    copy_file(project / name, release / name)
for source in (project / 'docs').glob('seed[345]*'):
    if source.is_file():
        copy_file(source, release / 'docs' / source.name)
for name in ['validate_seed3.py', 'validate_seed4.py', 'validate_seed5.py', 'analyze_review_rollout.py']:
    copy_file(project / 'scripts' / name, release / 'scripts' / name, adapt=True)
# Check the released task comparison separately; added oracle files are not source.
a = release / 'environments/seed4_review_bot'
b = release / 'environments/seed5_review_bot_neutral'
differences = []
for source in (project / 'rles/seed4_review_bot').rglob('*'):
    if source.is_file() and '__pycache__' not in source.parts and source.suffix != '.pyc':
        relative = source.relative_to(project / 'rles/seed4_review_bot')
        if (a / relative).read_bytes() != (b / relative).read_bytes():
            differences.append(str(relative))
assert differences == ['environment/review-bot']
manifest = {}
for source in release.rglob('*'):
    if source.is_file():
        data = source.read_bytes()
        assert all(value not in data for value, _ in secrets), 'Unredacted configured value in release'
        manifest[str(source.relative_to(release))] = hashlib.sha256(data).hexdigest()
(release / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
archive = project / 'submission/seed3-5-calibrated.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as output:
    for source in sorted(release.rglob('*')):
        if source.is_file():
            output.write(source, source.relative_to(release.parent))
with zipfile.ZipFile(archive) as output:
    assert output.testzip() is None
print('Package:', archive)
print('Files:', len(manifest) + 1, 'Archive bytes:', archive.stat().st_size)
print('Configured values absent from all release files; original workspace logs unchanged.')
