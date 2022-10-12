module.exports = {
	apps: [
		{
			name: "worker",
			script: "npx",
			args: "yarn start",
			autorestart: true,
			max_memory_restart: "1G",
		},
	],
};