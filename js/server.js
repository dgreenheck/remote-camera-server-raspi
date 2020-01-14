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

function serveVideo(filename,req,res) {
  fs.stat(filename, function(err, stats) {
    if (err) {
      if (err.code === 'ENOENT') {
        res.writeHead(404);
        res.end();
        return;
      }
    }

    var start;
    var end;
    var total = 0;
    var contentRange = false;  // True if sending partial data
    var contentLength = 0;

    var range = req.headers.range;
    // If a range is specified in the header, parse it
    if (range) {
      var positions = range.replace(/bytes=/, "").split("-");
      start = parseInt(positions[0], 10);
      total = stats.size;

      // If no end specified, serve rest of the file
      end = positions[1] ? parseInt(positions[1], 10) : total - 1;

      var chunksize = (end - start) + 1;
      contentRange = true;
      contentLength = chunksize;
    }
    // Otherwise serve the entire file
    else {
      start = 0;
      end = stats.size;
      contentLength = stats.size
    }

    if (start <= end) {
      var responseCode = 200;
      var responseHeader = {
        "Accept-Ranges": "bytes",
        "Content-Length": contentLength,
        "Content-Type": "video/mp4"
      };
      // If sending partial data, specify the range in the header
      if (contentRange) {
        responseCode = 206;
        responseHeader["Content-Range"] = "bytes " + start + "-" + end + "/" + total;
      }
      res.writeHead(responseCode, responseHeader);

      var stream = fs.createReadStream(filename, { start: start, end: end}).on("readable", function() {
        var chunk;
        while (null !== (chunk = stream.read(1024))) {
           res.write(chunk);
        }
      }).on("error", function(err) {
        res.end(err);
      }).on("end", function(err) {
        res.end();
      });
    }
    else {
      // HTTP 403: Forbidden
      res.writeHead(403);
      res.end();
    }
  });
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
        serveVideo(filename,req,res);
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
