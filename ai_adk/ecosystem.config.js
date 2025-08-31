const path = require('path');
const fs = require('fs');

const currentDir = __dirname;

module.exports = {
  apps: [{
    name: "ai-adk",
    version: "1.0.1",
    script: "uv",
    args: ["run", "adk", "web", "--host", "0.0.0.0", "--port", "5003"],
    cwd: currentDir,
    env: {
      PYTHONIOENCODING: 'UTF-8', // 解决中文乱码
    },
  }]
}