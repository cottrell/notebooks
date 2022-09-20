all:
	cat Makefile

install:
	# sudo npm install -g @vue/cli  # I think no longer used
	# do this to init a new project
	# npm init vue@latest

setup-hello-world:
	vue create hello-world
	cd hello-world
	# try to avoid adding anything if you don't need it
	# vue add vuetify  # mangle the template code to a vuetify starter template
	# npm i -s vuetify  # upgrade to latest vuetify
	# vue ui
	npm run server

enable_debugger:
	echo "edit rules in package.json "rules": { "no-unused-vars": 1, "no-debugger": "off" }"
