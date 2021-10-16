all:
	cat Makefile

install:
	sudo npm install -g @vue/cli

setup-hello-world:
	vue create hello-world
	cd hello-world
	vue add vuetify  # mangle the template code to a vuetify starter template
	npm i -s vuetify  # upgrade to latest vuetify
	# vue ui
	npm run server
