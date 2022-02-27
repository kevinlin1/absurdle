output = materials

submit: clean
	bundle install; bundle exec jekyll build
	mkdir -p $(output)
	cp -r _site/* $(output)
	sed -i 's/"\/absurdle\//"/g' $(output)/index.html
	pandoc README.md -o $(output)/instructor-guide.docx
	cp -r scaffold/ $(output)
	cp -r check/ $(output)
	zip $(output).zip -r -9 $(output)

clean:
	rm -rf $(output) $(output).zip
