const path = require('path');
const fs = require('fs');

const currentDir = __dirname;

module.exports = {
  apps: [{
    name: "ai-langchain",
    version: "1.0.1",
    script: "uv",
    args: ["run", "main.py"],
    cwd: currentDir,
    env: {
      PYTHONIOENCODING: 'UTF-8', // 解决中文乱码
    },
  }]
}