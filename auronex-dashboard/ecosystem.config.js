/**
 * PM2 Configuration - Production
 * Para rodar Next.js em produção com PM2
 */

module.exports = {
  apps: [
    {
      name: 'auronex-dashboard',
      script: 'node_modules/next/dist/bin/next',
      args: 'start -p 8501',
      cwd: './',
      instances: 'max', // Usar todos os CPUs disponíveis
      exec_mode: 'cluster',
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        PORT: 8501,
      },
      error_file: './logs/pm2-error.log',
      out_file: './logs/pm2-out.log',
      log_file: './logs/pm2-combined.log',
      time: true,
      autorestart: true,
      max_restarts: 10,
      min_uptime: '10s',
    },
  ],
}

