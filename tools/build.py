"""Regenerate the plugin's reference views in place, without a distribution copy."""
import argparse
import json

from _paths import MODEL_ROOT, ROOT
import flow
from flow_docs import build


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    model = flow.load_model()
    errors = flow.model_errors(model)
    if errors:
        print(json.dumps({'errors': errors}, ensure_ascii=False, indent=2))
        return 1
    return build(model, MODEL_ROOT, check=args.check, docs_root=ROOT / 'docs')


if __name__ == '__main__':
    raise SystemExit(main())
