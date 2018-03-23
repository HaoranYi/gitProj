// debug run
// $ ts-node ./lib/server.ts

import app from "./app";
const port = 4040;
app.listen(port, function() {
  console.log('Express server listening on port ' + port);
});
