const functions = require('@google-cloud/functions-framework');

functions.http('helloHttp', (req, res) => {
  //res.send(`Hello ${req.query.name || req.body.name || 'World 101'}!`);
  res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Cloud Functions Demo</title>
    </head>
    <body style="background-color: lightyellow; color: black;">
      <h1>Welcome to Cloud Functions Demo</h1>
      <h2>Application Version: V2</h2>
    </body>
    </html>
  `);
});