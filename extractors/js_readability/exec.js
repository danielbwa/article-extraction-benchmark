var { Readability } = require('@mozilla/readability');
var { JSDOM } = require('jsdom');

let inputData = '';

process.stdin.on('data', chunk => {
    inputData += chunk;
});

process.stdin.on('end', () => {
    try {
        const input = JSON.parse(inputData);
        var doc = new JSDOM(input.html, {
            url: input.url
        });
        let reader = new Readability(doc.window.document);
        let article = reader.parse();

        // Output the result as JSON
        console.log(JSON.stringify(article));
    } catch (error) {
        console.error(JSON.stringify({ error: error.message }));
    }
});
