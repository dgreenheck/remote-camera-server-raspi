var http = require('http');
var url = require('url');
const fs = require('fs');
var mongo = require('mongodb');
var MongoClient = require('mongodb').MongoClient;
var Server = require('mongodb').Server;

function getFileSizeInBytes(filename) {
  var stats = fs.statSync(filename)
  var fileSizeInBytes = stats["size"]
  return fileSizeInBytes
}

// Directory where the video recordings are stored
const recordingsDir = '//home/admin/recordings/'

http.createServer(function(req,res) {
  // Parse the client request URL
  var q = url.parse(req.url, true);
  // Get the arguments in the request URL
  console.log(q.pathname);

  // Access security camera recordings
  if(q.pathname == '/recordings') {
    // If query is empty, return list of filenames
    if(Object.keys(q.query).length === 0) {
      console.log('Returning list of filenames')
      fs.readdir(recordingsDir, (err, files) => {
        if(err) {
          // Directory not found
          res.writeHead(404);
          res.end();
          return;
        }
        res.writeHead(200, {'Content-Type': 'application/json'});
        res.end(JSON.stringify(files));
      });
    }
    else {
      // Client requested specific file
      if(q.query.name) {
        console.log(q.query.name);
        // Get the file with the filename
        filename = recordingsDir.concat(q.query.name);

        fs.readFile(filename, function(err, data) {
          if(err) {
            // File not fou8nd
            res.writeHead(404);
            res.end();
            return;
          }
          // Return file data
          res.writeHead(200, {
            'Content-Type': 'video/mp4',
            'Content-Length': getFileSizeInBytes(filename)});

      	  res.end(data);
        });
      }
    }
  }
  else {
    // HTTP 404: Not Found
    res.writeHead(404, {'Content-Type': 'text/plain'})
    res.end('File not found');
  }
}).listen(80);
console.log('Listening on Port 80...')
