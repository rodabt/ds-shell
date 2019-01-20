validate:
	prospector

clean:
	rm -rf __EXPERIMENT__

update_local:
	git add . && git commit 

update_remote:
	git push origin master
