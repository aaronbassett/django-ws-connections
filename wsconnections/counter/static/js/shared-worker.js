const connections = [];
var sharedWebSocket;

onconnect = function(e) {
  const port = e.ports[0];
  connections.push(port);
  port.start();

  if (!sharedWebSocket) {
    sharedWebSocket = new WebSocket(
      "ws://" + location.host + "/ws/count/" + location.hash.substring(1) + "/"
    );

    sharedWebSocket.onmessage = function(e) {
      connections.forEach(function(connection) {
        let data = JSON.parse(e.data);
        connection.postMessage(data);
      });
    };
  }

  sharedWebSocket.send("PING")
};
