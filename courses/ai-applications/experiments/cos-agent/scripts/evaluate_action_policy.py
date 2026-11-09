"""Run from cos-agent: python -X utf8 -m scripts.evaluate_action_policy --help."""
import argparse
import asyncio
import json

from beauty_agent.action_evaluation import (evaluate_cases, execution_manifest, load_cases, report_path)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Offline action case validation or fixed-state baseline replay. No model/API calls.')
    parser.add_argument('--cases', required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--validate-only', action='store_true')
    mode.add_argument('--planner', choices=['baseline'])
    parser.add_argument('--report', required=True)
    args = parser.parse_args(argv)
    try:
        target = report_path(args.report, [args.cases])
    except ValueError as exc:
        parser.error(str(exc))
    report = {'schema_version': 'action-policy-report-0.1', 'mode': 'development_preview',
              'production_enabled': False, 'run_kind': 'validate-only' if args.validate_only else 'baseline',
              'quality_claim': None}
    try:
        cases, validation, inputs = load_cases(args.cases)
        target = report_path(target, inputs)
        report.update(validation=validation, execution_manifest=execution_manifest(inputs),
                      selected_scenarios=len(cases), selected_turns=sum(len(c.turns) for c in cases))
        if not args.validate_only:
            report.update(asyncio.run(evaluate_cases(cases)))
        report['status'] = 'validated' if args.validate_only else 'replayed'
        exit_code = int(bool(report.get('summary', {}).get('execution_errors')))
    except (ValueError, KeyError, OSError) as exc:
        report.update(status='validation_failed', error_type=type(exc).__name__, error=str(exc))
        exit_code = 1
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    print(json.dumps({'status': report['status'], 'report': str(target),
                      'summary': report.get('summary'), 'error': report.get('error')}, ensure_ascii=False))
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
