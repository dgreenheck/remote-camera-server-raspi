var http = require('http');
var url = require('url');
var mongo = require('mongodb');
var MongoClient = require('mongodb').MongoClient;
var Server = require('mongodb').Server;

http.createServer(function(req,res) {
  // Get the arguments in the request URL
  var q = url.parse(req.url, true).query;

  // Build connection string for database
  var connectionString = 'mongodb://'
  connectionString = connectionString.concat(q.user,':',q.pass,'@localhost:27017/image_db')
  console.log(connectionString)
  
  MongoClient.connect(connectionString, function(err,db) {
    // Check for error in accessing database
    if (err) {
      console.log(err.message);
      if(err.message == 'auth fails') {
        // HTTP 401: Unauthorized
        res.writeHead(401);
        res.end();
        return;
      }
      else {
        // HTTP 500: Internal Server Error
        res.writeHead(500);
        res.end();
        return;
      }
    }
    console.log("Successfully connected to MongoDB");

    // Connect to the database
    var dbo = db.db("image_db");

    // Form query to retrieve image data
    dbo.collection("images").findOne({}, function(err, result) {
      if (err) throw err;

      if(result) {
      	// HTTP 200: Success
      	res.writeHead(200, {'Content-Type': 'text/html'});
      	res.write(JSON.stringify(result));
      	res.end();
      }
      else {
      	// HTTP 404: Not Found
      	res.writeHead(404);
      	res.end();
      }
    });
  });
}).listen(80);
