const assert = require("node:assert/strict");
const test = require("node:test");
const { createServer } = require("../src/server");

function request(path) {
  const server = createServer();

  return new Promise((resolve, reject) => {
    server.listen(0, "127.0.0.1", () => {
      const { port } = server.address();
      const req = httpGet({ hostname: "127.0.0.1", port, path });
      req.then(resolve, reject).finally(() => server.close());
    });
  });
}

function httpGet(options) {
  return new Promise((resolve, reject) => {
    const req = require("node:http").request(options, (res) => {
      let body = "";
      res.setEncoding("utf8");
      res.on("data", (chunk) => {
        body += chunk;
      });
      res.on("end", () => {
        resolve({ statusCode: res.statusCode, headers: res.headers, body });
      });
    });
    req.on("error", reject);
    req.end();
  });
}

test("GET / still returns ok", async () => {
  const res = await request("/");

  assert.equal(res.statusCode, 200);
  assert.equal(res.body, "ok");
});

test("GET /health returns 200", async () => {
  const res = await request("/health");

  assert.equal(res.statusCode, 200);
});

test("/health returns application/json content type", async () => {
  const res = await request("/health");

  assert.equal(res.statusCode, 200);
  assert.match(res.headers["content-type"], /application\/json/);
});

test("/health body has status=ok and integer uptime_s", async () => {
  const res = await request("/health");
  const body = JSON.parse(res.body);

  assert.deepEqual(Object.keys(body).sort(), ["status", "uptime_s"]);
  assert.equal(body.status, "ok");
  assert.equal(Number.isInteger(body.uptime_s), true);
});
