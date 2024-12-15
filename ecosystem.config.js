module.exports = {
  apps: [
    {
      name: 'PortalNano_bot',
      script: 'pnpx',
      args: 'pnpm start',
      autorestart: true,
      max_memory_restart: '1G',
    },
  ],
};
