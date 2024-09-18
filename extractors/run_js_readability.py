#!/usr/bin/env python3
import gzip
import json
import subprocess
from pathlib import Path

# Path to your exec.js file
EXEC_JS_PATH = Path('./extractors/js_readability/exec.js')


def main():
    output = {}
    for path in Path('html').glob('*.html.gz'):
        with gzip.open(path, 'rt', encoding='utf8') as f:
            html = f.read()

        item_id = path.stem.split('.')[0]

        # Create a JSON object with the HTML content
        input_json = json.dumps({
            "html": html,
            "url": "https://www.example.com/the-source-page"
        })

        # Call exec.js with Node.js and pass the JSON through stdin

        result = subprocess.run(
            ['node', str(EXEC_JS_PATH)],
            input=input_json,
            capture_output=True,
            text=True,
            check=True
        )

        # Parse the JSON output from exec.js
        article = json.loads(result.stdout)
        output[item_id] = {'articleBody': article.get('textContent', '')}
        print(f"Processed {item_id}")

    (Path('output') / 'js_readability.json').write_text(
        json.dumps(output, sort_keys=True, ensure_ascii=False, indent=4),
        encoding='utf8'
    )


if __name__ == '__main__':
    main()
