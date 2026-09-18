#!/usr/bin/env python3
"""Validate the archived review against its named git baseline.

Use --current only to check an unchanged checkout against that historical review.
"""
import argparse
import collections
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
GROUPS = ('model-foundations', 'model-decisions', 'other-articles', 'presentation')


def read(name):
    return json.loads((HERE / name).read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current', action='store_true')
    args = parser.parse_args()
    manifest = read('manifest.json')
    units = {u['id']: u for u in manifest['units']}
    assert len(units) == len(manifest['units']), 'duplicate manifest unit'
    covered = collections.defaultdict(collections.Counter)
    for f in manifest['files']:
        content = ((ROOT / f['file']).read_bytes() if args.current else
                   subprocess.check_output(['git', 'show', f"{manifest['research_commit']}:{f['file']}"], cwd=ROOT))
        assert hashlib.sha256(content).hexdigest() == f['sha256'], f"source changed: {f['file']}"
        lines = content.decode().splitlines()
        subset = [u for u in units.values() if u['file'] == f['file']]
        assert len(subset) == f['units']
        for u in subset:
            text = '\n'.join(lines[u['start'] - 1:u['end']])
            assert text == u['text'], u['id']
            assert hashlib.sha256(text.encode()).hexdigest() == u['sha256'], u['id']
            covered[f['file']].update(range(u['start'], u['end'] + 1))
        assert all(covered[f['file']][n] == 1 for n, line in enumerate(lines, 1) if line.strip()), f['file']
        assert all(n == 1 for n in covered[f['file']].values()), f['file']
    ledgers, findings = [], []
    for group in GROUPS:
        ledger, items = read(group + '-ledger.json'), read(group + '-findings.json')
        expected = {u['id'] for u in read(group + '-input.json')}
        assert len(ledger) == len(expected) and {r['id'] for r in ledger} == expected, group
        ledgers.extend(ledger)
        findings.extend(items)
    assert len(ledgers) == len(units) and {r['id'] for r in ledgers} == set(units)
    assert len({f['id'] for f in findings}) == len(findings)
    fmap = {f['id']: f for f in findings}
    for row in ledgers:
        assert row['verdict'] in {'keep', 'copy_edit', 'clarify', 'verify', 'restructure'}, row['id']
        assert len(row['reason']) >= 10, row['id']
        assert row['verdict'] == 'keep' or row['finding_ids'], row['id']
        for fid in row['finding_ids']:
            assert fid in fmap and row['id'] in fmap[fid]['unit_ids'], (row['id'], fid)
    lmap = {r['id']: r for r in ledgers}
    for f in findings:
        assert f['priority'] in {'high', 'medium', 'low'}, f['id']
        assert f['category'] in {'style', 'readability', 'claim', 'data', 'structure'}, f['id']
        assert f['verification'] in {'public_document', 'raw_checked', 'needs_source'}, f['id']
        assert f['target'] in {'source_of_truth', 'reading_layer', 'either'}, f['id']
        assert all(f.get(k) for k in ['problem', 'evidence', 'before', 'proposal', 'preserves', 'unit_ids']), f['id']
        assert isinstance(f['taxonomy_ids'], list), f['id']
        assert len(set(f['unit_ids'])) == len(f['unit_ids']), f['id']
        for uid in f['unit_ids']:
            assert uid in units and f['id'] in lmap[uid]['finding_ids'], (f['id'], uid)
        assert f['before'] in '\n'.join(units[u]['text'] for u in f['unit_ids']), f"quote not exact: {f['id']}"
    byfile=[]
    for file in manifest['files']:
        ids={u['id'] for u in units.values() if u['file']==file['file']}
        byfile.append({**{k:file[k] for k in ('file','lines','units','scope')},
            'verdicts':dict(collections.Counter(r['verdict'] for r in ledgers if r['id'] in ids)),
            'finding_ids':[f['id'] for f in findings if ids.intersection(f['unit_ids'])]})
    result={'research_commit':manifest['research_commit'], 'source_check_mode':'current' if args.current else 'git_baseline', 'files':len(byfile), 'units':len(units),
        'source_hashes_match':True,'nonblank_line_coverage_exactly_once':True,'ledger_ids_complete_unique':True,
        'bidirectional_finding_links_valid':True,'quoted_before_text_matches_source':True,
        'findings':len(findings), 'priorities':dict(collections.Counter(f['priority'] for f in findings)),
        'categories':dict(collections.Counter(f['category'] for f in findings)),
        'verification':dict(collections.Counter(f['verification'] for f in findings)),
        'verdicts':dict(collections.Counter(r['verdict'] for r in ledgers)), 'by_file':byfile,
        'note':'Reading coverage and report integrity, not validation of every underlying experiment.'}
    (HERE/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='by_file'},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
